from matplotlib import use
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

import PySimpleGUI as sg; use('qt5agg')

from material_editor.materials import IsotropicMaterial
from numerical_methods.lamb_wave import Lamb

def main():
    data, choices = IsotropicMaterial._parse_materials()
    modes = ['Symmetric', 'Antisymmetric', 'Both']

    """
        Simultaneous PySimpleGUI Window AND a Matplotlib Interactive Window
        A number of people have requested the ability to run a normal PySimpleGUI window that
        launches a MatplotLib window that is interactive with the usual Matplotlib controls.
        It turns out to be a rather simple thing to do.  The secret is to add parameter block=False to plt.show()
    """

    def draw_plot():
        plt.plot([0.1, 0.2, 0.5, 0.7])
        plt.show(block=False)



    console_frame_layout = [[sg.Multiline("", size=(100, 10), autoscroll=True,
                                  reroute_stdout=True, reroute_stderr=True, key='-OUTPUT-')]]

    layout = [[sg.Frame('Lamb waves', layout = [
              [sg.Text('Material'), sg.InputCombo(values = choices,
                             default_value = "AluminumDisperse",
                             key = "material_name",
                             enable_events = True,
                             size=(33, 20)),
                             sg.Stretch()], [sg.Text('Symmetry modes'), sg.InputCombo(values = modes, default_value = 'Symmetric', key = 'mode', enable_events = True, size = (25,20))],
        [sg.Text('Thickness [mm]             '), sg.Input('10', enable_events=True, key='thickness', size = (4,5), justification = 'center')],
        [sg.Text('Frequency [Hz]              '), sg.Input('1000', enable_events=True, key='frequency', size=(4, 5), justification = 'center')],
        [sg.Text('Maximum velocity [m/s]  '), sg.Input('1000', enable_events=True, key='velocity', size=(4, 5), justification='center')],
              [sg.Button('Calculate and plot'), sg.Cancel(), sg.Button('Help')]])],
              [sg.Frame("Output", layout = console_frame_layout)]]



    main_window = sg.Window('Counter Strike Global Offensive', layout, size = (1250, 750))

    while True:
        """
        main loop
        
        ------------------
        """

        event, values = main_window.read()

        if event in (None, 'Cancel'):
            break
        elif event == 'Help':
            sg.popup('Click plot in order to calculate and plot dispersion curves for the chosen material', title = "Help")
        elif event == 'Calculate and plot':

            print(datetime.now())

            new_material = IsotropicMaterial(values['material_name'])
            fd_max = float(values['thickness'])*float(values['frequency'])  #maximum frequency-thickness product


            E = new_material._E  # E = Young's modulus, in Pa.
            p = new_material._density  # p = Density (rho), in kg/m3.
            v = new_material._v  # v = Poisson's ratio (nu).

            c_L = np.sqrt(E * (1 - v) / (p * (1 + v) * (1 - 2 * v)))
            c_S = np.sqrt(E / (2 * p * (1 + v)))
            c_R = c_S * ((0.862 + 1.14 * v) / (1 + v))

            # Example: A 10 mm aluminum plate.

            alum = Lamb(thickness = float(values['thickness']),
                        nmodes_sym=10,
                        nmodes_antisym=10,
                        fd_max=fd_max,
                        vp_max=15000,
                        c_L=c_L,
                        c_S=c_S,
                        c_R=c_R,
                        material=values['material_name'])

            # Plot phase velocity, group velocity and wavenumber.

            print(f"{datetime.now().isoformat(' ', 'seconds')} : Calculating phase velocity for modes: {values['mode'].lower()}")
            alum.plot_phase_velocity(modes = values['mode'].lower())
            print(f"{datetime.now().isoformat(' ', 'seconds')} : Calculating group velocity for modes: {values['mode'].lower()}")
            alum.plot_group_velocity(modes = values['mode'].lower())
            print(f"{datetime.now().isoformat(' ', 'seconds')} : Calculating wave number for modes: {values['mode'].lower()}")
            alum.plot_wave_number(modes = values['mode'].lower())




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

    main_window.close()

if __name__ == "__main__":
    main()