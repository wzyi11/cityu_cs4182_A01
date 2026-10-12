# A1 Starter

Complete `src/student.py`, run the public tests, and generate the required output with `python demo.py`.

The optional `--opengl` flag displays the same output using instructor-provided OpenGL infrastructure. You are not assessed on that infrastructure.

### Environment

I used **miniconda** to create an `env`, and I decided to create it in this folder.

```bash
# in this folder
cd A01_40175691

# create an env
conda create --prefix ./env python=3.12

# activate it
conda activate ./env

# download for the backages required
pip install -r requirements.txt

# test for the environment
python environment_check.py  # 'python' there uses the python.exe in the ./env
```

Use the `python.exe` in the `./env` folder.

### Test for 4 Functions
```bash 
python -m pytest -r
```

And can see `4 passed`.

### Get Transformed Results
```bash
python demo.py
python demo.py --opengl
```
Can see 3 images in the `output` folder.

### Pytest and CG_Framework
Need the two above to run successfully.
