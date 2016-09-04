import numpy as np
from scipy.optimize import minimize

# General constants
ELECTRON_CHARGE = 1.60217662e-19
LIGHT_SPEED = 2.99792458e8
PERMITTIVITY = 8.854187817e-12
ELECTRON_REST_MASS = 9.10956e-31
PROTON_REST_MASS = 1.6726219e-27
AVOGADRO = 6.0221409e23

# For Si
SILICON_Z = 14
SILICON_REL_MASS = 28.0855
SILICON_DENSITY = 2328
SI_ELECTRON_DENSITY = (AVOGADRO * SILICON_Z * SILICON_DENSITY) / (SILICON_REL_MASS * 1)
SI_EXCITATION_POTENTIAL = 173


def ev_to_joules(energy):
    return energy*ELECTRON_CHARGE

def joules_to_ev(energy):
    return energy/ELECTRON_CHARGE

def beta(v):
    return v/LIGHT_SPEED

def gamma(beta):
    return 1 / np.sqrt(1 - (beta ** 2))

def proton_kin_en(vel):
    B = beta(vel)
    g = gamma(B)
    return (g*PROTON_REST_MASS*(LIGHT_SPEED**2)) - (PROTON_REST_MASS*(LIGHT_SPEED**2))

def proton_bethe(vel): # All SI units!
    B = beta(vel)
    term1 = (4 * np.pi) / (ELECTRON_REST_MASS * (LIGHT_SPEED**2))
    term2 = (SI_ELECTRON_DENSITY * 1)  / (B ** 2)
    term3 = (ELECTRON_CHARGE ** 2) / (4 * np.pi * PERMITTIVITY)
    term3 = term3 ** 2
    term4log = (2 * ELECTRON_REST_MASS * (LIGHT_SPEED**2) * (B ** 2)) / (SI_EXCITATION_POTENTIAL * (1 - (B ** 2)))
    term4 = np.log(term4log) - (B ** 2)
    return term1 * term2 * term3 * term4 * -1

def reverse_proton_bethe(lookup):
    # Use optimisation to reverse Bethe - get velocity
    func_to_min = lambda vel: abs(proton_bethe(vel) - lookup)
    vel = minimize(func_to_min, 1)
    return vel.x[0]

def proton_energy(de_dx):
    vel = reverse_proton_bethe(de_dx)
    return proton_kin_en(vel)
