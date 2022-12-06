import numpy as np
import matplotlib.pyplot as plt
from lambwaves import Lamb

# You can obtain the values of c_L and c_S and an approximate value for
# c_R (if v > 0.3) from the material's mechanical properties by using 
# the following equations:
E = 68.9e9          # E = Young's modulus, in Pa.
p = 2700            # p = Density (rho), in kg/m3.
v = 0.33            # v = Poisson's ratio (nu).

"""
c_L: longitudinal wave velocity of the material
c_S: shear wave velocity of the material 
c_R: Rayleigh weave velocity of the material 
"""
c_L = np.sqrt(E*(1-v) / (p*(1+v)*(1-2*v)))
c_S = np.sqrt(E / (2*p*(1+v)))
c_R = c_S * ((0.862+1.14*v) / (1+v))

# Example: A 10 mm aluminum plate.

alum = Lamb(thickness=10,
            nmodes_sym=5,
            nmodes_antisym=5,
            fd_max=10000,
            vp_max=15000,
            c_L=c_L,
            c_S=c_S,
            c_R=c_R,
            material='Default')

# Plot phase velocity, group velocity and wavenumber.

alum.plot_phase_velocity()
alum.plot_group_velocity()
alum.plot_wave_number()

# Plot wave structure (displacement profiles across thickness) for A0
# and S0 modes at different fd values.

#alum.plot_wave_structure(mode='A0', nrows=3, ncols=2,
                         #fd=[500,1000,1500,2000,2500,3000])

#alum.plot_wave_structure(mode='S0', nrows=4, ncols=2,
                         #fd=[500,1000,1500,2000,2500,3000,3500,4000])

# Generate animations for A0 and S0 modes at 1000 kHz mm.

#alum.animate_displacement(mode='S0', fd=1000)
#alum.animate_displacement(mode='A0', fd=1000)

# Save all results to a txt file.

#alum.save_results()

plt.show()
