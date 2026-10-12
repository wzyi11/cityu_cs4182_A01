# A1 Report

**Student ID:**  40175691
**Name:**  Zhouyi Wu

## Environment evidence

```cmd
(E:\cityu\cs4182\Assignment_01\env) E:\cityu\cs4182\Assignment_01\assignments\A01_environment_modelling_transformations>python environment_check.py
Python: 3.12.14
Platform: Windows-11-10.0.26200-SP0
NumPy: 2.5.3
OpenGL vendor: Intel
OpenGL renderer: Intel(R) Arc(TM) Graphics
OpenGL version: 4.6.0 - Build 32.0.101.8132
GLSL version: 4.60 - Build 32.0.101.8132
```


## Transformation order

The demonstration compares `T @ R @ S` with `S @ R @ T` at `offset = [1.5, 0.5, -0.5]`, `angle = 40°`, `scale = [1.4, 0.7, 1.0]`. Matrix multiplication composes right-to-left, so the rightmost matrix is applied first: `T @ R @ S` scales and rotates the object about the origin and then moves it to `offset`, whereas `S @ R @ T` moves it first and then rotates and scales that displacement along with the geometry.

The difference is measurable. The cube starts centred on the origin, so its centroid after transformation shows where the model matrix puts the object:

| Order | Centroid | x extent |
|---|---|---|
| `T @ R @ S` | `[1.500, 0.500, -0.500]` | `[-0.22, 3.22]` |
| `S @ R @ T` | `[1.159, 0.350, -1.347]` | `[-0.81, 3.13]` |

`T @ R @ S` lands the centroid exactly on `offset`, so the offset means "where the object goes". `S @ R @ T` does not — left-multiplying the offset by `S @ R` gives `[1.159, 0.350, -1.347]`, exactly the centroid observed.

**Figure descriptions**:

- `outputs/a01_transformed_objects.png` — the supplied cube. Left panel `T @ R @ S`, right panel `S @ R @ T`.
  
- `outputs/a01_transformed_objects2.png` — a sphere centred on the origin. The anisotropic scale turns it into an ellipsoid, and the two panels show different ellipsoid axis directions, which makes the rotation/scaling non-commutativity directly visible.
- `outputs/a01_transformed_objects3.png` — a regular tetrahedron. 

## Coordinate-space questions

1. **In which coordinate space are the input cube vertices defined?**
   
   <p style="color: purple; text-decoration: underline; font-size:18px;">Model space </p>

   <p style="color: gray; font-style: italic;"> This center of the cube is the origin. And the abosolute value of the vertex coordinate is 1. </p>

2. **Why does changing the matrix multiplication order change the result?** 
   <p style="color: purple; ">Mathematically, changing the order of matrix multiplication does not guarantee identical results, and the operation may even become undefined.<br>
   Also <code>T @ R </code> means translation and rotation, but <code>R @ T</code> means rotation and translation.
   </p>


3. **What does the homogeneous coordinate `w` represent for a point?** 
   <ul>
      <li style="color:purple;">The homogeneous coordinate <i style=" color: blue">w</i> allows affine transformations such as translation to be written as a single 4×4 matrix multiplication.</li>
      <li style="color:purple;"><code>w = 1</code> denotes a point position and enables translation from the matrix’s last column.</li>
      <li style="color:purple;"><code>w = 0</code> denotes a direction vector, which ignores translation and only applies rotation and scaling.</li>
      <li style="color:purple;"><code>transform_points</code> sets <i style=" color: blue">w=1</i> and performs homogeneous division <code>[x,y,z,w]→[x/w,y/w,z/w]</code>. Here <i style=" color: blue">w</i> stays 1 so division does nothing.</li>
      <li style="color:purple;">In perspective projection, <i style=" color: blue">w</i> depends on depth, and dividing by <i style=" color: blue">w</i> produces perspective foreshortening.</li>
   </ul>


4. **State one environment problem you encountered and how you diagnosed it.** 
   I placed the Conda virtual environment directory within my project folder instead of Conda’s default `envs` folder. VS Code’s built-in terminal was unable to activate this project-local environment. For diagnosis, I tried activating the environment in Windows Command Prompt directly, and the environment activated as expected.

## Attribution and AI use declaration
- **Tool used:** Claude Code (Anthropic).

- **Prompts or task types:** 
   * summarising `ASSIGNMENT.md` and the package structure and explaining the four report questions; 
   * diagnosing why `python -m pytest` reported `No module named pytest` ; 
   * writing the second and third primitives in `demo.py`; 

- **Files or functions affected:** 
  * In `demo.py`, `sphere_mesh()`, `TETRA_VERTICES`/`TETRA_FACES`, `shade_faces()`, `save_comparison()`, the `faces`/`edge`/`alpha` parameters added to `draw()`, and the figure 2 and figure 3 blocks in `main()` were written by the AI. 

- **How I verified and understood it:** 
  * for the commandor `python -m pytest -r`, I answer my stategy in the *Question 4*.
  * for the `demo.py`:
    * `sphere_mesh(f, i, i)`: Use the `np.linespace` to get the points to descrtibe a sphere. The faces in a sphere is described by 4 points.
    * `TETRA`: Simple Math for a tetra.
    * `draw()`: Restrict it only for cube. Use give the value of variable `faces` with `FACE`, which is the faces of the cube. 
    * `save_comparison()`: Draw 2 panels and save them. 
    * `main()`: First, give the values of transformations. Second, tansform the three objects one by one, and draw and save them in the `outputs` folder.
 
