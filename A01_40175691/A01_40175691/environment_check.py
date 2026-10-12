"""Print reproducibility and optional OpenGL diagnostics for A1."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np

print(f"Python: {sys.version.split()[0]}")
print(f"Platform: {platform.platform()}")
print(f"NumPy: {np.__version__}")

try:
    from cg_framework.opengl_preview import collect_opengl_info

    info = collect_opengl_info()
    print(f"OpenGL vendor: {info.vendor}")
    print(f"OpenGL renderer: {info.renderer}")
    print(f"OpenGL version: {info.version}")
    print(f"GLSL version: {info.glsl_version}")
except Exception as exc:
    print(f"OpenGL diagnostics unavailable: {exc}")
    print("The NumPy tasks and tests can still be completed on this machine.")

