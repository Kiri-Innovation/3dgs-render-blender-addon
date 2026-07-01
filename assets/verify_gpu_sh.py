"""Verification script — paste into Blender 5.1 Text Editor and Run.
Tests the GPU SH rotation against the CPU reference on a synthetic batch.
Reports max-abs-diff per SH band and per-frame time difference.

Expected:
  - max diff < 1e-3 (single-precision GPU vs double-precision CPU)
  - GPU should be measurably faster on N >= ~100k splats
"""

import importlib.util
import os
import sys
import time

import bpy
import numpy as np


ADDON_ROOT = os.path.dirname(bpy.context.preferences.addons[
    "bl_ext.user_default.dgs_render_by_kiri_engine"
].module if hasattr(bpy.context.preferences.addons.get("bl_ext.user_default.dgs_render_by_kiri_engine", None), "module") else __file__)

# Fallback: derive from common install location
if not os.path.isdir(ADDON_ROOT):
    ADDON_ROOT = os.path.expanduser(
        "~/Library/Application Support/Blender/5.1/extensions/user_default/dgs_render_by_kiri_engine"
    )

print(f"Addon root: {ADDON_ROOT}")
assets_dir = os.path.join(ADDON_ROOT, "assets")


def _force_reload(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules[name] = mod
    return mod


pbu = _force_reload("proxy_binding_utils", os.path.join(assets_dir, "proxy_binding_utils.py"))
gpu_mod = _force_reload("proxy_binding_gpu", os.path.join(assets_dir, "proxy_binding_gpu.py"))

# Synthetic batch
for N in (1_000, 100_000, 500_000):
    rng = np.random.default_rng(0)
    sh_degree = 3
    K = (sh_degree + 1) ** 2  # 16
    sh = rng.standard_normal((N, 3, K)).astype(np.float64)

    # Random near-identity rotation matrices (project random small perturbations
    # to nearest rotation via SVD so they're valid orthonormal matrices).
    pert = np.eye(3, dtype=np.float64) + rng.standard_normal((N, 3, 3)) * 0.1
    U, _, Vh = np.linalg.svd(pert)
    R = U @ Vh
    det = np.linalg.det(R)
    R[det < 0] *= -1.0  # ensure rotations, not reflections

    print(f"\n--- N = {N:,} ---")

    t0 = time.perf_counter()
    cpu_out = pbu.rotate_sh_coeffs(sh, R, sh_degree, sh_quality_mode="Final")
    cpu_ms = (time.perf_counter() - t0) * 1000.0
    print(f"  CPU rotate_sh_coeffs: {cpu_ms:.1f} ms")

    precompute = pbu.get_sh_rotation_precompute(sh_degree, sh_quality_mode="Final")
    t0 = time.perf_counter()
    gpu_out = gpu_mod.rotate_sh_coeffs_gpu(sh, R, sh_degree, precompute)
    gpu_ms = (time.perf_counter() - t0) * 1000.0

    if gpu_out is None:
        print(f"  GPU FAILED: {gpu_mod.last_error()}")
        continue

    print(f"  GPU rotate_sh_coeffs_gpu: {gpu_ms:.1f} ms  ({cpu_ms / gpu_ms:.1f}x)")

    diff = np.abs(cpu_out - gpu_out)
    print(f"  max |CPU - GPU| = {diff.max():.3e}")
    print(f"  mean |CPU - GPU| = {diff.mean():.3e}")

print("\nDone.")
