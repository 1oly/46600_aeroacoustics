import numpy as np
from scipy import stats

# Physical parameters
V = 50.73  # free stream velocity (m/s)
V_dist = stats.norm(V, 0.05 * V)

alpha = 3.39  # Angle of attack (degrees)

trip = False # trip tape True/False

outputfilename = "NACA_mc_Vdist"

# Data from measurement campaign:
c0 = 335  # speed of sound (m/s)
c = 0.9  # chord length (m)
L = 1.0  # span (wetted by flow) (m)
r = 2.3  # observer distance (m)
nu = 1.4529e-5  # air kinematic viscosity (m^2/s)
theta = np.pi/2  # Observer angle
phi = np.pi/2  # Observer angle

# Frequency parameters
f_min = 20.0  # Minimum frequency (Hz)
f_max = 10000.0  # Maximum frequency (Hz)
f_ref = 1000.0  # Reference frequency (Hz)
df = 0.1  # Frequency step in log scale

# Simulation parameters
num_simulations = 100  # Number of Monte Carlo simulations
