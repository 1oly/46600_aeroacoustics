import numpy as np

# Physical parameters
V = [33,50,66,80]  # free stream velocity (m/s)
c0 = 335  # speed of sound (m/s)
c = 0.9  # chord length (m)
L = 1.0  # span (wetted by flow) (m)
r = 2.3  # observer distance (m)
alpha = [0, -2, -4, -6, -8, -10, -12, -14, -16,   2,   4,   6,   8, 10,  12,  14,  16]  # Angle of attack (degrees)
nu = 1.4529e-5  # air kinematic viscosity (m^2/s)
theta = np.pi/2  # Observer angle
phi = np.pi/2  # Observer angle
trip = False # trip tape True/False

outputfilename = "NACA_clean"

# Frequency parameters
f_min = 20.0  # Minimum frequency (Hz)
f_max = 10000.0  # Maximum frequency (Hz)
f_ref = 1000.0  # Reference frequency (Hz)
df = 0.1  # Frequency step in log scale

