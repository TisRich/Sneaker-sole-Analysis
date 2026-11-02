# Sneaker Sole FEA: Flat vs Curved Sole, Heel Strike vs Midfoot Strike

Static finite element analysis of two EVA running-shoe soles designed in SolidWorks, solved in **MATLAB (PDE Toolbox)** and compared against **SolidWorks Simulation**.

The study asks how sole shape (flat vs curved heel) and landing pattern (rearfoot/heel strike vs midfoot strike) change the peak von Mises stress and the peak displacement in the sole at impact.

| | |
|---|---|
| **Material** | EVA foam, linear elastic, E = 25 MPa, ν = 0.48 |
| **Load** | 1946 N (437.5 lbf, about 2.5 × a 175 lb body weight) |
| **Heel strike** | Load on a heel patch centered 6 cm from the back of the sole (4 cm target diameter) |
| **Midfoot strike** | Load spread evenly over the whole top surface (assumes a flat-footed landing) |
| **Supports** | Every face except the loaded top face is fixed (base and sides), to match the SolidWorks setup |
| **Mesh** | Linear tetrahedra, Hmax = 3 mm |
| **Units** | STL in cm, scaled to SI (m, N, Pa) in the script |

---

## Results at a glance

| Case | MATLAB peak stress (MPa) | SolidWorks peak stress (MPa) | MATLAB peak displacement (mm) | SolidWorks peak displacement (mm) |
|---|---:|---:|---:|---:|
| Flat sole, heel strike | **1.215** | 0.410 | **0.860** | 0.368 |
| Flat sole, midfoot | 0.295 | 0.050 | 0.177 | 0.027 |
| Curved sole, heel strike | **1.217** | 0.027 | **0.876** | 0.013 |
| Curved sole, midfoot | 0.253 | 0.027 | 0.145 | 0.013 |

MATLAB values come from [`results/Combined_Midfoot_HeelStrike_Results.xlsx`](results/Combined_Midfoot_HeelStrike_Results.xlsx). SolidWorks values are the legend maximums read from the result images in [`results/solidworks/`](results/solidworks/).

### Peak von Mises stress

![Peak von Mises stress, MATLAB vs SolidWorks](docs/charts/stress_comparison.svg)

### Peak displacement

![Peak displacement, MATLAB vs SolidWorks](docs/charts/displacement_comparison.svg)

### How far apart the two tools are

![Ratio of MATLAB to SolidWorks results](docs/charts/matlab_vs_solidworks_ratio.svg)

### Load setup in MATLAB

![Loaded area and applied pressure per case](docs/charts/loading_setup.svg)

| Case | Loaded area (cm²) | Applied pressure (MPa) | Solve time (s) |
|---|---:|---:|---:|
| Flat sole, heel strike | 35.8 | 0.544 | 16.6 |
| Flat sole, midfoot | 167.7 | 0.116 | 13.2 |
| Curved sole, heel strike | 31.9 | 0.610 | 7.4 |
| Curved sole, midfoot | 205.7 | 0.095 | 6.1 |

---

## What the results say

**Landing pattern matters far more than sole shape (MATLAB).**
Heel strike puts the same force on about one fifth of the area, so the pressure is about 5 to 6.5 times higher. Peak stress rises about 4 to 5 times (0.25 to 0.30 MPa midfoot vs about 1.22 MPa heel strike) and peak displacement rises about 5 to 6 times.

**The flat and curved soles behave almost the same in MATLAB.**
Heel strike gives 1.215 vs 1.217 MPa. In midfoot strike the curved sole is about 14% lower in stress and 18% lower in displacement, because its top surface is larger (206 vs 168 cm²), which spreads the same force more thinly.

**SolidWorks agrees on the trend for the flat sole, but not on the size.**
Both tools say heel strike is much worse than midfoot strike for the flat sole (SolidWorks: 8 times the stress, 14 times the displacement). MATLAB's numbers are 2 to 7 times higher than SolidWorks'.

**The curved sole is where the tools disagree most.**
MATLAB is about 10 times higher for midfoot strike and 45 to 68 times higher for heel strike. In SolidWorks the curved sole shows nearly the same result for both landing patterns, which is not what you would expect when the loaded area shrinks five-fold.

## Why MATLAB and SolidWorks differ

These are the likely causes, roughly in order of impact. They are things to check, not confirmed answers.

1. **Which axis is "down" in the MATLAB model.** In the loading-region and face-identification plots the sole's width runs along **z** and its thickness along **y**. The script pushes along `loadDirection = [0; 0; -1]`, which would then be a sideways (shear) load across the width instead of a downward (compressive) load through the thickness. Shear on a near-incompressible foam is much softer than confined compression, which would explain the larger MATLAB displacement and stress. Checking the mesh dimensions printed by `SoleFEM.m` will confirm which axis is the 3.5 cm thickness.
2. **Shape of the heel patch.** The heel patch is selected with a circle in the x–y plane. If the thickness is along y, that circle becomes a 4 cm band across the full sole width, which is what the loading-region plots show (a rectangle of about 32 to 36 cm² instead of a 12.6 cm² circle). SolidWorks used its own heel region.
3. **Supports.** Fixing the base *and* the sides confines a material with ν = 0.48 almost completely, so the result is very sensitive to exactly which faces are fixed. SolidWorks and MATLAB split the faces differently (MATLAB fixes every face except the top).
4. **Curved sole SolidWorks results.** The curved heel-strike and curved midfoot stress plots have identical legends (2.457e-03 to 2.673e+04 N/m²), which suggests one of them may be showing the other study or a shared legend range. The flat midfoot displacement image also comes from a different study ("Static 4") than its stress image ("FinalMidfoot"). Re-exporting these from the same studies would make the comparison cleaner.
5. **Load magnitude.** The report lists 2.4 × BW (420 lbf) for the curved sole, while MATLAB applies 1946 N (2.5 × BW) to both. This only accounts for about 4%.
6. **Element type.** MATLAB uses linear tetrahedra, which are stiff for nearly incompressible materials (ν close to 0.5). A `'quadratic'` mesh and a mesh convergence check would tighten the MATLAB numbers.

## Figures

### MATLAB: flat sole

| Heel strike stress | Heel strike displacement |
|---|---|
| ![](results/matlab_figures/Flat_Sole_HeelStrike_Stress.png) | ![](results/matlab_figures/Flat_Sole_HeelStrike_Displacement.png) |
| **Midfoot stress** | **Midfoot displacement** |
| ![](results/matlab_figures/Flat_Sole_Midfoot_Stress.png) | ![](results/matlab_figures/Flat_Sole_Midfoot_Displacement.png) |
| **Heel strike loading region** | **Midfoot loading region** |
| ![](results/matlab_figures/Flat_Sole_HeelStrike_Loading_Region.png) | ![](results/matlab_figures/Flat_Sole_Midfoot_Loading_Region.png) |

### MATLAB: curved sole

| Heel strike stress | Heel strike displacement |
|---|---|
| ![](results/matlab_figures/Curved_Sole_HeelStrike_Stress.png) | ![](results/matlab_figures/Curved_Sole_HeelStrike_Displacement.png) |
| **Midfoot stress** | **Midfoot displacement** |
| ![](results/matlab_figures/Curved_Sole_Midfoot_Stress.png) | ![](results/matlab_figures/Curved_Sole_Midfoot_Displacement.png) |

### MATLAB: geometry and mesh

| Flat sole faces | Curved sole faces |
|---|---|
| ![](results/matlab_figures/Flat_Sole_Face_Identification.png) | ![](results/matlab_figures/Curved_Sole_Face_Identification.png) |
| **Flat sole mesh** | **Curved sole mesh** |
| ![](results/matlab_figures/Flat_Sole_Preliminary_Mesh.png) | ![](results/matlab_figures/Curved_Sole_Preliminary_Mesh.png) |

### SolidWorks Simulation

| Case | Stress | Displacement |
|---|---|---|
| Flat, heel strike | ![](results/solidworks/Flat_Sole_HeelStrike_Stress.jpg) | ![](results/solidworks/Flat_Sole_HeelStrike_Displacement.jpg) |
| Flat, midfoot | ![](results/solidworks/Flat_Sole_Midfoot_Stress.jpg) | ![](results/solidworks/Flat_Sole_Midfoot_Displacement.jpg) |
| Curved, heel strike | ![](results/solidworks/Curved_Sole_HeelStrike_Stress.jpg) | ![](results/solidworks/Curved_Sole_HeelStrike_Displacement.jpg) |
| Curved, midfoot | ![](results/solidworks/Curved_Sole_Midfoot_Stress.jpg) | ![](results/solidworks/Curved_Sole_Midfoot_Displacement.jpg) |

---

## Repository layout

```
matlab/
  SoleFEM.m        Main script: imports both STLs, meshes, runs midfoot and heel-strike cases, exports figures and Excel
  SoleFaces.m      Helper script to view face numbers of one STL (used to pick the loading face)
results/
  Combined_Midfoot_HeelStrike_Results.xlsx   MATLAB summary table (4 cases)
  matlab_figures/  PNG figures exported by SoleFEM.m
  solidworks/      SolidWorks Simulation result images
docs/
  charts/          README infographics (SVG)
  tools/make_charts.py   Rebuilds the charts (Python + matplotlib)
```

## How to run

1. MATLAB R2023a or later with the **Partial Differential Equation Toolbox**.
2. Export each sole from SolidWorks as STL and put the files next to `SoleFEM.m` as `Update_FlatS.STL` and `CurvedS.STL` (the STL files are not in this repository).
3. Run `SoleFaces.m` on a new STL to find the top (loading) face number, then set `loadFaces` in `SoleFEM.m`.
4. Create a `Results_Figures` folder next to the script, then run `SoleFEM.m`. It prints the mesh size, the load area and pressure, and the peak results for every case, and saves every figure (PNG and FIG) and the Excel table to `Results_Figures`.

Key settings at the top of `SoleFEM.m`:

| Variable | Meaning | Value used |
|---|---|---|
| `Hmax` | Maximum element size | 0.003 m |
| `meshOrder` | Element order | `'linear'` |
| `E`, `nu` | EVA properties | 25e6 Pa, 0.48 |
| `F` | Total impact force | 1946 N |
| `loadDirection` | Direction of the applied traction | `[0; 0; -1]` |
| `heelRadius`, `heelOffset` | Heel patch radius and distance from the back | 0.02 m, 0.06 m |
| `loadFaces` | Top face of each sole | `{2, 3}` |

## Next steps

- Confirm the sole's vertical axis and, if needed, change `loadDirection` and the heel-patch circle to match it.
- Switch to `'quadratic'` elements and run a mesh convergence check (Hmax of 5, 4, 3, and 2 mm).
- Re-export the curved sole SolidWorks studies and compare again.
- Add the transient (dynamic) heel-strike study, using a ground reaction force curve that rises to peak in about 25 ms with 3 to 9% damping.
