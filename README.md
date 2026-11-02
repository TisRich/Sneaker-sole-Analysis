# Sneaker Sole Analysis

Static FEA in MATLAB of two EVA sneaker soles (flat and curved) under normal walking loads, compared with SolidWorks. This is a static study, so it does not cover running.

## Setup

- **Material:** EVA, E = 25 MPa, ν = 0.48
- **Load:** 934 N (about 1.2 × body weight), on a heel patch (heel strike) or the whole top surface (midfoot)
- **Supports:** base and sides fixed
- **Mesh:** 3 mm, chosen from a mesh convergence study with a 5% tolerance

## Results

| Case | Stress, MATLAB (MPa) | Stress, SolidWorks (MPa) | Displacement, MATLAB (mm) | Displacement, SolidWorks (mm) |
|---|---:|---:|---:|---:|
| Flat, heel strike | 0.583 | 0.161 | 0.413 | 0.102 |
| Flat, midfoot | 0.141 | 0.018 | 0.085 | 0.0128 |
| Curved, heel strike | 0.584 | 0.027 | 0.420 | 0.0128 |
| Curved, midfoot | 0.121 | 0.027 | 0.070 | 0.0064 |

![Peak von Mises stress](docs/charts/stress_comparison.svg)

![Peak displacement](docs/charts/displacement_comparison.svg)

**Takeaways**
- Heel strike causes about 4 to 5 times more stress than a midfoot landing.
- Under midfoot loading, the curved sole has about 15% less stress than the flat sole.
- Both tools show the same trends. MATLAB gives higher values, likely because the two tools apply supports and loads differently.

## Files

- `matlab/SoleFEM.m`: runs all four cases and saves the figures and Excel results
- `matlab/SoleFaces.m`: shows the face numbers of an STL
- `results/`: MATLAB figures, SolidWorks images, and the Excel summary
