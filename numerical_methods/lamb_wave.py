"""
=========================================================================
Tool for dispersion calculation

Created by Bartlomiej Jargut
https://github.com/dee7ine

Lamb wave class implemented by Francisco Rotea
https://github.com/franciscorotea
-------------------------------------------------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

=========================================================================
"""


import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from typing import Any, Callable
from functools import cache

from numerical_methods.Plot_utilities import add_plot, add_cutoff_freqs, add_velocities
from numerical_methods.Utilities import interpolate, correct_instability, write_txt, find_max
from materials.Materials import IsotropicMaterial
from Exceptions import IncorrectMode


class Lamb:

    def __init__(self, thickness: float, nmodes_sym: int, nmodes_antisym: int, fd_max: float, vp_max: float,
                 c_l: float, c_s: float, c_r: float = None, fd_points: int = 100, vp_step: int = 100,
                 material: str = '') -> None:
        """"
        Parameters
        ----------
        :param thickness:               thickness of the plate, in mm.
        :param nmodes_sym:              number of symmetric modes to calculate.
        :param nmodes_antisym:          number of antisymmetric modes to calculate.
        :param fd_max:                  maximum value of frequency × thickness to calculate.
        :param vp_max:                  maximum value of phase velocity to calculate, in m/s.
        :param c_l:                     Longitudinal wave velocity of the material, in m/s.
        :param c_s:                     shear wave velocity of the material, in m/s.
        :param c_r:                     rayleigh wave velocity of the material, in m/s.
        :param fd_points:               number of frequency × thickness points.
        :param vp_step:                 increment between phase velocity intervals.
        :param material:                name of the material being analyzed.

        :return:
        """
        self.d = thickness / 1e3
        self.h = (thickness / 2) / 1e3
        self.nmodes_sym = nmodes_sym
        self.nmodes_antisym = nmodes_antisym
        self.fd_max = fd_max
        self.vp_max = vp_max
        self.c_L = c_l  # *(10e-3/10e-6)
        self.c_S = c_s  # *(10e-3/10e-6)
        self.c_R = c_r
        self.fd_points = fd_points
        self.vp_step = vp_step
        self.material = material

        # print(f"c_L = {self.c_L}, c_S = {self.c_S}, c_r = {self.c_R}")

        # Solve the dispersion equations.

        sym = self._solve_disp_eqn(function=self._symmetric,
                                   nmodes=nmodes_sym,
                                   c=c_s,
                                   label='S')

        antisym = self._solve_disp_eqn(function=self._antisymmetric,
                                       nmodes=nmodes_antisym,
                                       c=c_l,
                                       label='A')

        # Calculate group velocity (vg) and wavenumber (k) from phase
        # velocity (vp) and interpolate all results.

        self.vp_sym, self.vg_sym, self.k_sym = interpolate(sym, self.d)

        # print(self.vp_sym)
        # print(self.vg_sym)
        # print(self.k_sym)

        self.vp_antisym, self.vg_antisym, self.k_antisym = interpolate(antisym,
                                                                       self.d)

    @cache
    def _calc_constants(self, vp: float, fd: float) -> tuple[float | Any, Any, Any]:
        """Calculate the constants p and q (defined to simplify the
        dispersion equations) and wavenumber from a pair of phase
        velocity and frequency × thickness product.

        Parameters
        ----------
        :param: vp : float or int
            Phase velocity.
        :param: fd : float or int
            Frequency × thickness product.

        :return: k : float
            Wavenumber.
            p, q : float
            A pair of constants introduced to simplify the dispersion
            relations.
        """
        omega = 2 * np.pi * (fd / self.d)

        k = omega / vp

        p = np.sqrt((omega / self.c_L) ** 2 - k ** 2, dtype=np.complex128)
        q = np.sqrt((omega / self.c_S) ** 2 - k ** 2, dtype=np.complex128)

        return k, p, q

    def _symmetric(self, vp: float, fd: float) -> float:
        """Rayleigh-Lamb frequency relation for symmetric modes, used to
        determine the velocity at which a wave of a particular frequency
        will propagate within the plate. The roots of this equation are
        used to generate the dispersion curves.

        :param vp : float or int
            Phase velocity.
        :param fd : float or int
            Frequency × thickness product.

        :return symmetric : float
            Dispersion relation for symmetric modes.
        """
        k, p, q = self._calc_constants(vp, fd)

        symmetric = (np.tan(q * self.h) / q
                     + (4 * (k ** 2) * p * np.tan(p * self.h)) / (q ** 2 - k ** 2) ** 2)

        return np.real(symmetric)

    def _antisymmetric(self, vp: float, fd: float) -> float:
        """Rayleigh-Lamb frequency relation for antisymmetric modes,
        used to determine the velocity at which a wave of a particular
        frequency will propagate within the plate. The roots of this
        equation are used to generate the dispersion curves.

        :param vp : float or int
            Phase velocity.
        :param fd : float or int
            Frequency × thickness product.

        :return antisymmetric : float
            Dispersion relation for antisymmetric modes.
        """
        k, p, q = self._calc_constants(vp, fd)

        antisymmetric = (q * np.tan(q * self.h)
                         + (((q ** 2 - k ** 2) ** 2) * np.tan(p * self.h)) / (4 * (k ** 2) * p))

        return np.real(antisymmetric)

    def _solve_disp_eqn(self, function: Callable[[float, float], float], nmodes: int, c: float, label: str) -> dict:
        """
        Numerical solution of dispersion equation

        :param function:
        :param nmodes:
        :param c:
        :param label:

        :return:
        """
        fd_arr = np.linspace(0, self.fd_max, self.fd_points)
        result = np.zeros((len(fd_arr), nmodes + 1))

        print(f'\nCalculating {function.__name__[1:]} modes..\n')

        for i, fd in enumerate(fd_arr):

            # print(f'{i}/{self.fd_points} - {np.around(fd, 1)} kHz × mm')

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

                            if np.abs(function(bisection, fd)) < 1e-2 and not np.isclose(bisection, c):

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

        # print(result_dict)
        return result_dict

    def plot(self, ax: plt.axes, result: dict, y_max: float, cutoff_frequencies: bool = True,
             arrow_dir: str = 'down', material_velocities: bool = True, plt_kwargs: dict = {}) -> None:
        """Generate a dispersion plot for a family of modes (symmetric
        or antisymmetric).
        :param ax : axes
            Matplotlib axes in which the plot will be added.
        :param result : dict
            A dictionary with a result (vp, vg or k) interpolator at
            each mode.
        :param y_max : float or int
            Maximum y value in the plot.
        :param cutoff_frequencies : bool, optional
            Set to True to add cutoff frequencies to the plot.
        :param arrow_dir : {'up', 'down'}, optional
            Set arrows direction of cutoff frequencies. Can be 'up' (for
            group velocity plots) or 'down' (for phase velocity plots).
        :param material_velocities : bool, optional
            Add material velocities (longitudinal, shear and Rayleigh)
            to the plot. Defaults to True.
        :param plt_kwargs : dict, optional
            Matplotlib kwargs (to change color, linewidth, linestyle,
            etc.).

        :return:
        """
        for mode, arr in result.items():

            # Generate a fd array for each mode and add the
            # corresponding mode plot.

            fd = np.arange(np.amin(arr.x), np.amax(arr.x), 0.1)
            add_plot(ax, result, mode, fd, **plt_kwargs)

            if cutoff_frequencies:
                add_cutoff_freqs(ax, mode, arrow_dir, y_max,
                                 c_l=self.c_L, c_s=self.c_S)

        if material_velocities:
            add_velocities(ax, self.c_L, self.c_S, self.c_R, self.fd_max)

        ax.set_xlim([0, self.fd_max])
        ax.set_ylim([0, y_max])

        ax.set_xlabel('Frequency × thickness [KHz × mm]')

    def plot_phase_velocity(self, modes: str = 'both', cutoff_frequencies: bool = True,
                            material_velocities: bool = True, save_img: bool = False,
                            sym_style: dict = {'color': 'blue'},
                            antisym_style: dict = {'color': 'red', 'linestyle': '--'}) -> tuple[plt.Figure, plt.Axes]:
        """Generate a plot of phase velocity as a function of frequency
        × thickness.

        :param modes : {'both', 'symmetric', 'antisymmetric'}, optional
            Which family of modes to plot. Can be 'symmetric',
            'antisymmetric' or 'both'. Defaults to 'both'.
        :param cutoff_frequencies : bool, optional
            Add cutoff frequencies to the plot. Defaults to True.
        :param material_velocities : bool, optional
            Add material velocities (longitudinal, shear and Rayleigh)
            to the plot. Defaults to True.
        :param save_img : bool, optional
            Save the result image as png. Defaults to False.
        :param sym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the symmetric
            curves (to change color, linewidth, linestyle, etc.).
        :param antisym_style : dict, optional
            A dictionary with matplotlib kwargs to modify the
            antisymmetric curves (to change color, linewidth, linestyle,
            etc.).

        :return fig, ax : matplotlib objects
            The figure and the axes of the generated plot.
        """
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.canvas.setWindowTitle(f'Phase Velocity for {self.d * 10**3} mm thick {self.material}')

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
            raise IncorrectMode('modes must be "symmetric", "antisymmetric"'
                            'or "both".')

        ax.legend(loc='lower right')
        ax.set_title(f'Phase Velocity for {self.d * 10**3} mm thick {self.material}')
        ax.set_ylabel('Phase Velocity [m/s] ')

        if save_img:
            fig.savefig(f'results/Phase Velocity - {self.d * 1e3} mm '
                        f'{self.material} plate.png',
                        bbox_inches='tight')

        return fig, ax

    def plot_group_velocity(self, modes: str = 'both', cutoff_frequencies: bool = True,
                            save_img: bool = False, sym_style: dict = {'color': 'blue'},
                            antisym_style: dict = {'color': 'red', 'linestyle': '--'}) -> tuple[plt.figure, plt.axes]:
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
        fig.canvas.setWindowTitle(f'Group Velocity for {self.d * 10**3} mm thick {self.material}')

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
            raise IncorrectMode('modes must be "symmetric", "antisymmetric"'
                            'or "both".')

        ax.legend(loc='lower right')
        ax.set_title(f'Group Velocity for {self.d * 10**3} mm thick {self.material}')
        ax.set_ylabel('Group Velocity [m/s]')

        if save_img:
            fig.savefig(f'results/Group Velocity - {self.d * 1e3} mm '
                        f'{self.material} plate.png',
                        bbox_inches='tight')

        return fig, ax

    def plot_wave_number(self, modes='both', save_img: bool = False,
                         sym_style: dict = {'color': 'blue'},
                         antisym_style: dict = {'color': 'red', 'linestyle': '--'},
                         size: tuple = (7, 4)) -> tuple[plt.figure, plt.axes]:

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
        size: list

        Returns
        -------
        fig, ax : matplotlib objects
            The figure and the axes of the generated plot.

        """

        fig, ax = plt.subplots(figsize=size)
        fig.canvas.setWindowTitle(f'Wave Number for {self.d * 10**3} mm thick {self.material}')

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
        ax.set_title(f'Wave Number for {self.d * 10 ** 3} mm thick {self.material}')
        ax.set_ylabel('Wave Number [1/m]')

        if save_img:
            fig.savefig(f'results/Wave Number - {self.d * 1e3} mm '
                        f'{self.material} plate.png',
                        bbox_inches='tight')

        return fig, ax

    def save_results(self) -> None:
        """Save all results to a txt file."""

        if self.material:
            filename = f'{self.material} plate - {self.d * 1e3} mm.txt'
        else:
            filename = f'{self.d * 1e3} mm plate.txt'

        header = (f'Material: {self.material}\n'
                  f'Thickness: {str(self.d * 1e3)} mm\n'
                  f'Longitudinal wave velocity: {str(self.c_L)} m/s\n'
                  f'Shear wave velocity: {str(self.c_S)} m/s\n\n')

        write_txt(self.vp_sym, self.vp_antisym, 'Phase Velocity',
                  filename, header)
        write_txt(self.vg_sym, self.vg_antisym, 'Group Velocity',
                  filename, header)
        write_txt(self.k_sym, self.k_antisym, 'Wavenumber',
                  filename, header)


def main() -> None:

    # You can obtain the values of c_L and c_S and an approximate value for
    # c_R (if v > 0.3) from the material's mechanical properties by using
    # the following equations:

    new_material = IsotropicMaterial(material="Ice")
    E = new_material.e  # E = Young's modulus, in Pa.
    p = new_material.density  # p = Density (rho), in kg/m3.
    v = new_material.v  # v = Poisson's ratio (nu).

    c_L = np.sqrt(E * (1 - v) / (p * (1 + v) * (1 - 2 * v)))
    c_S = np.sqrt(E / (2 * p * (1 + v)))
    c_R = c_S * ((0.862 + 1.14 * v) / (1 + v))

    # Example: A 10 mm aluminum plate.

    alum = Lamb(thickness=10,
                nmodes_sym=5,
                nmodes_antisym=5,
                fd_max=10000,
                vp_max=15000,
                c_l=c_L,
                c_s=c_S,
                c_r=c_R,
                material='Ice')

    # Plot phase velocity, group velocity and wavenumber.

    alum.plot_phase_velocity()
    alum.plot_group_velocity()
    alum.plot_wave_number()

    # Plot wave structure (displacement profiles across thickness) for A0
    # and S0 modes at different fd values.

    # alum.plot_wave_structure(mode='A0', nrows=3, ncols=2,
    # fd=[500,1000,1500,2000,2500,3000])

    # alum.plot_wave_structure(mode='S0', nrows=4, ncols=2,
    # fd=[500,1000,1500,2000,2500,3000,3500,4000])

    # Generate animations for A0 and S0 modes at 1000 kHz mm.

    # alum.animate_displacement(mode='S0', fd=1000)
    # alum.animate_displacement(mode='A0', fd=1000)

    # Save all results to a txt file.

    # alum.save_results()

    plt.show()


if __name__ == "__main__":
    main()
