# Aeroacoustics 46600
Introduction to julia for the course [Aeroacoustics](https://kurser.dtu.dk/course/46600) at the Technical University of Denmark.

This tutorial will guide you through installing julia and getting familiar with the [AeroAcoustics.jl](https://github.com/1oly/AeroAcoustics.jl) package.

## Installation
[1. Install julia on your platform](https://julialang.org/downloads/)  
[2. Install VScode editor and julia extension](https://github.com/julia-vscode/julia-vscode#installing-juliavs-codevs-code-julia-extension)  
(If it's not working try adding `“C:\Users\[MY_USER]\AppData\Local\Programs\Julia-1.8.5\bin\julia.exe”` to VScode julia extension.)
3. Install additional packages to run `quick_start.jl` script. Enter package-manager by pressing `]`
```
pkg> add AeroAcoustics HDF5 PyPlot
```
Then locate ´quick_start.jl´ and run line-by-line in vscode.

A Jupyter notebook is also available.

## Data
The data provided in the `/data` directory contains cross-spectral matrices computed from acoustic array measurements conducted in [PLCT](https://plct.dk). The airfoil is a NACA63018 with a chord length of 0.9m and a span of 2m.

| Filename  | U0 [m/s] | Mach No. | AoA [deg] | Cl | Cd | Cm |
| ------------- | ------------- | --------------| ------- | ----| ---- | ---- |
| NACA63018_u0_50mps_aoa_0_clean.h5  | 50 | 0.1508  | 0 | 0.005 | 0.003 | -0.001
| NACA63018_u0_80mps_aoa_0_clean.h5  | 80 | 0.2404  | 0 | -0.008 | 0.005 | 0
| NACA63018_u0_80mps_aoa_6_clean.h5  | 80 | 0.2412  | 6 | 0.6527 | 0.011 | -0.016

The cross-spectral matrices are computed from 20 second time samples of 84 microphones using Welch's method with a Hanning window, a segment size of 4096 and 50% overlap. The narrow band data is subsequently summed into 1/12th octave bands.

## Implementing custom steeringvectors
The formulation of steeringvectors in AeroAcoustics.jl is defined [here](https://github.com/1oly/AeroAcoustics.jl/blob/master/src/steeringvectors.jl). These functions can serve as basis for implementing custom steeringvectors. Here is a short tutorial:
1. Start by copying the content of `steeringvectors.jl` to a new file, e.g., `my_awesome_steeringvectors.jl`
2. Rename the functions to not interfere with what is imported by AeroAcoustics.jl. Have a look at the cleaned version added to this repo.
3. Import the new implementation of your awesome steeringvectors with the line: `include("my_awesome_steeringvectors.jl)` in your main script. I have added this line to `quick_start.jl`
4. Call your own function in the script instead of the one from AeroAcoustics.jl, exchange `steeringvectors!(E)` with `my_custom_steeringvectors!(E)`.
