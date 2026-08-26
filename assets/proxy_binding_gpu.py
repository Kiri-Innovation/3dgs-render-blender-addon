"""GPU acceleration for the heaviest math step in proxy-rig bake:
rotating Spherical Harmonics coefficients per splat.

Why only SH rotation: at SH degree 3 the rotation step is roughly half of
compute_bound_state's per-frame cost (Fibonacci-sphere sample evaluation
plus per-degree pseudo-inverse multiply, repeated per splat). It's also
embarrassingly parallel — each splat is independent — so a one-thread-per-splat
compute shader maps directly.

Blender 5.1 has compute shaders and images via gpu.types but no SSBOs in
Python, so inputs/outputs go through RGBA32F GPUTextures (image-load/store).

Returns None on any failure so the caller falls back to the existing CPU
rotate_sh_coeffs. No way to test this out-of-Blender (background mode
disables GPU drawing), so failures are expected on first runs — fallback
keeps correctness.
"""

import numpy as np

try:
    import bpy
    import gpu
    _GPU_OK = True
except Exception:
    bpy = None
    gpu = None
    _GPU_OK = False


_SHADER_CACHE = {}
_CONST_TEX_CACHE = {}
_LAST_ERROR = None


# Texture-width default for packing. Wide-and-short fits typical GPU memory and
# keeps height < the 16384 hard limit even at 10M splats.
_TEX_WIDTH = 1024


_SH_ROTATION_GLSL_TEMPLATE = r"""
void main()
{
    int splat_id = int(gl_GlobalInvocationID.x);
    if (splat_id >= num_splats) return;

    int K = (sh_degree + 1) * (sh_degree + 1);
    int total_sh_floats = 3 * K;

    // ----- Load rotation matrix R for this splat -----
    int rot_row_base = splat_id * 3;
    int rb0 = rot_row_base + 0;
    int rb1 = rot_row_base + 1;
    int rb2 = rot_row_base + 2;
    vec3 R0 = imageLoad(rotation_in, ivec2(rb0 % rot_tex_w, rb0 / rot_tex_w)).rgb;
    vec3 R1 = imageLoad(rotation_in, ivec2(rb1 % rot_tex_w, rb1 / rot_tex_w)).rgb;
    vec3 R2 = imageLoad(rotation_in, ivec2(rb2 % rot_tex_w, rb2 / rot_tex_w)).rgb;
    // CPU semantics use a row-vector product (sample_dir * R). GLSL vectors
    // are columns, so storing the CPU rows as GLSL columns gives R^T * v,
    // which is the equivalent column-vector operation.
    mat3 R = mat3(R0, R1, R2);

    // ----- Load this splat's input SH coefficients -----
    // Layout: per splat, 3*K floats packed densely as (channel * K + band).
    // At max sh_degree=3, that's 48 floats = 12 RGBA texels per splat. The
    // shader always reads up to 12 texels; unused tail is zero-padded.
    float sh_in_vals[48];
    int sh_texel_base = splat_id * 12;
    for (int t = 0; t < 12; t++) {
        int texel_idx = sh_texel_base + t;
        vec4 v = imageLoad(sh_in, ivec2(texel_idx % sh_tex_w, texel_idx / sh_tex_w));
        sh_in_vals[t * 4 + 0] = v.x;
        sh_in_vals[t * 4 + 1] = v.y;
        sh_in_vals[t * 4 + 2] = v.z;
        sh_in_vals[t * 4 + 3] = v.w;
    }
    float sh_out_vals[48];
    for (int i = 0; i < 48; i++) sh_out_vals[i] = sh_in_vals[i];

    // ----- Accumulate per-degree rotation matrices (rb1=3x3, rb2=5x5, rb3=7x7) -----
    float rb_d1[9];   for (int i = 0; i < 9;  i++) rb_d1[i] = 0.0;
    float rb_d2[25];  for (int i = 0; i < 25; i++) rb_d2[i] = 0.0;
    float rb_d3[49];  for (int i = 0; i < 49; i++) rb_d3[i] = 0.0;

    for (int s = 0; s < num_samples; s++) {
        // Read sample direction s from sample_dirs_tex (single row, S texels)
        vec3 sd = imageLoad(sample_dirs_tex, ivec2(s, 0)).rgb;
        vec3 dir = R * sd;
        float x = dir.x, y = dir.y, z = dir.z;
        float xx = x * x, yy = y * y, zz = z * z;
        float xy = x * y, yz = y * z, xz = x * z;

        // Real SH basis at dir, bands 1..3
        float b1 = -SH_C1 * y;
        float b2 =  SH_C1 * z;
        float b3 = -SH_C1 * x;
        float b4 = SH_C2_0 * xy;
        float b5 = SH_C2_1 * yz;
        float b6 = SH_C2_2 * (2.0 * zz - xx - yy);
        float b7 = SH_C2_3 * xz;
        float b8 = SH_C2_4 * (xx - yy);
        float b9  = SH_C3_0 * y * (3.0 * xx - yy);
        float b10 = SH_C3_1 * xy * z;
        float b11 = SH_C3_2 * y * (4.0 * zz - xx - yy);
        float b12 = SH_C3_3 * z * (2.0 * zz - 3.0 * xx - 3.0 * yy);
        float b13 = SH_C3_4 * x * (4.0 * zz - xx - yy);
        float b14 = SH_C3_5 * z * (xx - yy);
        float b15 = SH_C3_6 * x * (xx - 3.0 * yy);

        // pinv_tex layout: rows = stacked degrees, columns = ceil(S/4) RGBA
        // texels. pinv_row_offset_d{d} gives the first row of degree d's
        // pseudoinverse block. Each row has block_size_d entries actually no
        // wait — rows of the pinv_block matrix are block_size_d × S each, so
        // each row stores S floats (one per sample direction).
        int pinv_col = s / 4;
        int pinv_chan = s - pinv_col * 4;

        if (sh_degree >= 1) {
            for (int row = 0; row < 3; row++) {
                vec4 pv = imageLoad(pinv_tex, ivec2(pinv_col, pinv_row_offset_d1 + row));
                float p = pinv_chan == 0 ? pv.x : (pinv_chan == 1 ? pv.y : (pinv_chan == 2 ? pv.z : pv.w));
                rb_d1[row * 3 + 0] += p * b1;
                rb_d1[row * 3 + 1] += p * b2;
                rb_d1[row * 3 + 2] += p * b3;
            }
        }
        if (sh_degree >= 2) {
            for (int row = 0; row < 5; row++) {
                vec4 pv = imageLoad(pinv_tex, ivec2(pinv_col, pinv_row_offset_d2 + row));
                float p = pinv_chan == 0 ? pv.x : (pinv_chan == 1 ? pv.y : (pinv_chan == 2 ? pv.z : pv.w));
                rb_d2[row * 5 + 0] += p * b4;
                rb_d2[row * 5 + 1] += p * b5;
                rb_d2[row * 5 + 2] += p * b6;
                rb_d2[row * 5 + 3] += p * b7;
                rb_d2[row * 5 + 4] += p * b8;
            }
        }
        if (sh_degree >= 3) {
            for (int row = 0; row < 7; row++) {
                vec4 pv = imageLoad(pinv_tex, ivec2(pinv_col, pinv_row_offset_d3 + row));
                float p = pinv_chan == 0 ? pv.x : (pinv_chan == 1 ? pv.y : (pinv_chan == 2 ? pv.z : pv.w));
                rb_d3[row * 7 + 0] += p * b9;
                rb_d3[row * 7 + 1] += p * b10;
                rb_d3[row * 7 + 2] += p * b11;
                rb_d3[row * 7 + 3] += p * b12;
                rb_d3[row * 7 + 4] += p * b13;
                rb_d3[row * 7 + 5] += p * b14;
                rb_d3[row * 7 + 6] += p * b15;
            }
        }
    }

    // ----- Apply rotation_block_d to per-channel coefficients -----
    // CPU semantics: rotated[n,c,j] = sum_i coeff[n,c,i] * rotation_block[n,j,i]
    if (sh_degree >= 1) {
        for (int c = 0; c < 3; c++) {
            for (int j = 0; j < 3; j++) {
                float acc = 0.0;
                for (int i = 0; i < 3; i++) {
                    acc += sh_in_vals[c * K + 1 + i] * rb_d1[j * 3 + i];
                }
                sh_out_vals[c * K + 1 + j] = acc;
            }
        }
    }
    if (sh_degree >= 2) {
        for (int c = 0; c < 3; c++) {
            for (int j = 0; j < 5; j++) {
                float acc = 0.0;
                for (int i = 0; i < 5; i++) {
                    acc += sh_in_vals[c * K + 4 + i] * rb_d2[j * 5 + i];
                }
                sh_out_vals[c * K + 4 + j] = acc;
            }
        }
    }
    if (sh_degree >= 3) {
        for (int c = 0; c < 3; c++) {
            for (int j = 0; j < 7; j++) {
                float acc = 0.0;
                for (int i = 0; i < 7; i++) {
                    acc += sh_in_vals[c * K + 9 + i] * rb_d3[j * 7 + i];
                }
                sh_out_vals[c * K + 9 + j] = acc;
            }
        }
    }

    // ----- Write back -----
    for (int t = 0; t < 12; t++) {
        int texel_idx = splat_id * 12 + t;
        imageStore(sh_out, ivec2(texel_idx % sh_tex_w, texel_idx / sh_tex_w),
                   vec4(sh_out_vals[t * 4 + 0],
                        sh_out_vals[t * 4 + 1],
                        sh_out_vals[t * 4 + 2],
                        sh_out_vals[t * 4 + 3]));
    }
}
"""


_SH_CONSTANTS_GLSL = r"""
#define SH_C1   0.4886025119029199
#define SH_C2_0 1.0925484305920792
#define SH_C2_1 -1.0925484305920792
#define SH_C2_2 0.31539156525252005
#define SH_C2_3 -1.0925484305920792
#define SH_C2_4 0.5462742152960396
#define SH_C3_0 -0.5900435899266435
#define SH_C3_1 2.890611442640554
#define SH_C3_2 -0.4570457994644658
#define SH_C3_3 0.3731763325901154
#define SH_C3_4 -0.4570457994644658
#define SH_C3_5 1.445305721320277
#define SH_C3_6 -0.5900435899266435
"""


def last_error():
    return _LAST_ERROR


def _last_error():
    # Backward-compat alias for callers using the underscore-prefixed form.
    return _LAST_ERROR


def _set_error(msg):
    global _LAST_ERROR
    _LAST_ERROR = msg


def is_available():
    if not _GPU_OK:
        return False
    try:
        return not bpy.app.background
    except Exception:
        return False


def clear_caches():
    global _LAST_ERROR
    _SHADER_CACHE.clear()
    _CONST_TEX_CACHE.clear()
    _LAST_ERROR = None


def _pack_to_rgba_2d(flat_floats, tex_width=_TEX_WIDTH):
    """Pack a 1D float array into a 2D RGBA32F image. Pads with zeros."""
    arr = np.asarray(flat_floats, dtype=np.float32).reshape(-1)
    pad_floats = (-arr.size) % 4
    if pad_floats:
        arr = np.concatenate([arr, np.zeros(pad_floats, dtype=np.float32)])
    n_texels = arr.size // 4
    height = (n_texels + tex_width - 1) // tex_width
    expected = height * tex_width * 4
    if arr.size < expected:
        padded = np.zeros(expected, dtype=np.float32)
        padded[: arr.size] = arr
        arr = padded
    return arr.reshape(height, tex_width, 4), tex_width, height


def _upload_rgba(rgba_arr):
    flat = np.ascontiguousarray(rgba_arr, dtype=np.float32).reshape(-1)
    try:
        buf = gpu.types.Buffer("FLOAT", flat.size, flat)
    except (TypeError, ValueError):
        buf = gpu.types.Buffer("FLOAT", flat.size, flat.tolist())
    height = rgba_arr.shape[0]
    width = rgba_arr.shape[1]
    return gpu.types.GPUTexture((width, height), format="RGBA32F", data=buf)


def _alloc_rgba(width, height):
    return gpu.types.GPUTexture((width, height), format="RGBA32F")


def _readback_rgba(tex):
    buf = tex.read()
    return np.array(buf, dtype=np.float32).reshape(tex.height, tex.width, 4)


def _build_shader(sh_degree, sample_count):
    """Build (and cache) the compute shader for this (sh_degree, sample_count)
    pair. Compile failures are cached as None so we don't retry."""
    key = (int(sh_degree), int(sample_count))
    if key in _SHADER_CACHE:
        return _SHADER_CACHE[key]
    if not _GPU_OK:
        return None
    try:
        info = gpu.types.GPUShaderCreateInfo()
        info.local_group_size(64, 1, 1)
        info.image(0, "RGBA32F", "FLOAT_2D", "rotation_in", qualifiers={"READ"})
        info.image(1, "RGBA32F", "FLOAT_2D", "sh_in", qualifiers={"READ"})
        info.image(2, "RGBA32F", "FLOAT_2D", "sh_out", qualifiers={"WRITE"})
        info.image(3, "RGBA32F", "FLOAT_2D", "sample_dirs_tex", qualifiers={"READ"})
        info.image(4, "RGBA32F", "FLOAT_2D", "pinv_tex", qualifiers={"READ"})
        info.push_constant("INT", "num_splats")
        info.push_constant("INT", "sh_degree")
        info.push_constant("INT", "num_samples")
        info.push_constant("INT", "rot_tex_w")
        info.push_constant("INT", "sh_tex_w")
        info.push_constant("INT", "pinv_row_offset_d1")
        info.push_constant("INT", "pinv_row_offset_d2")
        info.push_constant("INT", "pinv_row_offset_d3")
        info.compute_source(_SH_CONSTANTS_GLSL + _SH_ROTATION_GLSL_TEMPLATE)
        shader = gpu.shader.create_from_info(info)
        _SHADER_CACHE[key] = shader
        return shader
    except Exception as exc:
        _set_error(f"SH shader compile failed (degree={sh_degree}, samples={sample_count}): {exc}")
        _SHADER_CACHE[key] = None
        return None


def _get_const_textures(sh_degree, precompute):
    """Build (and cache) the constant textures: sample_dirs + stacked pinv
    blocks per degree. row_offsets gives the row at which each degree's block
    starts in the pinv texture. `precompute` is the dict returned by
    proxy_binding_utils.get_sh_rotation_precompute()."""
    sample_dirs = precompute["sample_dirs"]  # (S, 3)
    S = sample_dirs.shape[0]
    key = (int(sh_degree), int(S))
    if key in _CONST_TEX_CACHE:
        return _CONST_TEX_CACHE[key]

    sd_rgba = np.zeros((1, S, 4), dtype=np.float32)
    sd_rgba[0, :, :3] = sample_dirs
    sample_dirs_tex = _upload_rgba(sd_rgba)

    # Stack pinv blocks vertically (rows). Each row stores all S coefficients.
    # Pack S into ceil(S/4) RGBA32F columns.
    row_offsets = {}
    rows = []
    cur = 0
    for d in range(1, sh_degree + 1):
        block = precompute["pinv_blocks"][d]  # (block_size_d, S)
        row_offsets[d] = cur
        rows.append(block.astype(np.float32))
        cur += block.shape[0]
    if not rows:
        _CONST_TEX_CACHE[key] = (sample_dirs_tex, None, row_offsets, S)
        return _CONST_TEX_CACHE[key]
    stacked = np.concatenate(rows, axis=0)  # (total_rows, S)
    pad = (-S) % 4
    if pad:
        stacked = np.pad(stacked, ((0, 0), (0, pad)))
    pinv_w = (S + pad) // 4
    pinv_h = stacked.shape[0]
    pinv_rgba = stacked.reshape(pinv_h, pinv_w, 4)
    pinv_tex = _upload_rgba(pinv_rgba)

    _CONST_TEX_CACHE[key] = (sample_dirs_tex, pinv_tex, row_offsets, S)
    return _CONST_TEX_CACHE[key]


def rotate_sh_coeffs_gpu(sh_coeffs, rotation_matrices, sh_degree, precompute):
    """GPU port of proxy_binding_utils.rotate_sh_coeffs. Returns numpy array of
    same shape on success, or None on any failure so the caller falls back to
    CPU. Input shape (N, 3, K) where K = (sh_degree+1)**2. `precompute` is the
    dict returned by proxy_binding_utils.get_sh_rotation_precompute()."""
    if not _GPU_OK:
        return None
    if sh_degree <= 0:
        return np.asarray(sh_coeffs, dtype=np.float64).copy()

    sh_coeffs_arr = np.asarray(sh_coeffs, dtype=np.float64)
    if sh_coeffs_arr.ndim != 3 or sh_coeffs_arr.shape[1] != 3:
        return None
    N, _, K = sh_coeffs_arr.shape

    sample_count = int(precompute["sample_dirs"].shape[0])

    try:
        shader = _build_shader(sh_degree, sample_count)
        if shader is None:
            return None
        const = _get_const_textures(sh_degree, precompute)
        if const is None:
            return None
        sample_dirs_tex, pinv_tex, row_offsets, S = const
        if pinv_tex is None:
            return None

        # Pad input SH coeffs to (N, 3, 16) — max K for max degree — for fixed
        # 12-texel stride per splat in the shader.
        sh_padded = np.zeros((N, 3, 16), dtype=np.float32)
        sh_padded[:, :, :K] = sh_coeffs_arr.astype(np.float32)
        sh_flat = sh_padded.reshape(N, 3 * 16).reshape(-1)
        sh_rgba, sh_tw, sh_th = _pack_to_rgba_2d(sh_flat)
        sh_in_tex = _upload_rgba(sh_rgba)
        sh_out_tex = _alloc_rgba(sh_tw, sh_th)

        rot_arr = np.asarray(rotation_matrices, dtype=np.float32)
        # Pack rows of R as RGBA (xyz of each row, w=0)
        rows_rgba = np.zeros((rot_arr.shape[0] * 3, 4), dtype=np.float32)
        rows_rgba[:, :3] = rot_arr.reshape(rot_arr.shape[0] * 3, 3)
        rot_rgba, rot_tw, _ = _pack_to_rgba_2d(rows_rgba.reshape(-1))
        rot_in_tex = _upload_rgba(rot_rgba)

        shader.bind()
        shader.image("rotation_in", rot_in_tex)
        shader.image("sh_in", sh_in_tex)
        shader.image("sh_out", sh_out_tex)
        shader.image("sample_dirs_tex", sample_dirs_tex)
        shader.image("pinv_tex", pinv_tex)
        shader.uniform_int("num_splats", int(N))
        shader.uniform_int("sh_degree", int(sh_degree))
        shader.uniform_int("num_samples", int(S))
        shader.uniform_int("rot_tex_w", int(rot_tw))
        shader.uniform_int("sh_tex_w", int(sh_tw))
        shader.uniform_int("pinv_row_offset_d1", int(row_offsets.get(1, 0)))
        shader.uniform_int("pinv_row_offset_d2", int(row_offsets.get(2, 0)))
        shader.uniform_int("pinv_row_offset_d3", int(row_offsets.get(3, 0)))

        groups_x = (N + 63) // 64
        gpu.compute.dispatch(shader, int(groups_x), 1, 1)

        out_rgba = _readback_rgba(sh_out_tex)
        out_flat = out_rgba.reshape(-1)
        # We packed N * 3 * 16 floats — unpack to (N, 3, 16) then slice K
        out_unpacked = out_flat[: N * 3 * 16].reshape(N, 3, 16)
        return out_unpacked[:, :, :K].astype(np.float64)
    except Exception as exc:
        _set_error(f"SH dispatch failed: {exc}")
        return None
