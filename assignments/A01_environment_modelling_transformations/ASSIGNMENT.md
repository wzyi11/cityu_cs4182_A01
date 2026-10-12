# Assignment 1: Environment, Object Modelling, and Transformations

**Suggested period:** Weeks 1–3  
**Weight:** 10%  
**Aligned tutorial:** T1  
**Estimated workload:** 8–10 hours

## Purpose

Establish a reproducible Python/PyOpenGL environment and implement the transformations used to position a polygon mesh in a three-dimensional scene. OpenGL setup is diagnostic scaffolding; the assessed work is the mathematical transformation code.

## Learning outcomes

After completing this assignment, you should be able to:

1. represent points, triangles, and polygon meshes as NumPy arrays;
2. construct translation, rotation, and scaling matrices in homogeneous coordinates;
3. compose transformations in the intended order; and
4. verify a graphics environment and communicate enough information to reproduce it.

## Student tasks

Complete every `TODO` in `src/student.py`:

1. `translation_matrix(offset)`
2. `rotation_y_matrix(angle_degrees)`
3. `scaling_matrix(scale)`
4. `compose_model_matrix(offset, angle_degrees, scale)` using `T @ R @ S`
5. `transform_points(points, matrix)` using homogeneous coordinates

Then:

- run `environment_check.py` and copy its output into `report.md`;
- use `demo.py` to transform the supplied cube;
- add one second object or primitive to the demonstration; and
- compare `T @ R @ S` with one different transformation order.

Low-level mesh upload, shader compilation, and VAO/VBO/EBO implementation are not required.

## Required commands

```bash
python environment_check.py
python -m pytest -q
python demo.py
python demo.py --opengl       # optional interactive preview
```

## Submission

Submit `src/student.py`, your modified `demo.py`, `tests/`, `outputs/a01_transformed_objects.png`, `requirements.txt`, `README.md`, and a completed `report.md`.

## Report questions

1. In which coordinate space are the input cube vertices defined?
2. Why does changing the matrix multiplication order change the result?
3. What does the homogeneous coordinate `w` represent for a point?
4. State one environment problem you encountered and how you diagnosed it.

## Assessment

| Criterion | Marks |
|---|---:|
| Environment evidence and one-command execution | 10 |
| Translation, rotation, and scaling matrices | 30 |
| Matrix composition and transformation order | 25 |
| Homogeneous point transformation | 20 |
| Second object, tests, report, and code quality | 15 |
| **Total** | **100** |

## Minimum viable submission

A submission can pass if the environment evidence is present, all public matrix tests pass, and the transformed reference cube is saved successfully.
