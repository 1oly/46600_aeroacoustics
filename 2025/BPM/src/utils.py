import numpy as np
# This code is translated from https://github.com/byuflowlab/BPM.jl/blob/b5708e2284e17384c8a0957b72b6da181b90fe04/src/BPM.jl#L582
# Equations below refer to the report "Brooks, T. F., Pope, D. S., & Marcolini, M. A. (1989). Airfoil self-noise and prediction. Nasa Reference Publication, 1218."

# eq. (25/26)
def calc_spl(delta, M, L, Dh, r, A, K1, delta_K1):
    return 10.0 * np.log10(delta * M**5 * L * Dh / r**2) + A + K1 - 3 + delta_K1 # eq. (25/26)

def displacement_thickness(Re, c, alpha, trip=True):
    # eq. (3)
    if trip:  # heavily tripped boundary layer
        if Re <= 0.3e6:
            d0 = c * 0.0601 * Re**(-0.114)
        else:
            d0 = c * 10.0**(3.411 - 1.5397 * np.log10(Re) + 0.1059 * (np.log10(Re))**2)
    else:  # eq. (6) untripped boundary layer / clean
        d0 = c * 10.0**(3.0187 - 1.5397 * np.log10(Re) + 0.1059 * (np.log10(Re))**2)
    
    # eq. (9) Pressure Side Displacement Thickness
    dp = d0 * 10.0**(-0.0432 * alpha + 0.00113 * alpha**2)
    
    # Suction Side Displacement Thickness
    if trip: # eq. (12) 
        if alpha <= 5.0:
            ds = d0 * 10.0**(0.0679 * alpha)
        elif 5.0 < alpha <= 12.5:
            ds = d0 * 0.381 * 10.0**(0.1516 * alpha)
        else:
            ds = d0 * 14.296 * 10.0**(0.0258 * alpha)
    else: # eq. (15) 
        if alpha <= 7.5:
            ds = d0 * 10.0**(0.0679 * alpha)
        elif 7.5 < alpha <= 12.5:
            ds = d0 * 0.0162 * 10.0**(0.3066 * alpha)
        else:
            ds = d0 * 52.42 * 10.0**(0.0258 * alpha)
    
    return dp, ds

def Dhfunc(M, theta, phi):
    Mc = 0.8 * M  # assumed convection Mach number (pg. 107)
    # eq. (B1) directivity function
    Dh = 2 * np.sin(theta/2.0)**2 * np.sin(phi)**2 / ((1 + M * np.cos(theta)) * (1 + (M - Mc) * np.cos(theta))**2)
    return Dh

def Dlfunc(M, theta, phi):
    # eq. (B2) directivity function
    Dl = np.sin(theta)**2 * np.sin(phi)**2 / (1 + M * np.cos(theta))**4
    return Dl

def St2_func(alpha, St1):
    # eq. (34)
    if alpha <= 1.333:
        St2 = St1
    elif 1.333 < alpha <= 12.5:
        St2 = St1 * 10.0**(0.0054 * (alpha - 1.333)**2)
    else:
        St2 = St1 * 4.72
    return St2

def a0_func(Re):
    # eq. (38)
    if Re < 9.52e4:
        a0 = 0.57
    elif 9.52e4 <= Re <= 8.57e5:
        a0 = -9.57e-13 * (Re - 8.57e5)**2 + 1.13
    else:
        a0 = 1.13
    return a0

def Amin_func(a):
    # eq. (35)
    a = abs(a)
    if a < 0.204:
        Amin = np.sqrt(67.552 - 886.788 * a**2) - 8.219
    elif 0.204 <= a <= 0.244:
        Amin = -32.665 * a + 3.981
    else:
        Amin = -142.795 * a**3 + 103.656 * a**2 - 57.757 * a + 6.006
    return Amin

def Amax_func(a):
    # eq. (36)
    a = abs(a)
    if a < 0.13:
        Amax = np.sqrt(67.552 - 886.788 * a**2) - 8.219
    elif 0.13 <= a <= 0.321:
        Amax = -15.901 * a + 1.098
    else:
        Amax = -4.669 * a**3 + 3.491 * a**2 - 16.699 * a + 1.149
    return Amax

def K1_func(Re):
    # eq. (47)
    if Re < 2.47e5:
        K1 = -4.31 * np.log10(Re) + 156.3
    elif 2.47e5 <= Re < 8.0e5:
        K1 = -9.0 * np.log10(Re) + 181.6
    else:
        K1 = 128.5
    return K1

def delta_K1_func(Rp, alpha):
    # eq. (48)
    if Rp <= 5000.0:
        delta_K1 = -alpha * (5.29 - 1.43 * np.log10(Rp))
    else:
        delta_K1 = 0.0
    return delta_K1

### FUNCTIONS BELOW ARE FOR STALL CALCULATION (not implemented) ###

def b0_func(Re):
    # eq. (44)
    if Re < 9.52e4:
        b0 = 0.30
    elif 9.52e4 <= Re < 8.57e5:
        b0 = -4.48e-13 * (Re - 8.57e5)**2 + 0.56
    else:
        b0 = 0.56
    return b0

def Bmin_func(b):
    # eq. (41)
    b = abs(b)
    if b < 0.13:
        Bmin = np.sqrt(16.888 - 886.788 * b**2) - 4.109
    elif 0.13 <= b <= 0.145:
        Bmin = -83.607 * b + 8.138
    else:
        Bmin = -817.810 * b**3 + 355.210 * b**2 - 135.024 * b + 10.619
    return Bmin

def Bmax_func(b):
    # eq. (42)
    b = abs(b)
    if b < 0.10:
        Bmax = np.sqrt(16.888 - 886.788 * b**2) - 4.109
    elif 0.10 <= b <= 0.187:
        Bmax = -31.313 * b + 1.854 
    else:
        Bmax = -80.541 * b**3 + 44.174 * b**2 - 39.381 * b + 2.344
    return Bmax

def K2_func(alpha, M, K1):
    # eq. (49)
    gamma = 27.094 * M + 3.31
    beta = 72.650 * M + 10.74
    gamma0 = 23.430 * M + 4.651
    beta0 = -34.190 * M - 13.820

    if alpha <= gamma0 - gamma:
        K2 = K1 - 1000.0
    elif gamma0 - gamma < alpha <= gamma0 + gamma:
        K2 = K1 + np.sqrt(beta**2 - (beta/gamma)**2 * (alpha-gamma0)**2) + beta0
    else:
        K2 = K1 - 12.0
    return K2
