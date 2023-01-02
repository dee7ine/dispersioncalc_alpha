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


import matplotlib.pyplot as plt
import numpy as np


def add_plot(ax: plt.Axes, result: dict, mode: str, fd: np.array, **plt_kwargs):
    """Add a dispersion plot for a specific mode to a matplotlib axes
    object.
    
    Parameters
    ----------
    ax : axes
        Matplotlib axes in which the plot will be added.
    result : dict
        A dictionary with a result (vp, vg or k) interpolator at each 
        mode.
    mode : str
        Mode to plot. Can be "A0", "A1", "A2", ..., "An" or "S0", "S1", 
        "S2", ..., "Sn", with 'n' being the order of the corresponding 
        mode.
    fd : array
        An array of frequency thickness values to plot.
    plt_kwargs : dict, optional
        Matplotlib kwargs (to change color, linewidth, linestyle, etc.).
        
    """
    
    var = result[mode](fd)
    n = int(mode[1:]) + 1
    
    # Mode 'A0' and 'S0' are different from the rest (they have labels 
    # for legend and different text positioning when indicating each 
    # mode).
    
    if n == 1:
        legend = 'Symmetric' if mode[0] == 'S' else 'Antisymmetric'
        mode_plot = ax.plot(fd, var, label=legend, **plt_kwargs)
        
        # Get the plot color so that the text indicating the mode is the 
        # same color as the curve.
        
        plot_color = mode_plot[0].get_color()
        ax.text(x=fd[0], y=var[0], color=plot_color, 
                s='$\mathregular{' + mode[0] + '_' + mode[1:] + '}$',
                va='bottom' if mode[0] == 'A' else 'bottom')
    else:
        mode_plot = ax.plot(fd, var, **plt_kwargs)
        
        # Get the plot color so that the text indicating the mode is the 
        # same color as the curve.
        
        plot_color = mode_plot[0].get_color()
        ax.text(x=fd[0], y=var[0], color=plot_color,
                s='$\mathregular{' + mode[0] + '_' + mode[1:] +
                  '}$',
                va='top', ha='right')


def add_cutoff_freqs(ax, mode, arrow_dir, y_max, c_l, c_s,
                     plt_kwargs={'color': 'k', 'ls': '--', 'lw': 0.5}) -> None:
    """
    Add vertical lines indicating cutoff frequencies to a matplotlib
    axes object.
    
    Parameters

    ----------
    :param ax: Matplotlib axes in which the plot will be added.
    :type ax:           Matplotlib axes
    :param mode: Mode to plot. Can be "A0", "A1", "A2", ..., "An" or "S0", "S1",
        "S2", ..., "Sn", with 'n' being the order of the corresponding
        mode.
    :type: mode:        str
    :param arrow_dir: Set arrows' direction in the plot. Can be 'up' (for group
        velocity plots) or 'down' (for phase velocity plots).
    :type arrow_dir:    str
    :param y_max: Maximum y value in the plot. Used to position arrows in phase
        velocity plots.
    :type y_max:        float
    :param c_l: Longitudinal wave velocity of the material, in m/s.
    :type c_l:          float
    :param c_s: Shear wave velocity of the material, in m/s.
    :type c_s:          float
    :param plt_kwargs: (optional argument) Matplotlib kwargs (to change color, linewidth, linestyle, etc.).

    :type plt_kwargs:   dict

    :return
    """
    
    if arrow_dir == 'down':
        arrow_y_pos = y_max
        arrow_str = r'$\downarrow$'
        arrow_va = 'top'
    elif arrow_dir == 'up':
        arrow_y_pos = 0
        arrow_str = r'$\uparrow$'
        arrow_va = 'bottom'
        
    n = int(mode[1:]) + 1

    ax.axvline(x=n*c_s if mode[0] == 'S' else n*c_l,
               **plt_kwargs)
    
    ax.text(x=n*c_s if mode[0] == 'S' else n*c_l,
            y=arrow_y_pos, s=arrow_str, va=arrow_va, ha='center', 
            clip_on=True)

    if n % 2 != 0:
        ax.axvline(x=n*c_l/2 if mode[0] == 'S' else n*c_s/2,
                   **plt_kwargs)
        
        ax.text(x=n*c_l/2 if mode[0] == 'S' else n*c_s/2,
                y=arrow_y_pos, s=arrow_str, va=arrow_va, ha='center', 
                clip_on=True)   


def add_velocities(ax, c_l, c_s, c_r, x_max,
                   plt_kwargs={'color': 'k', 'ls': ':', 'lw': 0.5}):
    """Add horizontal lines indicating material velocities to a 
    matplotlib axes object.
    
    Parameters
    ----------
    ax : axes
        Matplotlib axes in which the plot will be added.
    x_max : float or int
        Maximum x value in the plot. Used to position the velocity 
        labels.
    c_l : float or int
        Longitudinal wave velocity of the material, in m/s.
    c_s: float or int
        Shear wave velocity of the material, in m/s.
    c_r: float or int, optional
        Rayleigh wave velocity of the material, in m/s.
    plt_kwargs : dict, optional
        Matplotlib kwargs (to change color, linewidth, linestyle, etc.).
        
    """
    
    ax.axhline(y=c_l, **plt_kwargs)
    ax.text(x=x_max, y=c_l, s=r'$\mathregular{c_L}$', va='center', ha='left')
    
    ax.axhline(y=c_l, **plt_kwargs)
    ax.text(x=x_max, y=c_l, s=r'$\mathregular{c_S}$', va='center', ha='left')
    
    if c_r:
        ax.axhline(y=c_r, **plt_kwargs)
        ax.text(x=0, y=c_r, s=r'$\mathregular{c_R}$', va='center',
                ha='right')
