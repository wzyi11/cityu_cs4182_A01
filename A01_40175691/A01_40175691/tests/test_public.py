import importlib
import os

import numpy as np

impl = importlib.import_module(os.environ.get("CS4182_IMPL_MODULE", "src.student"))


def test_translation_moves_a_point():
    matrix = impl.translation_matrix(np.array([2.0, -1.0, 0.5]))
    result = impl.transform_points(np.array([[1.0, 2.0, 3.0]]), matrix)
    np.testing.assert_allclose(result, [[3.0, 1.0, 3.5]], atol=1e-7)


def test_rotation_y_ninety_degrees():
    result = impl.transform_points(np.array([[1.0, 0.0, 0.0]]), impl.rotation_y_matrix(90.0))
    np.testing.assert_allclose(result, [[0.0, 0.0, -1.0]], atol=1e-7)


def test_nonuniform_scaling():
    result = impl.transform_points(
        np.array([[1.0, -2.0, 3.0]]), impl.scaling_matrix(np.array([2.0, 3.0, 4.0]))
    )
    np.testing.assert_allclose(result, [[2.0, -6.0, 12.0]], atol=1e-7)


def test_model_matrix_applies_scale_then_rotate_then_translate():
    matrix = impl.compose_model_matrix(np.array([1.0, 0.0, 0.0]), 90.0, 2.0)
    result = impl.transform_points(np.array([[1.0, 0.0, 0.0]]), matrix)
    np.testing.assert_allclose(result, [[1.0, 0.0, -2.0]], atol=1e-7)
