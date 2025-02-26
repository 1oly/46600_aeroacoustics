import numpy as np
from utils import *

class Params:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def run_bpm_model(params):
    # Extract parameters
    V = params.V
    c0 = params.c0
    c = params.c
    L = params.L
    r = params.r
    alpha = params.alpha
    nu = params.nu
    theta = params.theta
    phi = params.phi
    f_min = params.f_min
    f_max = params.f_max
    f_ref = params.f_ref
    df = params.df
    trip = params.trip

    # Generate frequency array
    f = np.array([f_ref * 10.0**(df*n) for n in range(
        int(np.floor(np.log10(f_min/f_ref)/df)),
        int(np.ceil(np.log10(f_max/f_ref)/df)) + 1
    )])

    # Mach number
    M = V / c0
    # Reynolds number (chord-based)
    Re = V * c / nu
    # Compute boundary layer thickness
    dp, ds = displacement_thickness(Re, c, alpha, trip=trip)
    # Compute Reynolds numbers (delta-based)
    Rp = V * dp / nu
    Rs = V * ds / nu

    # Directivity functions
    Dl = Dlfunc(M, theta, phi)
    Dh = Dhfunc(M, theta, phi)

    # Determine peak Strouhal numbers
    St1 = 0.02 * M**(-0.6) # eq. (32)
    St2 = St2_func(alpha, St1) # eq. (33)
    St1bar = (St1 + St2) / 2.0

    # Construct A-curve
    a0 = a0_func(Re)
    Amin0 = Amin_func(a0)
    Amax0 = Amax_func(a0)
    A_ratio = (20 + Amin0) / (Amin0 - Amax0)

    # Construct A-curve A' used in eq. (30)
    ap0 = a0_func(3 * Re)
    Apmin0 = Amin_func(ap0)
    Apmax0 = Amax_func(ap0)
    Ap_ratio = (20 + Apmin0) / (Apmin0 - Apmax0)

    # Compute K1 and ΔK1
    K1 = K1_func(Re) # eq. (47)
    delta_K1 = delta_K1_func(Rp, alpha) # eq. (48)

    # Initialize arrays
    spl_p = np.zeros_like(f)
    spl_s = np.zeros_like(f)

    # Compute pressure for each frequency
    for i, freq in enumerate(f):
        # Pressure side
        Stp = freq * dp / V
        ap = np.log10(Stp / St1)
        Apmin = Amin_func(ap)
        Apmax = Amax_func(ap)
        Ap = Apmin + A_ratio * (Apmax - Apmin)
        spl_p[i] = calc_spl(dp, M, L, Dh, r, Ap, K1, delta_K1)

        # Suction side
        Sts = freq * ds / V
        as_ = np.log10(Sts / St1bar)
        Asmin = Amin_func(as_)
        Asmax = Amax_func(as_)
        As = Asmin + A_ratio * (Asmax - Asmin)
        spl_s[i] = calc_spl(ds, M, L, Dh, r, As, K1, 0)

    return f, spl_p, spl_s
