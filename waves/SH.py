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
import scipy.interpolate
from dataclasses import dataclass

from materials.Materials import IsotropicMaterial


PROJECT_NAME = 'dispersioncalc_alpha'
CURRENT_DIR = Path(__file__)
SOURCE_ROOT = [p for p in CURRENT_DIR.parents if p.parts[-1] == PROJECT_NAME][0]


@dataclass(eq=False, frozen=False, slots=True)
class SH:

    d: float
    h: float

    fd_max: float
    vp_max: float
    c_L: float
    c_S: float
    c_R: float

    number_of_modes: int
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

    def __init__(self, thickness: float, number_of_modes: int, fd_max: float, vp_max: float,
                 c_l: float, c_s: float, c_r: float = None, fd_points: int = 100, vp_step: int = 100,
                 material: str = '') -> None:
        """"
        :param thickness:               thickness of the plate, in mm.
        :param number_of_modes:         number of modes to calculate.
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
        self.number_of_modes = number_of_modes
        self.fd_max = fd_max
        self.vp_max = vp_max
        self.c_L = c_l  # *(10e-3/10e-6)
        self.c_S = c_s  # *(10e-3/10e-6)
        self.c_R = c_r
        self.fd_points = fd_points
        self.vp_step = vp_step
        self.material = material

        # print(f"c_L = {self.c_L}, c_S = {self.c_S}, c_r = {self.c_R}")

    def __equation(self) -> None:
        """Rayleigh-Lamb frequency relation for symmetric modes, used to
        determine the velocity at which a wave of a particular frequency
        will propagate within the plate. The roots of this equation are
        used to generate the dispersion curves.

        :return symmetric : float
            Dispersion relation for symmetric modes.
        """

        # fd_max as a limit to calculation

        with np.printoptions(threshold=np.inf):

            """
            converting units
            """
            d = self.d  # * 10e3       # m to mm
            c_s = self.c_S  # / 10e3   # m/s to mm/microsecond

            fd_arr = np.linspace(0, self.fd_max, self.fd_points)
            # vp_arr1 = np.zeros(len(fd_arr))
            # vp_arr2 = np.zeros(len(fd_arr))
            result_arr = np.zeros((len(fd_arr), self.number_of_modes + 1))
            print('shape')
            print(result_arr.shape)

            print(f'\nCalculating SH modes..\n')

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

            """
            for n_mode in range(self.number_of_modes):
            mode_result = np.vstack((result_arr[:, 0], result_arr[:, n_mode+1]))
            mode_result = mode_result[:, ~np.isnan(mode_result).any(axis=0)]
            """

            # result_arr = [vector(mode) for mode in range(0, self.number_of_modes)]

            # print('result')
            # print(result)

            for i, fd in enumerate(fd_arr):
                # k = omega / vp

                for mode in range(1, self.number_of_modes):

                    omega = 2 * np.pi * (fd / self.d)
                    result_arr[i][0] = fd

                    test_check = (fd / c_s) ** 2 - ((mode * np.pi) ** 2)
                    print(f'input checking {test_check}')
                    # result_arr[i][mode] = np.sqrt(np.absolute((fd / self.c_S) ** 2 - ((mode * np.pi) ** 2)))
                    result_arr[i][mode] = (omega * d) / (np.sqrt((fd / c_s) ** 2 - ((mode * np.pi) ** 2)))

            result_arr = np.transpose(result_arr)
            #result_arr[result_arr == 0] = np.nan
            #result_arr = result_arr[:, ~np.isnan(result_arr).any(axis=0)]
            #filter(lambda v: v == v, result_arr)

            print('result_arr')
            print(fd_arr[1])
            print(fd_arr[2])
            print(fd_arr[3])
            print(result_arr)
            print(result_arr.shape)

    def plot_phase_velocity(self) -> None:
        """
        Calculates SH wave number from equation

        :return:
        """
        with np.printoptions(threshold=np.inf):

            omega = np.arange(0.1, 2*np.pi*5e6, 1e3)  # generating omega vector
            # result_arr = np.zeros([self.number_of_modes, len(omega)])

            ct = self.c_S
            d = self.d

            fig, ax = plt.subplots(figsize=(7, 4))
            # plt.tight_layout()
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Phase Velocity [m/s]')
            plt.title(f'Phase velocity for {self.d*1e3}mm thick {self.material} ')

            for mode in range(1, 5):
                
                # kh = np.real(np.emath.sqrt(np.square(omega*d/ct) - np.square(mode*np.pi)))
                kh = np.emath.sqrt(np.square(omega * d / ct) - np.square(mode * np.pi))
                k = np.real(kh/d)

                k[k == 0] = np.nan  # filter 0 values

                vp = omega/k
                vp[vp == 0] = np.nan

                ax.plot(omega, vp, label=f'SH{mode}')

            ax.legend()

    def plot_wave_number(self) -> None:
        """
        Calculates SH wave number from equation

        :return:
        """
        with np.printoptions(threshold=np.inf):
            omega = np.arange(0.1, 2 * np.pi * 5e6, 1e3)  # generating omega vector
            # result_arr = np.zeros([self.number_of_modes, len(omega)])

            ct = self.c_S
            d = self.d

            fig, ax = plt.subplots(figsize=(7, 4))
            # plt.tight_layout()
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Wave number')
            plt.title(f'Wave Number for {self.d * 1e3}mm thick {self.material} ')

            for mode in range(1, 5):
                kh = np.real(np.emath.sqrt(np.square(omega * d / ct) - np.square(mode * np.pi)))
                k = kh / d
                k[k == 0] = np.nan

                ax.plot(omega, k, label=f'SH{mode}')

            ax.legend()

    def plot_group_velocity(self) -> None:
        """
        Calculates SH wave number from equation

        :return:
        """
        with np.printoptions(threshold=np.inf):
            omega = np.arange(0.1, 2 * np.pi * 5e6, 1e3)  # generating omega vector
            # result_arr = np.zeros([self.number_of_modes, len(omega)])

            ct = self.c_S
            d = self.d

            fig, ax = plt.subplots(figsize=(7, 4))
            # plt.tight_layout()
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Group Velocity')
            plt.title(f'Group velocity for {self.d * 1e3}mm thick {self.material} ')

            for mode in range(1, 5):
                # kh = np.real(np.emath.sqrt(np.square(omega*d/ct) - np.square(mode*np.pi)))
                kh = np.emath.sqrt(np.square(omega * d / ct) - np.square(mode * np.pi))
                k = np.real(kh / d)

                k[k == 0] = np.nan  # filter 0 values

                vp = omega / k
                vp[vp == 0] = np.nan

                univ_s = scipy.interpolate.InterpolatedUnivariateSpline(omega, vp)
                vp_prime = univ_s.derivative()

                vg = np.square(vp) * (1 / (vp - vp_prime(omega) * omega))

                ax.plot(omega, vg, label=f'SH{mode}')

            ax.legend()

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

    sh = SH(thickness=1,
            number_of_modes=5,
            fd_max=10000,
            vp_max=10000,
            c_l=c_L,
            c_s=c_S,
            c_r=c_R,
            material=new_material.name)

    # Plot phase velocity, group velocity and wavenumber.

    sh.plot_wave_number()
    sh.plot_phase_velocity()
    sh.plot_group_velocity()

    plt.show()


if __name__ == "__main__":
    main()
