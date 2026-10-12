"""Assignment 1 student functions.

Replace each ``raise NotImplementedError`` with your own implementation. Do
not change the public function names or signatures.
"""

from __future__ import annotations

import numpy as np

import math


def translation_matrix(offset: np.ndarray) -> np.ndarray:
    """Return a 4 x 4 homogeneous translation matrix."""
    # TODO(A1.1): Validate the three-component offset and construct the matrix.

    if offset.shape != (3,): 
        print ("Invalidate Offset")

    res = np.eye(4)
    for i in range(3) :
        res[i, 3] = offset[i]

    return res
    
    # raise NotImplementedError("TODO(A1.1): implement translation_matrix")


def rotation_y_matrix(angle_degrees: float) -> np.ndarray:
    """Return a right-handed 4 x 4 rotation matrix about the y axis."""
    # TODO(A1.2): Convert degrees to radians and construct the matrix.

    radian = math.radians(angle_degrees)
    sin = math.sin(radian)
    cos = math.cos(radian)

    res = np.eye(4)
    res[0, 0] = cos
    res[0, 2] = sin
    res[2, 0] = -sin
    res[2, 2] = cos
    return res

    # raise NotImplementedError("TODO(A1.2): implement rotation_y_matrix")


def scaling_matrix(scale: float | np.ndarray) -> np.ndarray:
    """Return a 4 x 4 matrix for uniform or three-axis scaling."""
    # TODO(A1.3): Accept either one scalar or a three-component array.

    res = np.eye(4)

    if type(scale) == float:
        for i in range(3):
            res[i, i] = scale
        return res
    elif type(scale) == np.ndarray and scale.shape == (3,):
        for i in range(3):
            res[i, i] = scale[i]
        return res
    else:
        raise NotImplementedError("TODO(A1.3): implement scaling_matrix")


    # raise NotImplementedError("TODO(A1.3): implement scaling_matrix")


def compose_model_matrix(
    offset: np.ndarray, angle_degrees: float, scale: float | np.ndarray
) -> np.ndarray:
    """Return a model matrix that applies scale, then rotation, then translation."""
    # TODO(A1.4): Compose the matrices in the order T @ R @ S.

    res = np.eye(4)
    res = scaling_matrix(scale) @ res
    res = rotation_y_matrix(angle_degrees) @ res
    res = translation_matrix(offset) @ res
    return res

    # raise NotImplementedError("TODO(A1.4): implement compose_model_matrix")


def transform_points(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Transform an N x 3 point array and return Euclidean N x 3 coordinates."""
    # TODO(A1.5): Add w=1, apply the matrix, and perform the homogeneous divide.
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        pts = pts.reshape(1, -1)

    n = pts.shape[0]
    homogeneous = np.hstack([pts, np.ones((n, 1))])   # N x 4, w = 1
    transformed = homogeneous @ matrix.T              # 左乘矩阵
    w = transformed[:, 3:4]
    w = np.where(w == 0.0, 1.0, w)                    # 防除零

    return transformed[:, :3] / w                     # 齐次除法

