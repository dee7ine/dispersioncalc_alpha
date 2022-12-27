import os
import logging
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg  # use('qt5agg')

from materials.Materials import IsotropicMaterial
from numerical_methods.lamb_wave import Lamb


logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


class UI:

    _menu_layout: list
    _console_frame_layout: list
    _material_frame_layout: list
    _main_frame_layout: list
    _default_data_path: str = f'{os.getcwd()}\\materials\\material_data.txt'
    _modes = ['Symmetric', 'Antisymmetric', 'Both']
    _data: list
    _choices: list

    def __init__(self) -> None:

        sg.theme('SystemDefaultForReal')
        self._data, self._choices = IsotropicMaterial.parse_materials()

        self._menu_layout = self._menu_layout()
        self._console_frame_layout = self._console_frame_layout()
        self._material_frame_layout = self._material_frame_layout()
        self._main_frame_layout = self._main_frame_layout()

        self.main_window = sg.Window(title='Counter Strike: Global Offensive',
                                     layout=self._main_frame_layout,
                                     size=(1250, 650))
        self._app_main_loop()

    def _menu_layout(self) -> list:

        return [['File', ['Open', 'Save']],
                ['Edit', ['Paste', ['Special', 'Normal'], 'Undo']],
                ['Help', 'About...'], ]

    def _console_frame_layout(self) -> list:

        return [[sg.Multiline(f"Beginning session {datetime.now().isoformat(' ', 'seconds')}",
                              size=(100, 10),
                              autoscroll=True,
                              reroute_stdout=True,
                              reroute_stderr=True,
                              key='-OUTPUT-',
                              background_color='white')]]

    def _material_frame_layout(self) -> list:

        return [[sg.Frame('', layout=[[sg.Text("E [MPa]"), sg.Input('68.9', enable_events=True, key='young_modulus', size=(6, 5))],
                [sg.Text(text="v [no unit]"), sg.Input('0.33', enable_events=True, key='poisson_ratio', size=(6, 5))],
                [sg.Text(text="Density [kg/m3]"), sg.Input('2700', enable_events=True, key='density', size=(6, 5))],
                [sg.Text("C11"), sg.Input('0', enable_events=True, key='C11', size=(6, 5))],
                [sg.Text("C66"), sg.Input('0', enable_events=True, key='C66', size=(6, 5))],
                [sg.Text("Material name"), sg.Input('default', enable_events=True, key='new_material_name', size=(6, 5))],
                [sg.Button('Create', key='Create', tooltip='Add material to data file')]], size=(250, 200))],
                [sg.Frame('', layout=[[sg.Text('Material data path'),
                sg.InputText(default_text=self._default_data_path, key='-data_path-', size=(75, 22))],
                [sg.FileBrowse(file_types=(("TXT Files", "*.txt"), ("ALL Files", "*.*")), enable_events=True,
                target='-data_path-', tooltip="Choose file containing material data"),
                sg.Button('Load', tooltip="Load data file"), sg.Button('Help', key='Material_Help', tooltip='Helpful tips')]], size=(500,60))]]

    def _main_frame_layout(self) -> list:

        return [[sg.Menu(self._menu_layout, tearoff=False)],
                [sg.Frame('Lamb waves', layout=[[sg.Frame('Parameters', layout=[[sg.Text('Material'),
                sg.InputCombo(values=self._choices, default_value="AluminumDisperse", key="material_name", enable_events=True, readonly=True,
                background_color='white', size=(33, 20)), sg.Stretch()], [sg.Text('Symmetry modes'),
                sg.InputCombo(values=self._modes, default_value='Symmetric', key='mode', enable_events=True, readonly=True, background_color='white', size=(25, 20))],
                [sg.Text('Thickness [mm]             '),
                sg.Input('10', enable_events=True, key='thickness', size=(6, 5), justification='left')],
                [sg.Text('Frequency [Hz]              '),
                sg.Input('1000', enable_events=True, key='frequency', size=(6, 5), justification='left')],
                [sg.Text('Maximum velocity [m/s]  '),
                sg.Input('15000', enable_events=True, key='velocity', size=(6, 5), justification='left')],
                [sg.Frame('', layout=[[sg.Text('Number of modes')], [sg.Text('Symmetric     '), sg.Input('10', enable_events=True, key='symmetric', size=(5, 5))],
                [sg.Text('Antisymmetric'), sg.Input('10', enable_events=True, key='antisymmetric', size=(5, 5))],
                [sg.Text('Trace SH modes'), sg.Checkbox('', size=(5, 5))]])]])],
                [sg.Button('Calculate and plot', tooltip="Calculate and plot dispersion curves \n for given material data"),
                sg.Button('Close', tooltip='Close all already open plots'),
                sg.Cancel(), sg.Button('Help', key="Lamb_Help", tooltip="Helpful tips")]]),
                sg.Frame('Material editor', layout=self._material_frame_layout, tooltip="Material editing module"), sg.Frame('Plot', layout=[[sg.Canvas(size=(300, 300), key='-canvas-')]])],
                [sg.Frame("Output", layout=self._console_frame_layout)]]

    def _draw_figure(self, canvas, figure):

        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    def _model(self):

        axes = [2, 2, 5]

        data = np.ones(axes, dtype=np.bool_)

        alpha = 0.9

        colors = np.empty(axes + [4], dtype=np.float32)
        colors[:] = [1, 1, 1, alpha]

        fig = plt.figure(figsize=(3, 3))
        ax = fig.add_subplot(111, projection='3d')

        ax.voxels(data, facecolors=colors)
        return fig, ax

    def _app_main_loop(self) -> None:

        try:

            while True:

                event, values = self.main_window.read()

                if event in (None, 'Cancel'):

                    break

                elif event == 'Lamb_Help':

                    sg.popup('Click plot in order to calculate and plot dispersion curves for the chosen material',
                             title="Help")

                elif event == 'Material_Help':

                    sg.popup('Create a custom material.\nUse browse button to find material data file',
                             title="Help")

                elif event == 'Load':

                    # IsotropicMaterial.fix_file_path(values['-data_path-'])
                    # data, choices = IsotropicMaterial._parse_materials()
                    print(f"{datetime.now().isoformat(' ', 'seconds')} : Loading material data...")
                    IsotropicMaterial.fix_file_path(filepath=values['-data_path-'])

                    data, choices = IsotropicMaterial.parse_materials()
                    self.main_window.find_element('material_name').Update(values=choices)
                    logger.info('Calculating phase velocity')
                    self._draw_figure(self.main_window['-canvas-'].TKCanvas, self._model()[0])
                    print(f"{datetime.now().isoformat(' ', 'seconds')}: Data file updated")

                elif event == 'Calculate and plot':

                    print(datetime.now())

                    new_material = IsotropicMaterial(values['material_name'])
                    fd_max: float = float(values['thickness']) * float(
                        values['frequency'])  # maximum frequency-thickness product

                    """
                    Engineering constants and material object instance
    
                    -------------------------------------------------------
                    E = Young's modulus, in Pa.
                    p = Density (rho), in kg/m3.
                    v = Poisson's ratio (nu).
    
                    """

                    E: float = new_material._E
                    p: float = new_material._density
                    v: float = new_material._v

                    c_L = np.sqrt(E * (1 - v) / (p * (1 + v) * (1 - 2 * v)))
                    c_S = np.sqrt(E / (2 * p * (1 + v)))
                    c_R = c_S * ((0.862 + 1.14 * v) / (1 + v))

                    alum = Lamb(thickness=float(values['thickness']),
                                nmodes_sym=int(values['symmetric']),
                                nmodes_antisym=int(values['antisymmetric']),
                                fd_max=fd_max,
                                vp_max=15000,
                                c_L=c_L,
                                c_S=c_S,
                                c_R=c_R,
                                material=values['material_name'])

                    """
                    Plot phase velocity, group velocity and wavenumber.
                    """

                    print(f"{datetime.now().isoformat(' ', 'seconds')}: Calculating phase velocity for modes: {values['mode'].lower()}")
                    logging.debug('Calculating phase velocity')
                    alum.plot_phase_velocity(modes=values['mode'].lower())
                    print(f"{datetime.now().isoformat(' ', 'seconds')}: Calculating group velocity for modes: {values['mode'].lower()}")
                    alum.plot_group_velocity(modes=values['mode'].lower())
                    print(f"{datetime.now().isoformat(' ', 'seconds')}: Calculating wave number for modes: {values['mode'].lower()}")
                    alum.plot_wave_number(modes=values['mode'].lower())

                    plt.show(block=False)

                elif event == 'Create':

                    IsotropicMaterial.new_material(name=values['new_material_name'],
                                                   mass_density=values['density'],
                                                   E=values['young_modulus'],
                                                   v=values['poisson_ratio'],
                                                   C11=values['C11'],
                                                   C66=values['C66'])

                elif event == 'Close':

                    plt.close(fig='all')

            self.main_window.close()

        except Exception as e:
            sg.popup_error_with_traceback('An error occured', e)


if __name__ == "__main__":

    ui = UI()
