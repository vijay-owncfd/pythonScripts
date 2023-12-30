**Usage:** 
generateBackgroundMesh.py [-h] -stlPath STLPATH -dx DX -dy DY -dz DZ

**Description:**
Generate the background mesh for snappyHexMesh based on a given stl file and the base grid sizes in coordinate directions. Note: Base grid sizes should be positive values only.

**Options:**
  -h, --help        show this help message and exit
  -stlPath STLPATH  Path to the STL file.
  -dx DX            base grid size in x-direction
  -dy DY            base grid size in y-direction
  -dz DZ            base grid size in z-direction

image.png file shows how the background mesh covers the stl domain
