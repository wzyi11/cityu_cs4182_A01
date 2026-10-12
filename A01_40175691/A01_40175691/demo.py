"""Generate the Assignment 1 transformation-order comparison."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from cg_framework.figures import load_implementation, save_image

impl = load_implementation("src.student")

VERTICES = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
], dtype=float)
FACES = np.array([
    [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
    [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4],
])


# a sphere center on the origin
def sphere_mesh(radius: float = 1.0, n_lat: int = 12, n_lon: int = 18):
    """Return a sphere mesh centred on the origin as (N x 3 vertices, M x 4 faces).

    The sphere is a latitude/longitude grid: ``n_lat`` bands from pole to pole
    and ``n_lon`` slices around the y axis.  Every cell is a quad except at the
    two poles, where it degenerates to a triangle.
    """

    # np.linespace: like in matlab 
    theta = np.linspace(0.0, np.pi, n_lat + 1)   
    phi = np.linspace(0.0, 2.0 * np.pi, n_lon, endpoint=False)  

    vertices = np.array([
        [radius * np.sin(t) * np.cos(p),
         radius * np.cos(t),
         radius * np.sin(t) * np.sin(p)]
        for t in theta for p in phi
    ])

    faces = []
    for i in range(n_lat):
        for j in range(n_lon):
            a = i * n_lon + j                        
            b = i * n_lon + (j + 1) % n_lon          
            c = (i + 1) * n_lon + (j + 1) % n_lon    
            d = (i + 1) * n_lon + j                 
            faces.append([a, b, c, d])

    return vertices, np.array(faces)


# a tetra
TETRA = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float)
TETRA_VERTICES = TETRA / np.sqrt(3.0)
TETRA_FACES = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])


def shade_faces(vertices, faces, colour):
    """Return one RGB colour per face, shaded by a simple diffuse term.

    Poly3DCollection applies no lighting of its own, so a curved surface drawn
    with a single flat colour reads as a flat disc rather than a solid.  Taking
    the absolute value of the Lambert term keeps this robust to face winding
    (Poly3DCollection does not cull back faces, so the surface is double-sided).
    """
    polys = np.asarray(vertices)[np.asarray(faces)]
    normals = np.cross(polys[:, 1] - polys[:, 0], polys[:, 2] - polys[:, 0])
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = normals / np.where(lengths == 0.0, 1.0, lengths)

    light = np.array([0.4, -0.7, 0.8])          
    light = light / np.linalg.norm(light)
    lambert = np.abs(normals @ light)

    base = np.array(mcolors.to_rgb(colour))
    return base[None, :] * (0.35 + 0.65 * lambert)[:, None]   

# only for the cube now
def draw(ax, vertices, title, colour, faces=FACES, edge="#17324d", alpha=0.55):
    polygons = [vertices[face] for face in faces]
    ax.add_collection3d(Poly3DCollection(polygons, alpha=alpha, facecolor=colour, edgecolor=edge))
    ax.set(xlim=(-4, 4), ylim=(-4, 4), zlim=(-4, 4), xlabel="x", ylabel="y", zlabel="z", title=title)
    ax.set_box_aspect((1, 1, 1))


# 'NEW' save pictures
def save_comparison(path, panels, faces=FACES, edge="#17324d", alpha=0.55):
    """Draw two panels side by side and save them to ``path``.

    ``panels`` is ``[(vertices, title, colour), (vertices, title, colour)]``.
    Returns the rendered RGB image so ``--opengl`` can preview it.
    """
    fig = plt.figure(figsize=(10, 4.8))
    for index, (vertices, title, colour) in enumerate(panels):
        draw(fig.add_subplot(1, 2, index + 1, projection="3d"),
             vertices, title, colour, faces=faces, edge=edge, alpha=alpha)
    fig.tight_layout()
    canvas = fig.canvas
    canvas.draw()
    image = np.asarray(canvas.buffer_rgba())[..., :3]
    output = save_image(Path(path), image)
    plt.close(fig)
    print(f"Saved {output}")
    return image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--opengl", action="store_true")
    args = parser.parse_args()

    # transformation variables
    offset = np.array([1.5, 0.5, -0.5])
    scale = np.array([1.4, 0.7, 1.0])
    correct = impl.compose_model_matrix(offset, 40.0, scale)
    alternative = impl.scaling_matrix(scale) @ impl.rotation_y_matrix(40.0) @ impl.translation_matrix(offset)

    # cube
    image = save_comparison(
        "outputs/a01_transformed_objects.png",
        [
            (impl.transform_points(VERTICES, correct), "T @ R @ S", "#f5a623"),
            (impl.transform_points(VERTICES, alternative), "S @ R @ T", "#2aa198"),
        ],
    )

    # sphere
    sphere_vertices, sphere_faces = sphere_mesh(radius=1.0)
    sphere_left = impl.transform_points(sphere_vertices, correct)
    sphere_right = impl.transform_points(sphere_vertices, alternative)
    save_comparison(
        "outputs/a01_transformed_objects2.png",
        [
            (sphere_left, "Sphere: T @ R @ S", shade_faces(sphere_left, sphere_faces, "#f5a623")),
            (sphere_right, "Sphere: S @ R @ T", shade_faces(sphere_right, sphere_faces, "#2aa198")),
        ],
        faces=sphere_faces,
        edge="none",        # 12x18 条边会糊成一团，球面不画线框
        alpha=1.0,          # 着色画的是实心球，不要半透明
    )

    # tetra
    tetra_left = impl.transform_points(TETRA_VERTICES, correct)
    tetra_right = impl.transform_points(TETRA_VERTICES, alternative)
    save_comparison(
        "outputs/a01_transformed_objects3.png",
        [
            (tetra_left, "Tetrahedron: T @ R @ S", shade_faces(tetra_left, TETRA_FACES, "#f5a623")),
            (tetra_right, "Tetrahedron: S @ R @ T", shade_faces(tetra_right, TETRA_FACES, "#2aa198")),
        ],
        faces=TETRA_FACES,
        alpha=1.0,
    )

    if args.opengl:
        from cg_framework.opengl_preview import show_image

        show_image(image, "A1 Transformation Order")


if __name__ == "__main__":
    main()
