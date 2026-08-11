#define SH_C0 0.28209479177387814f
#define SH_C1 0.4886025119029199f

#define SH_C2_0 1.0925484305920792f
#define SH_C2_1 -1.0925484305920792f
#define SH_C2_2 0.31539156525252005f
#define SH_C2_3 -1.0925484305920792f
#define SH_C2_4 0.5462742152960396f

#define SH_C3_0 -0.5900435899266435f
#define SH_C3_1 2.890611442640554f
#define SH_C3_2 -0.4570457994644658f
#define SH_C3_3 0.3731763325901154f
#define SH_C3_4 -0.4570457994644658f
#define SH_C3_5 1.445305721320277f
#define SH_C3_6 -0.5900435899266435f

mat3 computeCov3D(vec3 scale, vec4 q) {
    mat3 S = mat3(0.0);
    S[0][0] = scale.x;
    S[1][1] = scale.y;
    S[2][2] = scale.z;
    
    float r = q.x;
    float x = q.y;
    float y = q.z;
    float z = q.w;

    mat3 R = mat3(
        1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - r * z), 2.0 * (x * z + r * y),
        2.0 * (x * y + r * z), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - r * x),
        2.0 * (x * z - r * y), 2.0 * (y * z + r * x), 1.0 - 2.0 * (x * x + y * y)
    );

    mat3 M = S * R;
    mat3 Sigma = transpose(M) * M;
    return Sigma;
}

vec3 computeCov2D(vec4 mean_view, float focal_x, float focal_y, float tan_fovx, float tan_fovy, mat3 cov3D, mat4 viewmatrix, bool is_orthographic) {
    vec4 t = mean_view;
    
    mat3 J;
    if (is_orthographic) {
        J = mat3(
            focal_x, 0.0, 0.0,
            0.0, focal_y, 0.0,
            0, 0, 0
        );
    } else {
        float limx = 1.3 * tan_fovx;
        float limy = 1.3 * tan_fovy;
        float txtz = t.x / t.z;
        float tytz = t.y / t.z;
        t.x = min(limx, max(-limx, txtz)) * t.z;
        t.y = min(limy, max(-limy, tytz)) * t.z;

        J = mat3(
            focal_x / t.z, 0.0, -(focal_x * t.x) / (t.z * t.z),
            0.0, focal_y / t.z, -(focal_y * t.y) / (t.z * t.z),
            0, 0, 0
        );
    }
    
    mat3 W = transpose(mat3(viewmatrix));
    mat3 T = W * J;

    mat3 cov = transpose(T) * transpose(cov3D) * T;
    cov[0][0] += 0.3;
    cov[1][1] += 0.3;
    return vec3(cov[0][0], cov[0][1], cov[1][1]);
}

ivec2 indexTo2D(int index, int texture_width) {
    int y = index / texture_width;
    int x = index - y * texture_width;
    return ivec2(x, y);
}

ivec3 indexTo3D(int index, int texture_width, int texture_height) {
    int z = index / (texture_width * texture_height);
    int remainder = index - z * (texture_width * texture_height);
    int y = remainder / texture_width;
    int x = remainder - y * texture_width;
    return ivec3(x, y, z);
}

struct ObjectMetadata {
    int start_idx;
    int gauss_count;
    float visibility;
    mat4 transform;
};

ObjectMetadata getObjectMetadata(int object_id) {
    ObjectMetadata metadata;
    
    int base_idx = object_id * 15;
    int texture_width = int(textureSize(object_metadata, 0).x);
    int texture_height = int(textureSize(object_metadata, 0).y);
    
    float start_idx_float = texelFetch(object_metadata, indexTo2D(base_idx + 0, texture_width), 0).r;
    metadata.start_idx = int(floatBitsToUint(start_idx_float));
    metadata.gauss_count = int(texelFetch(object_metadata, indexTo2D(base_idx + 1, texture_width), 0).r);
    metadata.visibility = texelFetch(object_metadata, indexTo2D(base_idx + 2, texture_width), 0).r;
    
    vec4 col0 = vec4(
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 0, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 1, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 2, texture_width), 0).r,
        0.0
    );
    vec4 col1 = vec4(
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 3, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 4, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 5, texture_width), 0).r,
        0.0
    );
    vec4 col2 = vec4(
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 6, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 7, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 8, texture_width), 0).r,
        0.0
    );
    vec4 col3 = vec4(
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 9, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 10, texture_width), 0).r,
        texelFetch(object_metadata, indexTo2D(base_idx + 3 + 11, texture_width), 0).r,
        1.0
    );
    
    metadata.transform = mat4(col0, col1, col2, col3);
    
    return metadata;
}

int determineObjectFromGaussianIndex(int gaussian_index) {
    ivec2 texture_size = textureSize(object_metadata, 0);
    int texture_width = texture_size.x;
    int texture_height = texture_size.y;
    int total_floats = texture_width * texture_height;
    int num_objects = total_floats / 15;
    
    for (int obj_id = 0; obj_id < num_objects; obj_id++) {
        ObjectMetadata meta = getObjectMetadata(obj_id);
        if (gaussian_index >= meta.start_idx && gaussian_index < (meta.start_idx + meta.gauss_count)) {
            return obj_id;
        }
    }
    
    return 0;
}

vec3 getSHCoeff(int gaussian_index, int sh_index, int texture_width, int texture_height) {
    int gaussian_stride = 59;
    int base_index = gaussian_index * gaussian_stride;
    int coeff_index = base_index + 11 + sh_index * 3;
    return vec3(
        texelFetch(gaussian_data, indexTo3D(coeff_index, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(coeff_index + 1, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(coeff_index + 2, texture_width, texture_height), 0).r
    );
}

vec3 evaluateSH(int gaussian_index, vec3 dir, int texture_width, int texture_height) {
    vec3 color = SH_C0 * getSHCoeff(gaussian_index, 0, texture_width, texture_height);
    
    if (sh_degree >= 1) {
        float x = dir.x;
        float y = dir.y;
        float z = dir.z;
        color = color - SH_C1 * y * getSHCoeff(gaussian_index, 1, texture_width, texture_height) + 
                        SH_C1 * z * getSHCoeff(gaussian_index, 2, texture_width, texture_height) - 
                        SH_C1 * x * getSHCoeff(gaussian_index, 3, texture_width, texture_height);
        
        if (sh_degree >= 2) {
            float xx = x * x, yy = y * y, zz = z * z;
            float xy = x * y, yz = y * z, xz = x * z;
            color = color +
                SH_C2_0 * xy * getSHCoeff(gaussian_index, 4, texture_width, texture_height) +
                SH_C2_1 * yz * getSHCoeff(gaussian_index, 5, texture_width, texture_height) +
                SH_C2_2 * (2.0 * zz - xx - yy) * getSHCoeff(gaussian_index, 6, texture_width, texture_height) +
                SH_C2_3 * xz * getSHCoeff(gaussian_index, 7, texture_width, texture_height) +
                SH_C2_4 * (xx - yy) * getSHCoeff(gaussian_index, 8, texture_width, texture_height);
            
            if (sh_degree >= 3) {
                color = color +
                    SH_C3_0 * y * (3.0 * xx - yy) * getSHCoeff(gaussian_index, 9, texture_width, texture_height) +
                    SH_C3_1 * xy * z * getSHCoeff(gaussian_index, 10, texture_width, texture_height) +
                    SH_C3_2 * y * (4.0 * zz - xx - yy) * getSHCoeff(gaussian_index, 11, texture_width, texture_height) +
                    SH_C3_3 * z * (2.0 * zz - 3.0 * xx - 3.0 * yy) * getSHCoeff(gaussian_index, 12, texture_width, texture_height) +
                    SH_C3_4 * x * (4.0 * zz - xx - yy) * getSHCoeff(gaussian_index, 13, texture_width, texture_height) +
                    SH_C3_5 * z * (xx - yy) * getSHCoeff(gaussian_index, 14, texture_width, texture_height) +
                    SH_C3_6 * x * (xx - 3.0 * yy) * getSHCoeff(gaussian_index, 15, texture_width, texture_height);
            }
        }
    }
    
    return color + 0.5;
}

mat3 quaternionToMatrix(vec4 q) {
    float r = q.x;
    float x = q.y;
    float y = q.z;
    float z = q.w;
    return mat3(
        1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - r * z), 2.0 * (x * z + r * y),
        2.0 * (x * y + r * z), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - r * x),
        2.0 * (x * z - r * y), 2.0 * (y * z + r * x), 1.0 - 2.0 * (x * x + y * y)
    );
}

vec4 relightLightPosition(int index) {
    if (index == 0) return relight_light_position_0;
    if (index == 1) return relight_light_position_1;
    if (index == 2) return relight_light_position_2;
    return relight_light_position_3;
}

vec4 relightLightColor(int index) {
    if (index == 0) return relight_light_color_0;
    if (index == 1) return relight_light_color_1;
    if (index == 2) return relight_light_color_2;
    return relight_light_color_3;
}

vec4 relightLightSettings(int index) {
    if (index == 0) return relight_light_settings_0;
    if (index == 1) return relight_light_settings_1;
    if (index == 2) return relight_light_settings_2;
    return relight_light_settings_3;
}

int shadowLightIndex(int index) {
    if (index == 0) return shadow_light_index_0;
    if (index == 1) return shadow_light_index_1;
    if (index == 2) return shadow_light_index_2;
    return shadow_light_index_3;
}

mat4 shadowViewMatrix(int index) {
    if (index == 0) return shadow_view_matrix_0;
    if (index == 1) return shadow_view_matrix_1;
    if (index == 2) return shadow_view_matrix_2;
    return shadow_view_matrix_3;
}

mat4 shadowProjectionMatrix(int index) {
    if (index == 0) return shadow_projection_matrix_0;
    if (index == 1) return shadow_projection_matrix_1;
    if (index == 2) return shadow_projection_matrix_2;
    return shadow_projection_matrix_3;
}

float meshShadowDepth(int index, vec2 uv) {
    if (index == 0) return texture(mesh_shadow_depth_0, uv).r;
    if (index == 1) return texture(mesh_shadow_depth_1, uv).r;
    if (index == 2) return texture(mesh_shadow_depth_2, uv).r;
    return texture(mesh_shadow_depth_3, uv).r;
}

float meshShadowVisibility(vec3 world_position, vec3 normal, int light_index) {
    if (shadow_enabled == 0) return 1.0;
    int map_index = -1;
    for (int index = 0; index < 4; index++) {
        if (index >= shadow_light_count) break;
        if (shadowLightIndex(index) == light_index) {
            map_index = index;
            break;
        }
    }
    if (map_index < 0) return 1.0;
    vec3 biased_position = world_position + normal * relight_settings.w;
    mat4 view_matrix = shadowViewMatrix(map_index);
    vec4 shadow_clip = shadowProjectionMatrix(map_index) * view_matrix * vec4(biased_position, 1.0);
    vec3 shadow_ndc = shadow_clip.xyz / shadow_clip.w;
    vec2 shadow_uv = shadow_ndc.xy * 0.5 + 0.5;
    if (any(lessThan(shadow_uv, vec2(0.0))) || any(greaterThan(shadow_uv, vec2(1.0))) || shadow_ndc.z < -1.0 || shadow_ndc.z > 1.0) return 1.0;
    float receiver_depth = -(view_matrix * vec4(biased_position, 1.0)).z;
    vec2 texel = shadow_filter_radius / vec2(textureSize(mesh_shadow_depth_0, 0));
    float visibility = 0.0;
    for (int x = -1; x <= 1; x++) {
        for (int y = -1; y <= 1; y++) {
            float caster_depth = meshShadowDepth(map_index, shadow_uv + vec2(x, y) * texel);
            visibility += receiver_depth > caster_depth + relight_settings.y ? 0.0 : 1.0;
        }
    }
    return visibility / 9.0;
}

vec4 proxyShadowLayer(int index, vec2 uv) {
    if (index == 0) return texture(proxy_shadow_layer_0, uv);
    if (index == 1) return texture(proxy_shadow_layer_1, uv);
    if (index == 2) return texture(proxy_shadow_layer_2, uv);
    return texture(proxy_shadow_layer_3, uv);
}

float proxyShadowTransmission(vec3 world_position, vec3 normal, int light_index) {
    if (shadow_enabled == 0 || light_index != shadow_light_index_0 || proxy_shadow_layer_count == 0) return 1.0;
    vec3 biased_position = world_position + normal * relight_settings.w;
    vec4 shadow_clip = shadow_projection_matrix_0 * shadow_view_matrix_0 * vec4(biased_position, 1.0);
    vec3 shadow_ndc = shadow_clip.xyz / shadow_clip.w;
    vec2 shadow_uv = shadow_ndc.xy * 0.5 + 0.5;
    if (any(lessThan(shadow_uv, vec2(0.0))) || any(greaterThan(shadow_uv, vec2(1.0)))) return 1.0;
    float receiver_depth = -(shadow_view_matrix_0 * vec4(biased_position, 1.0)).z;
    float layer_fraction = (receiver_depth - proxy_shadow_depth_range.x) / max(proxy_shadow_depth_range.y - proxy_shadow_depth_range.x, 0.0001);
    int receiver_layer = int(floor(layer_fraction * float(proxy_shadow_layer_count)));
    float transmission = 1.0;
    for (int index = 0; index < 4; index++) {
        if (index >= receiver_layer || index >= proxy_shadow_layer_count) break;
        transmission *= 1.0 - clamp(proxyShadowLayer(index, shadow_uv).a * relight_settings.z, 0.0, 1.0);
    }
    return transmission;
}

vec3 evaluateRelighting(vec3 base_color, vec3 world_position, vec4 rotation, vec3 scale, mat4 object_transform) {
    if (relight_mode == 0) return base_color;

    int smallest_axis = scale.x < scale.y ? (scale.x < scale.z ? 0 : 2) : (scale.y < scale.z ? 1 : 2);
    vec3 local_normal = smallest_axis == 0 ? vec3(1.0, 0.0, 0.0) : (smallest_axis == 1 ? vec3(0.0, 1.0, 0.0) : vec3(0.0, 0.0, 1.0));
    vec3 normal = normalize(transpose(inverse(mat3(object_transform))) * (quaternionToMatrix(rotation) * local_normal));
    if (dot(normal, camera_position - world_position) < 0.0) normal = -normal;
    vec3 irradiance = vec3(0.0);

    for (int index = 0; index < 4; index++) {
        if (index >= relight_light_count) break;
        vec4 light_position = relightLightPosition(index);
        vec4 light_color = relightLightColor(index);
        vec4 light_settings = relightLightSettings(index);
        vec3 light_dir;
        float attenuation = 1.0;
        if (light_position.w < 0.5) {
            light_dir = normalize(light_position.xyz);
        } else {
            vec3 light_delta = light_position.xyz - world_position;
            float distance_to_light = length(light_delta);
            light_dir = light_delta / max(distance_to_light, 0.0001);
            attenuation = 1.0 / max(distance_to_light * distance_to_light, 1.0);
            if (light_settings.x > 0.0) {
                attenuation *= clamp(1.0 - distance_to_light / light_settings.x, 0.0, 1.0);
            }
        }
        float normal_light = dot(normal, light_dir);
        if (relight_response == 0) {
            normal_light = max(normal_light, 0.0);
        } else if (relight_response == 1) {
            normal_light = max(normal_light, 0.0) + max(-normal_light, 0.0) * 0.15;
        } else if (relight_response == 2) {
            normal_light = abs(normal_light);
        } else {
            // Standard 3DGS has no trustworthy normal/albedo decomposition. Preserve its appearance and relight by visibility.
            normal_light = 1.0;
        }
        irradiance += light_color.rgb * light_color.a * normal_light * attenuation * meshShadowVisibility(world_position, normal, index) * proxyShadowTransmission(world_position, normal, index);
    }
    return base_color * (relight_ambient.rgb * relight_ambient.a + irradiance * relight_settings.x);
}

void main()
{
    int instance_id = gl_InstanceID;
    
    int indices_width = int(indices_dimensions.x);
    int indices_y = instance_id / indices_width;
    int indices_x = instance_id - indices_y * indices_width;
    int gaussian_index = int(texelFetch(sorted_indices, ivec2(indices_x, indices_y), 0).r);
    
    int gaussian_stride = 59;
    int base_index = gaussian_index * gaussian_stride;
    int texture_width = int(texture_dimensions.x);
    int texture_height = int(texture_dimensions.y);
    
    vec3 g_pos = vec3(
        texelFetch(gaussian_data, indexTo3D(base_index + 0, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(base_index + 1, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(base_index + 2, texture_width, texture_height), 0).r
    );
    
    int object_id = determineObjectFromGaussianIndex(gaussian_index);
    ObjectMetadata obj_metadata = getObjectMetadata(object_id);
    
    if (obj_metadata.visibility < 0.5) {
        gl_Position = vec4(-100, -100, -100, 1);
        return;
    }
    
    vec4 g_pos_transformed = obj_metadata.transform * vec4(g_pos, 1.0);
    g_pos = g_pos_transformed.xyz;
    
    vec4 g_rot = vec4(
        texelFetch(gaussian_data, indexTo3D(base_index + 3, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(base_index + 4, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(base_index + 5, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(base_index + 6, texture_width, texture_height), 0).r
    );
    
    vec3 g_scale = vec3(
        texelFetch(gaussian_data, indexTo3D(base_index + 7, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(base_index + 8, texture_width, texture_height), 0).r,
        texelFetch(gaussian_data, indexTo3D(base_index + 9, texture_width, texture_height), 0).r
    );
    
    float g_opacity = texelFetch(gaussian_data, indexTo3D(base_index + 10, texture_width, texture_height), 0).r;
    
    vec4 g_pos_view = ViewMatrix * vec4(g_pos, 1.0);
    vec4 g_pos_screen = ProjectionMatrix * g_pos_view;
    
    bool is_orthographic = (ProjectionMatrix[3][3] > 0.5);
    g_pos_screen.xyz = g_pos_screen.xyz / g_pos_screen.w;
    g_pos_screen.w = 1.0;
    
    if (any(greaterThan(abs(g_pos_screen.xyz), vec3(1.3)))) {
        gl_Position = vec4(-100, -100, -100, 1);
        return;
    }
    
    mat3 cov3d = computeCov3D(g_scale, g_rot);
    
    vec3 focal_params = focal_parameters;
    float focal_x = focal_params.x;
    float focal_y = focal_params.y;
    float focal_z = focal_params.z;
    
    float tan_fovx = 1.0 / focal_x;
    float tan_fovy = 1.0 / focal_y;
    
    vec3 cov2d = computeCov2D(g_pos_view, focal_z, focal_z, tan_fovx, tan_fovy, cov3d, ViewMatrix * obj_metadata.transform, is_orthographic);
    
    float det = (cov2d.x * cov2d.z - cov2d.y * cov2d.y);
    if (det == 0.0) {
        gl_Position = vec4(0.0, 0.0, 0.0, 0.0);
        return;
    }
    
    float det_inv = 1.0 / det;
    vec3 conic = vec3(cov2d.z * det_inv, -cov2d.y * det_inv, cov2d.x * det_inv);
    
    vec2 quadwh_scr = vec2(3.0 * sqrt(cov2d.x), 3.0 * sqrt(cov2d.z));
    vec2 wh = 2.0 * focal_parameters.xy * focal_parameters.z;
    vec2 quadwh_ndc = quadwh_scr / wh * 2.0;
    
    g_pos_screen.xy = g_pos_screen.xy + quad_coord * quadwh_ndc;
    vec2 coordxy = quad_coord * quadwh_scr;
    
    gl_Position = g_pos_screen;
    
    vec3 g_color;
    
    if (render_mode != 1) {
        vec3 view_dir = normalize(g_pos - camera_position);
        g_color = relight_mode == 2
            ? SH_C0 * getSHCoeff(gaussian_index, 0, texture_width, texture_height) + 0.5
            : evaluateSH(gaussian_index, view_dir, texture_width, texture_height);
        g_color = evaluateRelighting(g_color, g_pos, g_rot, g_scale, obj_metadata.transform);
    } else {
        float depth = -g_pos_view.z;
        float depth_normalized = depth / 100.0;
        g_color = vec3(depth_normalized, depth_normalized, depth_normalized);
    }
    
    v_color = g_color;
    v_alpha = g_opacity;
    v_conic = conic;
    v_coordxy = coordxy;
    v_rotation = g_rot;
    v_render_mode = render_mode;
    v_depth = (g_pos_screen.z + 1.0) * 0.5;
}
