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

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize
from typing import Callable
from dataclasses import dataclass

from utility_functions.Plot_utilities import add_plot, add_cutoff_freqs, add_velocities
from utility_functions.Utilities import interpolate, correct_instability, find_max
from materials.Materials import IsotropicMaterial
from Exceptions import IncorrectMode


PROJECT_NAME = 'dispersioncalc_alpha'
CURRENT_DIR = Path(__file__)
SOURCE_ROOT = [p for p in CURRENT_DIR.parents if p.parts[-1] == PROJECT_NAME][0]


@dataclass(eq=False, frozen=False, slots=True)
class SH:

    d: float
    h: float

    nmodes_sym: float
    nmodes_antisym: float

    fd_max: float
    vp_max: float
    c_L: float
    c_S: float
    c_R: float

    fd_points: int
    vp_step: int
    material: str

    sym: dict
    antisym: dict

    vp_sym: dict
    vg_sym: dict
    k_sym: dict

    vp_antisym: dict
    vg_antisym: dict
    k_antisym: dict

    def __init__(self, thickness: float, nmodes_sym: int, nmodes_antisym: int, fd_max: float, vp_max: float,
                 c_l: float, c_s: float, c_r: float = None, fd_points: int = 100, vp_step: int = 100,
                 material: str = '') -> None:
        """"
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

    def _equation(self, number_of_modes: int) -> float:
        """Rayleigh-Lamb frequency relation for symmetric modes, used to
        determine the velocity at which a wave of a particular frequency
        will propagate within the plate. The roots of this equation are
        used to generate the dispersion curves.

        :param vp : float
            Phase velocity.
        :param fd : float
            Frequency × thickness product.
        :param number_of_modes: int

        :return symmetric : float
            Dispersion relation for symmetric modes.
        """

        # fd_max as a limit to calculation
        with np.printoptions(threshold=np.inf):

            fd_arr = np.linspace(0, self.fd_max, self.fd_points)
            result_arr = np.zeros((len(fd_arr), number_of_modes + 1))

            print(f'\nCalculating SH modes..\n')

            vp = 0

            """
            Constants:
            pi
            ct
            k
            cS - shear wave velocity
            
            variable fd (frequencyxthickness)
            (Mπ)2 = (fd/cS)^2 − (omega*d/vp)^2
            
            vp = 1/(np.sqrt((fd/cs)**2 - (M*np.pi)**2)*omega*d
            
            """

            # x results wh
            # y results k

            for i, fd in enumerate(fd_arr):

                omega = 2 * np.pi * (fd / self.d)
                k = omega / vp

                result_arr[i][0] = fd
                result_arr[i][1] = vp

                vp += self.vp_step

            print('fd arr')
            print(fd_arr)


            print('result arr')
            print(result_arr)

            for n_mode in range(number_of_modes):
                mode_result = np.vstack((result_arr[:, 0], result_arr[:, n_mode+1]))
                mode_result = mode_result[:, ~np.isnan(mode_result).any(axis=0)]

            print('mode result')
            print(mode_result)



        """
        LAMB IMPLEMENTATION DON"T DELETE
        """

        """
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
        """

    def result_to_excel(self, result: list, result_type: str, mode: str) -> pd.DataFrame:

        main_df = pd.DataFrame()

        filename = f'{result_type.capitalize()}_{self.material}_{self.d*1e3}mm_{mode}'

        for index, _ in enumerate(result):

            temp_df_x = pd.DataFrame(result[index][0], columns=['x'])
            temp_df_y = pd.DataFrame(result[index][1], columns=['y'])
            temp_df = pd.concat([temp_df_x, temp_df_y], axis=1)

            main_df = pd.concat([main_df, temp_df], axis=1)
            # print(pd.DataFrame(values_list[index][0]))
            # x_list.append(pd.DataFrame(values_list[index][0], columns=['x']))
            # y_list.append(pd.DataFrame(values_list[index][1], columns=['y']))

        main_df.to_excel(f'{filename}.xlsx')

        return main_df


def main() -> None:

    # You can obtain the values of c_L and c_S and an approximate value for
    # c_R (if v > 0.3) from the material's mechanical properties by using
    # the following equations:

    new_material = IsotropicMaterial(material="Ice")
    # new_material.fix_file_path('C://Users//deefi//PycharmProjects//dispersioncalc_alpha//materials//material_data.txt')
    new_material.fix_file_path('//materials//material_data.txt')
    E = new_material.e  # E = Young's modulus, in Pa.
    p = new_material.density  # p = Density (rho), in kg/m3.
    v = new_material.v  # v = Poisson's ratio (nu).

    c_L = np.sqrt(E * (1 - v) / (p * (1 + v) * (1 - 2 * v)))
    c_S = np.sqrt(E / (2 * p * (1 + v)))
    c_R = c_S * ((0.862 + 1.14 * v) / (1 + v))

    # Example: A 10 mm aluminum plate.

    sh = SH(thickness=10,
                nmodes_sym=5,
                nmodes_antisym=5,
                fd_max=10000,
                vp_max=15000,
                c_l=c_L,
                c_s=c_S,
                c_r=c_R,
                material='Ice')

    # Plot phase velocity, group velocity and wavenumber.

    #sh.plot_phase_velocity()
    #sh.plot_group_velocity()
    #sh.plot_wave_number()

    sh._equation(number_of_modes=10)



if __name__ == "__main__":
    main()
