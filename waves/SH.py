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
from dataclasses import dataclass

from materials.Materials import IsotropicMaterial


PROJECT_NAME = 'dispersioncalc_alpha'
CURRENT_DIR = Path(__file__)
SOURCE_ROOT = [p for p in CURRENT_DIR.parents if p.parts[-1] == PROJECT_NAME][0]


@dataclass(eq=False, frozen=False, slots=True)
class SH:

    d: float
    h: float

    f_max: float
    f_step: float
    c_L: float
    c_S: float
    c_R: float

    number_of_modes: int
    material: str

    sym: dict
    antisym: dict

    vp_sym: dict
    vg_sym: dict
    k_sym: dict

    vp_antisym: dict
    vg_antisym: dict
    k_antisym: dict

    def __init__(self, thickness: float, number_of_modes: int, f_max: float, f_step: float,
                 c_l: float, c_s: float, c_r: float = None, material: str = '') -> None:
        """"
        :param thickness:               thickness of the plate, in mm.
        :param number_of_modes:         number of modes to calculate.
        :param f_max:                   maximum value of frequency × thickness to calculate.
        :param f_step                   frequency step
        :param c_l:                     longitudinal wave velocity of the material, in m/s.
        :param c_s:                     shear wave velocity of the material, in m/s.
        :param c_r:                     rayleigh wave velocity of the material, in m/s.
        :param material:                name of the material being analyzed.

        :return:
        """
        self.d = thickness / 1e3
        self.h = (thickness / 2) / 1e3
        self.number_of_modes = number_of_modes
        self.f_max = f_max
        self.f_step = f_step * 1e3
        self.c_L = c_l  # *(10e-3/10e-6)
        self.c_S = c_s  # *(10e-3/10e-6)
        self.c_R = c_r
        self.material = material

        # print(f"c_L = {self.c_L}, c_S = {self.c_S}, c_r = {self.c_R}")

    def plot_phase_velocity(self, save_result=True) -> None:
        """
        Calculates SH wave number from equation

        :return:
        """
        with np.printoptions(threshold=np.inf):

            omega = np.arange(0.1, self.f_max*2*np.pi, self.f_step*2*np.pi)  # generating omega vector
            result_arr = np.zeros([len(omega), 2 * self.number_of_modes])
            columns = []

            ct = self.c_S
            d = self.d

            fig, ax = plt.subplots(figsize=(7, 4))
            # plt.tight_layout()
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Phase Velocity [m/s]')
            plt.autoscale(True, 'both')
            plt.title(f'Phase velocity for {self.d*1e3}mm thick {self.material} ')

            filename: str = f'SH_Phase_velocity_{self.material}_{self.d * 1e3}mm'
            filepath: str = f'{SOURCE_ROOT}//results'

            for mode, mode_index in zip(range(0, self.number_of_modes), range(0, 2 * self.number_of_modes, 2)):
                
                # kh = np.real(np.emath.sqrt(np.square(omega*d/ct) - np.square(mode*np.pi)))
                kh = np.emath.sqrt(np.square(omega * d / ct) - np.square(mode * np.pi))
                k = np.real(kh/d)

                k[k == 0] = np.nan  # filter 0 values

                vp = omega/k
                vp[vp == 0] = np.nan
                freq_arr = omega / (2 * np.pi)

                ax.plot(omega/(2*np.pi), vp, label=f'SH{mode}')
                result_arr[:, mode_index] = freq_arr
                result_arr[:, mode_index + 1] = vp
                columns.append(f'SH{mode} f [Hz]')
                columns.append(f'SH{mode} vp [m/s]')

            if save_result:
                main_df = pd.DataFrame(result_arr, columns=columns)
                main_df.to_excel(f'{filepath}//{filename}.xlsx')

            ax.legend()

    def plot_wave_number(self, save_result=True) -> None:
        """
        Calculates SH wave number from equation

        :return:
        """
        with np.printoptions(threshold=np.inf):
            omega = np.arange(0.1, self.f_max*2*np.pi, self.f_step*2*np.pi)  # generating omega vector
            result_arr = np.zeros([len(omega), 2*self.number_of_modes])
            columns = []

            ct = self.c_S
            d = self.d

            fig, ax = plt.subplots(figsize=(7, 4))
            # plt.tight_layout()
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Wave number [1/m]')
            plt.autoscale(True, 'both')

            plt.title(f'Wave Number for {self.d * 1e3}mm thick {self.material} ')

            #main_df = pd.DataFrame()
            filename: str = f'SH_Wave_number_{self.material}_{self.d * 1e3}mm'
            filepath: str = f'{SOURCE_ROOT}//results'

            for mode, mode_index in zip(range(0, self.number_of_modes), range(0, 2*self.number_of_modes, 2)):

                kh = np.real(np.emath.sqrt(np.square(omega * d / ct) - np.square(mode * np.pi)))
                k = kh / d
                #kh = np.real(kh)
                k[k == 0] = np.nan

                freq_arr = omega / (2 * np.pi)
                ax.plot(omega/(2*np.pi), k, label=f'M{mode}')
                #ax.set_ylim([0, k[-1]])
                result_arr[:,mode_index] = freq_arr
                result_arr[:,mode_index+1] = k
                columns.append(f'SH{mode} f [Hz]')
                columns.append(f'SH{mode} k [1/m]')

            if save_result:
                main_df = pd.DataFrame(result_arr, columns=columns)
                #ax.text(4, 1000, f'M{mode}')
                main_df.to_excel(f'{filepath}//{filename}.xlsx')

            ax.legend()

    def plot_group_velocity(self, save_result=True) -> None:
        """
        Calculates SH wave number from equation

        :return:
        """
        with np.printoptions(threshold=np.inf):
            omega = np.arange(0.1, self.f_max*2*np.pi, self.f_step)  # generating omega vector
            result_arr = np.zeros([len(omega), 2 * self.number_of_modes])
            columns = []

            ct = self.c_S
            d = self.d

            fig, ax = plt.subplots(figsize=(7, 4))
            # plt.tight_layout()
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('Group Velocity [m/s]')
            plt.autoscale(True, 'both')
            plt.title(f'Group velocity for {self.d * 1e3}mm thick {self.material} ')

            filename: str = f'SH_Group_velocity_{self.material}_{self.d * 1e3}mm'
            filepath: str = f'{SOURCE_ROOT}//results'

            for mode, mode_index in zip(range(0, self.number_of_modes), range(0, 2 * self.number_of_modes, 2)):
                # kh = np.real(np.emath.sqrt(np.square(omega*d/ct) - np.square(mode*np.pi)))
                kh = np.emath.sqrt(np.square(omega * d / ct) - np.square(mode * np.pi))
                k = np.real(kh / d)

                k[k == 0] = np.nan  # filter 0 values

                vp = omega / k
                vp[vp == 0] = np.nan

                vg = np.diff(omega)/np.diff(k)

                freq_arr = omega/(2*np.pi)

                ax.plot(omega[:-1]/(2*np.pi), vg, label=f'SH{mode}')

                #result_arr[:, mode_index] = freq_arr
                #result_arr[:, mode_index + 1] = vg
                columns.append(f'SH{mode} f [Hz]')
                columns.append(f'SH{mode} vg [1/m]')

            """
            if save_result:
                main_df = pd.DataFrame(result_arr, columns=columns)
                main_df.to_excel(f'{filepath}//{filename}.xlsx')
            """

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

    new_material = IsotropicMaterial(material="AluminumDisperse")
    # new_material.fix_file_path('C://Users//deefi//PycharmProjects//dispersioncalc_alpha//materials//material_data.txt')
    new_material.fix_file_path('//materials//material_data.txt')
    E = new_material.e  # E = Young's modulus, in Pa.
    p = new_material.density  # p = Density (rho), in kg/m3.
    v = new_material.v  # v = Poisson's ratio (nu).

    c_L = np.sqrt(E * (1 - v) / (p * (1 + v) * (1 - 2 * v)))
    c_S = np.sqrt(E / (2 * p * (1 + v)))
    c_R = c_S * ((0.862 + 1.14 * v) / (1 + v))

    # Example: A 1 mm aluminum plate.

    sh = SH(thickness=1,
            number_of_modes=5,
            f_max=5e6,                 # 2*np.pi*5e6
            f_step=1,
            c_l=c_L,
            c_s=c_S,
            c_r=c_R,
            material=new_material.name)

    # Plot phase velocity, group velocity and wavenumber.

    sh.plot_wave_number(save_result=True)
    sh.plot_phase_velocity(save_result=False)
    sh.plot_group_velocity()

    plt.show()


if __name__ == "__main__":
    main()
