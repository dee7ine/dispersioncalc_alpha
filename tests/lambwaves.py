import numpy as np

import matplotlib.pyplot as plt

import scipy.optimize

from numerical_methods.Plot_utilities import add_plot, add_cutoff_freqs, add_velocities
from numerical_methods.Utilities import interpolate, correct_instability, write_txt, find_max

class Lamb:
    """A class used to calculate and plot Lamb wave dispersion curves 
    for traction-free, homogeneous and isotropic plates. It also allows 
    to generate an animation of the displacement vector field.
    
    Methods
    -------
    plot_phase_velocity(modes, cutoff_frequencies, material_velocities,
                        save_img, sym_style, antisym_style):
        Plot phase velocity as a function of frequency × thickness.
    plot_group_velocity(modes, cutoff_frequencies, save_img, sym_style,
                        antisym_style):
        Plot group velocity as a function of frequency × thickness.
    plot_wave_number(modes, save_img, sym_style, antisym_style):
        Plot wavenumber as a function of frequency × thickness.
    plot_wave_structure(mode, nrows, ncols, fd, save_img, inplane_style,
                        outofplane_style):
        Plot particle displacement across the thickness of the plate.
    animate_displacement(mode, fd, speed, save_gif, save_video):
        Generate an animation of the displacement vector field.
    save_results()
        Save all results to a txt file.

    Attributes
    ----------
    vp_sym:
        Dictionary with phase velocity interpolators for symmetric 
        modes.
    vg_sym:
        Dictionary with group velocity interpolators for symmetric 
        modes.
    k_sym:
        Dictionary with wavenumber interpolators for symmetric 
        modes.
    vp_antisym:
        Dictionary with phase velocity interpolators for antisymmetric 
        modes.
    vg_antisym:
        Dictionary with group velocity interpolators for antisymmetric 
        modes.
    k_antisym:
       Dictionary with wavenumber interpolators for antisymmetric 
       modes.

    """


    
    def __init__(self, thickness, nmodes_sym, nmodes_antisym, fd_max, vp_max, 
                 c_L, c_S, c_R = None, fd_points=100, vp_step=100, 
                 material=''):
        """"
        Parameters
        ----------
        thickness : float or int
            Thickness of the plate, in mm.
        nmodes_sym : int
            Number of symmetric modes to calculate.
        nmodes_antisym : int
            Number of antisymmetric modes to calculate.
        fd_max : float or int
            Maximum value of frequency × thickness to calculate.
        vp_max : float or int
            Maximum value of phase velocity to calculate, in m/s.
        c_L : float or int
            Longitudinal wave velocity of the material, in m/s.
        c_S: float or int
            Shear wave velocity of the material, in m/s.
        c_R: float or int, optional
            Rayleigh wave velocity of the material, in m/s.     
        fd_points : int, optional
            Number of frequency × thickness points.
        vp_step : int, optional
            Increment between phase velocity intervals.
        material : str, optional
            Name of the material being analyzed.
            
        """
        
        self.d = thickness/1e3
        self.h = (thickness/2)/1e3
        self.nmodes_sym = nmodes_sym
        self.nmodes_antisym = nmodes_antisym
        self.fd_max = fd_max
        self.vp_max = vp_max
        self.c_L = c_L
        self.c_S = c_S
        self.c_R = c_R
        self.fd_points = fd_points
        self.vp_step = vp_step
        self.material = material
        
        # Solve the dispersion equations.
        
        sym = self._solve_disp_eqn(function=self._symmetric, 
                                   nmodes=nmodes_sym, 
                                   c=c_S, 
                                   label='S')
        
        antisym = self._solve_disp_eqn(function=self._antisymmetric, 
                                       nmodes=nmodes_antisym, 
                                       c=c_L, 
                                       label='A')
        
        # Calculate group velocity (vg) and wavenumber (k) from phase 
        # velocity (vp) and interpolate all results.
        
        self.vp_sym, self.vg_sym, self.k_sym = interpolate(sym, self.d)
        self.vp_antisym, self.vg_antisym, self.k_antisym = interpolate(antisym, 
                                                                       self.d)

    def _calc_constants(self, vp, fd):
        """Calculate the constants p and q (defined to simplify the 
        dispersion equations) and wavenumber from a pair of phase 
        velocity and frequency × thickness product.
        
        Parameters
        ----------
        vp : float or int
            Phase velocity.
        fd : float or int
            Frequency × thickness product.
        
        Returns
        -------
        k : float
            Wavenumber.
        p, q : float
            A pair of constants introduced to simplify the dispersion 
            relations.
            
        """
        
        omega = 2*np.pi*(fd/self.d)
        
        k = omega/vp
    
        p = np.sqrt((omega/self.c_L)**2 - k**2, dtype=np.complex128)
        q = np.sqrt((omega/self.c_S)**2 - k**2, dtype=np.complex128)

        return k, p, q

    def _symmetric(self, vp, fd):
        """Rayleigh-Lamb frequency relation for symmetric modes, used to 
        determine the velocity at which a wave of a particular frequency 
        will propagate within the plate. The roots of this equation are 
        used to generate the dispersion curves.

        Parameters
        ----------
        vp : float or int
            Phase velocity.
        fd : float or int
            Frequency × thickness product.
        
        Returns
        -------
        symmetric : float
            Dispersion relation for symmetric modes.
        
        """
        
        k, p, q = self._calc_constants(vp, fd)
    
        symmetric = (np.tan(q*self.h)/q
                     + (4*(k**2)*p*np.tan(p*self.h))/(q**2 - k**2)**2)

        return np.real(symmetric)
        
    def _antisymmetric(self, vp, fd):
        """Rayleigh-Lamb frequency relation for antisymmetric modes, 
        used to determine the velocity at which a wave of a particular 
        frequency will propagate within the plate. The roots of this 
        equation are used to generate the dispersion curves.

        Parameters
        ----------
        vp : float or int
            Phase velocity.
        fd : float or int
            Frequency × thickness product.
            
        Returns
        -------
        antisymmetric : float
            Dispersion relation for antisymmetric modes.
            
        """
        
        k, p, q = self._calc_constants(vp, fd)

        antisymmetric = (q * np.tan(q*self.h)
                         + (((q**2 - k**2)**2)*np.tan(p*self.h))/(4*(k**2)*p))

        return np.real(antisymmetric)
    
    def _calc_wave_structure(self, modes, vp, fd, y):
        """Calculate the wave structure across the thickness of the 
        plate.
        
        Parameters
        ----------
        modes : {'A', 'S'}
            Family of modes to analyze. Can be 'A' (antisymmetric modes) 
            or 'S' (symmetric modes).
        vp : float or int
            Phase velocity.
        fd : float or int
            Frequency × thickness product.
        y : array
            Array representing thickness values to calculate wave 
            structure, from -d/2 to d/2.
            
        Returns
        -------
        u : array
            In plane displacement profile.
        w : array
            Out of plane plane displacement profile.
            
        """
        
        k, p, q = self._calc_constants(vp, fd)
        
        if modes == 'S':
            C = 1
            B = -2*k*q*np.cos(q*self.h) / ((k**2 - q**2) * np.cos(p*self.h))   
            u = 1j*(k*B*np.cos(p*y) + q*C*np.cos(q*y))
            w = -p*B*np.sin(p*y) + k*C*np.sin(q*y)
        elif modes == 'A':
            D = 1
            A = 2*k*q*np.sin(q*self.h) / ((k**2 - q**2) * np.sin(p*self.h))
            u = 1j*(k*A*np.sin(p*y) - q*D*np.sin(q*y))
            w = p*A*np.cos(p*y) + k*D*np.cos(q*y)

        return u, w        

    def _solve_disp_eqn(self, function, nmodes, c, label):
        """Function to calculate the numerical solution to the 
        dispersion equations.
        
        The algorithm works as follows:
            
            1) Fix a value of frequency × thickness product.
            2) Evaluate the function at two values of phase velocity 
               (vp and vp+step) and check their signs.
            3) Since the function is continuous, if the sign changes  
               in the interval under analysis, a root exists in this 
               interval. Use the bisection method to locate it 
               precisely.
            4) Continue searching for other roots at this value of 
               frequency × thickness.
            5) Change the value of frequency × thickness and repeat 
               steps 2 to 4.

        Parameters
        ----------
        function : {self._symmetric, self._antisymmetric}
            Family of modes to solve. Can be `self._symmetric` (to solve 
            symmetric modes) or `self._antisymmetric` (to solve 
            antisymmetric modes).
            
        Returns
        -------
        result_dict : dict
            A dictionary, where the keys are the corresponding mode 
            (e.g., 'A0', 'A1', 'A2', ..., 'An' for antisymmetric modes 
             or 'S0', 'S1', 'S2', ..., 'Sn' for symmetric modes) and the 
            values are numpy arrays of dimensions (2, fd_points), where 
            the first row has the fd values and the second row has the 
            phase velocity values calculated.
            
        """
                        
        fd_arr = np.linspace(0, self.fd_max, self.fd_points)      
        result = np.zeros((len(fd_arr), nmodes + 1))
        
        print(f'\nCalculating {function.__name__[1:]} modes..\n')
        
        for i, fd in enumerate(fd_arr):
            
            print(f'{i}/{self.fd_points} - {np.around(fd, 1)} kHz × mm')
        
            result[i][0] = fd
        
            j = 1
            
            vp_1 = 0
            vp_2 = self.vp_step

            while vp_2 < self.vp_max:
                x_1 = function(vp_1, fd)
                x_2 = function(vp_2, fd)

                if j < nmodes + 1:
                    if not np.isnan(x_1) and not np.isnan(x_2):
                        if np.sign(x_1) != np.sign(x_2):
                            bisection = scipy.optimize.bisect(f=function, 
                                                              a=vp_1, 
                                                              b=vp_2, 
                                                              args=(fd,))
                            
                            # TO FIX: I don't know why at some points 
                            # the function changes sign, but the roots
                            # found by the bisect method don't evaluate 
                            # to zero.
                            
                            # For now, these values are ignored (only
                            # take into account those values that 
                            # evaluate to 0.01 or less).
                            
                            if (np.abs(function(bisection, fd)) < 1e-2 and not
                                    np.isclose(bisection, c)):
                                
                                result[i][j] = bisection
                                j += 1
                                
                vp_1 = vp_2
                vp_2 = vp_2 + self.vp_step
        
        # Correct some instabilities and replace zeros with NaN, so it
        # is easier to filter.
           
        result = correct_instability(result, function)
        result[result == 0] = np.nan
        
        result_dict = {}
        
        for nmode in range(nmodes):
            
            # Filter all NaN values.
            
            mode_result = np.vstack((result[:, 0], result[:, nmode + 1]))
            mode_result = mode_result[:, ~np.isnan(mode_result).any(axis=0)]
            
            # Append to a dictionary with keys 'An' or 'Sn'.
            
            result_dict[label + str(nmode)] = mode_result
        
        return result_dict
    

    
    def plot(self, ax, result, y_max, cutoff_frequencies=False, 
             arrow_dir=None, material_velocities=False, plt_kwargs={}):
        """Generate a dispersion plot for a family of modes (symmetric
        or antisymmetric).
        
        Parameters
        ----------
        ax : axes
            Matplotlib axes in which the plot will be added.
        result : dict
            A dictionary with a result (vp, vg or k) interpolator at 
            each mode.
        y_max : float or int
            Maximum y value in the plot. 
        cutoff_frequencies : bool, optional
            Set to True to add cutoff frequencies to the plot.
        arrow_dir : {'up', 'down'}, optional
            Set arrows direction of cutoff frequencies. Can be 'up' (for 
            group velocity plots) or 'down' (for phase velocity plots).
        material_velocities : bool, optional
            Add material velocities (longitudinal, shear and Rayleigh) 
            to the plot. Defaults to True.       
        plt_kwargs : dict, optional
            Matplotlib kwargs (to change color, linewidth, linestyle, 
            etc.).
                    
        """
        
        for mode, arr in result.items():
            
            # Generate an fd array for each mode and add the 
            # corresponding mode plot.
            
            fd = np.arange(np.amin(arr.x), np.amax(arr.x), 0.1)
            add_plot(ax, result, mode, fd, **plt_kwargs)   
            
            if cutoff_frequencies:
                add_cutoff_freqs(ax, mode, arrow_dir, y_max, 
                                 self.c_L, self.c_S)
        
        if material_velocities:
            add_velocities(ax, self.c_L, self.c_S, self.c_R, self.fd_max)
                
        ax.set_xlim([0, self.fd_max])
        ax.set_ylim([0, y_max])
        
        ax.set_xlabel('Frequency × thickness [KHz × mm]')
        
    def plot_phase_velocity(self, modes='both', cutoff_frequencies=True, 
                            material_velocities=True, save_img=False,
                            sym_style={'color': 'blue'},
                            antisym_style={'color': 'red','linestyle' : '--'}):
        """Generate a plot of phase velocity as a function of frequency 
        × thickness.
        
        Parameters
        ----------
        modes : {'both', 'symmetric', 'antisymmetric'}, optional
            Which family of modes to plot. Can be 'symmetric', 
            'antisymmetric' or 'both'. Defaults to 'both'.
        cutoff_frequencies : bool, optional
            Add cutoff frequencies to the plot. Defaults to True.
        material_velocities : bool, optional
            Add material velocities (longitudinal, shear and Rayleigh) 
            to the plot. Defaults to True.
        save_img : bool, optional
            Save the result image as png. Defaults to False.
        sym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the symmetric 
            curves (to change color, linewidth, linestyle, etc.).
        antisym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the 
            antisymmetric curves (to change color, linewidth, linestyle, 
            etc.).
            
        Returns
        -------
        fig, ax : matplotlib objects
            The figure and the axes of the generated plot.
            
        """
        
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.canvas.set_window_title('Phase Velocity')
        
        # Calculate the maximum value to scale the ylim of the axes.
        
        max_sym, max_antisym = find_max(self.vp_sym), find_max(self.vp_antisym)
        
        if modes == 'symmetric':
            self.plot(ax, self.vp_sym, max_sym, cutoff_frequencies, 'down', 
                      material_velocities, plt_kwargs=sym_style)
        elif modes == 'antisymmetric':
            self.plot(ax, self.vp_antisym, max_antisym, cutoff_frequencies, 
                      'down', material_velocities, plt_kwargs=antisym_style)
        elif modes == 'both':
            max_ = max(max_sym, max_antisym)
            self.plot(ax, self.vp_sym, max_, cutoff_frequencies, 
                      'down', material_velocities, plt_kwargs=sym_style)
            self.plot(ax, self.vp_antisym, max_, cutoff_frequencies, 
                      'down', material_velocities, plt_kwargs=antisym_style)
        else:
            raise Exception('modes must be "symmetric", "antisymmetric"'
                            'or "both".') 
            
        ax.legend(loc='lower right')
        ax.set_ylabel('Phase Velocity [m/s]')
        
        if save_img:
            fig.savefig(f'results/Phase Velocity - {self.d*1e3} mm '
                        f'{self.material} plate.png', 
                        bbox_inches='tight')
        
        return fig, ax

    def plot_group_velocity(self, modes='both', cutoff_frequencies=True, 
                            save_img=False, sym_style={'color': 'blue'}, 
                            antisym_style={'color': 'red', 'linestyle' : '--'}):
        """Generate a plot of group velocity as a function of frequency 
        × thickness.
        
        Parameters
        ----------
        modes : {'both', 'symmetric', 'antisymmetric'}, optional
            Which family of modes to plot. Can be 'symmetric', 
            'antisymmetric' or 'both'. Defaults to 'both'.
        cutoff_frequencies : bool, optional
            Add cutoff frequencies to the plot. Defaults to True.
        save_img : bool, optional
            Save the result image as png. Defaults to False.            
        sym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the symmetric 
            curves (to change color, linewidth, linestyle, etc.).
        antisym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the 
            antisymmetric curves (to change color, linewidth, linestyle, 
            etc.).
            
        Returns
        -------
        fig, ax : matplotlib objects
            The figure and the axes of the generated plot.
            
        """
              
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.canvas.set_window_title('Group Velocity')
        
        # Calculate the maximum value to scale the ylim of the axes.
        
        max_sym, max_antisym = find_max(self.vg_sym), find_max(self.vg_antisym)
    
        if modes == 'symmetric':
            self.plot(ax, self.vg_sym, max_sym, cutoff_frequencies, 
                      'up', plt_kwargs=sym_style)
        elif modes == 'antisymmetric':
            self.plot(ax, self.vg_antisym, max_antisym, cutoff_frequencies, 
                      'up', plt_kwargs=antisym_style)
        elif modes == 'both':
            max_ = max(max_sym, max_antisym)
            self.plot(ax, self.vg_sym, max_, cutoff_frequencies, 
                      'up', plt_kwargs=sym_style)
            self.plot(ax, self.vg_antisym, max_, cutoff_frequencies, 
                      'up', plt_kwargs=antisym_style)
        else:
            raise Exception('modes must be "symmetric", "antisymmetric"'
                            'or "both".')  
             
        ax.legend(loc='lower right')
        ax.set_ylabel('Group Velocity [m/s]')
        
        if save_img:
            fig.savefig(f'results/Group Velocity - {self.d*1e3} mm '
                        f'{self.material} plate.png', 
                        bbox_inches='tight')    
            
        return fig, ax
    
    def plot_wave_number(self, modes='both', save_img=False,
                         sym_style={'color': 'blue'}, 
                         antisym_style={'color': 'red', 'linestyle' : '--'}):
        """Generate a plot of wavenumber as a function of frequency × 
        thickness.
        
        Parameters
        ----------
        modes : {'both', 'symmetric', 'antisymmetric'}, optional
            Which family of modes to plot. Can be 'symmetric', 
            'antisymmetric' or 'both'. Defaults to 'both'.
        save_img : bool, optional
            Save the result image as png. Defaults to False.                  
        sym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the symmetric 
            curves (to change color, linewidth, linestyle, etc.).
        antisym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the 
            antisymmetric curves (to change color, linewidth, linestyle, 
            etc.).
            
        Returns
        -------
        fig, ax : matplotlib objects
            The figure and the axes of the generated plot.
            
        """
            
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.canvas.set_window_title('Wave Number')
        
        # Calculate the maximum value to scale the ylim of the axes.
        
        max_sym, max_antisym = find_max(self.k_sym), find_max(self.k_antisym)

        if modes == 'symmetric':
            self.plot(ax, self.k_sym, max_sym, plt_kwargs=sym_style)
        elif modes == 'antisymmetric':
            self.plot(ax, self.k_antisym, max_antisym, plt_kwargs=antisym_style)
        elif modes == 'both':
            max_ = max(max_sym, max_antisym)
            self.plot(ax, self.k_sym, max_, plt_kwargs=sym_style)
            self.plot(ax, self.k_antisym, max_, plt_kwargs=antisym_style)
        else:
            raise Exception('modes must be "symmetric", "antisymmetric"'
                            'or "both".') 
            
        ax.legend(loc='upper left')
        ax.set_ylabel('Wave Number [1/m]')
        
        if save_img:
            fig.savefig(f'results/Wave Number - {self.d*1e3} mm '
                        f'{self.material} plate.png',
                        bbox_inches='tight')
            
        return fig, ax
    
    def save_results(self):
        """Save all results to a txt file."""
        
        if self.material:
            filename = f'{self.material} plate - {self.d*1e3} mm.txt'
        else:
            filename = f'{self.d*1e3} mm plate.txt'
            
        header = (f'Material: {self.material}\n'
                  f'Thickness: {str(self.d*1e3)} mm\n'
                  f'Longitudinal wave velocity: {str(self.c_L)} m/s\n'
                  f'Shear wave velocity: {str(self.c_S)} m/s\n\n')
                
        write_txt(self.vp_sym, self.vp_antisym, 'Phase Velocity', 
                  filename, header)
        write_txt(self.vg_sym, self.vg_antisym, 'Group Velocity', 
                  filename, header)
        write_txt(self.k_sym, self.k_antisym, 'Wavenumber', 
                  filename, header)

if __name__ == "__main__":
    E = 68.9e9  # E = Young's modulus, in Pa.
    p = 2700  # p = Density (rho), in kg/m3.
    v = 0.33  # v = Poisson's ratio (nu).

    c_L = np.sqrt(E * (1 - v) / (p * (1 + v) * (1 - 2 * v)))
    c_S = np.sqrt(E / (2 * p * (1 + v)))
    c_R = c_S * ((0.862 + 1.14 * v) / (1 + v))

    # Example: A 10 mm aluminum plate.

    alum = Lamb(thickness=10,
                nmodes_sym=5,
                nmodes_antisym=5,
                fd_max=10000,
                vp_max=15000,
                c_L=c_L,
                c_S=c_S,
                c_R=c_R,
                material='Aluminum')

    # Plot phase velocity, group velocity and wavenumber.

    alum.plot_phase_velocity()
    alum.plot_group_velocity()
    alum.plot_wave_number()

    # Plot wave structure (displacement profiles across thickness) for A0
    # and S0 modes at different fd values.

    alum.plot_wave_structure(mode='A0', nrows=3, ncols=2,
                             fd=[500, 1000, 1500, 2000, 2500, 3000])

    alum.plot_wave_structure(mode='S0', nrows=4, ncols=2,
                             fd=[500, 1000, 1500, 2000, 2500, 3000, 3500, 4000])

    # Generate animations for A0 and S0 modes at 1000 kHz mm.

    alum.animate_displacement(mode='S0', fd=1000)
    alum.animate_displacement(mode='A0', fd=1000)

    # Save all results to a txt file.

    alum.save_results()

    plt.show()