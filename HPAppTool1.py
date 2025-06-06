# Created By: Batsal Pudasaini
# Created On: 6/6/2025
# Create Heat Pump Web Based Application Tool
# python C:\Users\Batsalp\Documents\PythonPrograms\HPAppTool1.py
# C:\Users\Batsalp\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\pyinstaller --onefile --noconsole HPAppTool1.py
import os
import xlrd
import pandas as pd
from os.path import exists
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.formatting.rule import CellIsRule
import time

def PlotHeatPumpEnvelope():
    plotfig_window.clf()
    # Setup and input parameters
    Tw_delta = 0
    Ta_delta = 20
    Tw_env = [105,105,120,150,165,165,139,105]
    Ta_env = [13,47,60,75,75,27,13,13]

    # Meshgrid for plotting
    Ta_grid, Tw_grid = np.meshgrid(np.linspace(-10, 110, 500), np.linspace(20, 250, 500))

    # Assumptions
    SH = 20  # Superheat
    Hz = 60  # Compressor Speed
    FS = 45  # Fan Speed

    # Envelope mask
    from matplotlib.path import Path
    points = np.vstack((Ta_grid.flatten(), Tw_grid.flatten())).T
    polygon = Path(np.vstack((Ta_env, Tw_env)).T)
    in_mask = polygon.contains_points(points).reshape(Ta_grid.shape)

    PlotType = PlotTypeOptions.get()

    # Plot setup
    ax = plotfig_window.add_subplot(111)  # use 111 if it's a single plot
    ax.clear()  # Clear old plot if redrawing
    ax.plot(Ta_env, Tw_env, linewidth=1.2)
    ax.set_xlabel('Ambient Temperature [°F]')
    ax.set_ylabel('Water Temperature [°F]')
    ax.set_xlim([5, 80])
    ax.set_ylim([100, 170])

    if 'Heating Capacity' in PlotType:
        title = 'Heat Pump Envelope with Heating Capacity [Btu/Hr]'
        ax.set_title(title)

        HeatOutput = (3581.89 * Ta_grid - 928.36 * Tw_grid -
                      1977.98 * SH + 3657.22 * Hz + 43428.64)
        HeatOutput[~in_mask] = np.nan

        levels = np.arange(100000, 350001, 12500)
        contour = ax.contourf(Ta_grid, Tw_grid, HeatOutput, levels=levels, cmap='viridis')
        plotfig_window.colorbar(contour, ax=ax, label='Heating Capacity [Btu/hr]')
        ax.set_xlim([5, 80])
        ax.set_ylim([100, 170])

    elif 'COP' in PlotType:
        title = 'Heat Pump Envelope with Heating COP'
        ax.set_title(title)

        COP = (0.00012 * Tw_grid * Ta_grid - 0.02574 * Tw_grid +
               0.003015 * Ta_grid - 0.0142 * SH - 0.0065 * (FS - 50) + 5.2573)
        COP[~in_mask] = np.nan

        levels = np.arange(1.2, 3.1, 0.09)
        contour = ax.contourf(Ta_grid, Tw_grid, COP, levels=levels, cmap='plasma')
        plotfig_window.colorbar(contour, ax=ax, label='COP')
        ax.set_xlim([5, 80])
        ax.set_ylim([100, 170])

    else:
        Tw_env2 = [Tw_env[1], Tw_env[2], Tw_env[3], Tw_env[4], Tw_env[4], 130, Tw_env[1]]
        Ta_env2 = [Ta_env[1], Ta_env[2], Ta_env[3], Ta_env[4], Ta_env[4]+5, Ta_env[4]+5, 65]
        ax.fill(Ta_env2, Tw_env2, color=(0.7, 0.9, 1), alpha=0.6, edgecolor='none')

        label_Ta = np.mean(Ta_env2) + 2
        label_Tw = np.mean(Tw_env2) - 8
        ax.text(label_Ta, label_Tw, 'With\nAdditional\nComponents',
                ha='center', fontsize=8, fontweight='bold')
        ax.set_xlim([5, 85])
        ax.set_ylim([100, 170])

    # plt.tight_layout()
    # plt.show()
    chart_type.draw()  # refresh the canvas



lfs = 12
# color = "#556B2F"
# colorbckgnd = "#B0C4DE"
color = "light slate gray"

window = tk.Tk()
window.title("HP Envelope Plot VER 1.0")
window.geometry('920x650')
window.configure(background=color)

# tabcontrol = ttk.Notebook(window)
# ttk.Style().configure("TNotebook.Tab", font=("Times",12), foreground=color)
# tabcontrol.grid(row=1,column=1)

label = tk.Label(master=window,text=" ", font=("Times",5), bd = 2,background=color)
label.grid(row=0,column=0,sticky="W")

# tab1 = tk.Frame(tabcontrol, width = 800, height = 500,background=color)
# tab1.grid(row=0,column=0)
# tabcontrol.add(tab1, text = 'HP Output Plots')

label = tk.Label(master=window,text="Plot Type  ", font=("Times",lfs), width=15, bd = 2,background= color)
label.grid(row=1,column=0,sticky="W")

PlotTypeOptions = ttk.Combobox(master=window, width=35, font=("Times",lfs))
PlotTypeOptions['values'] = ('Heat Pump Envelope', 'Heat Pump Envelope with Heating Capacity', 'Heat Pump Envelope with COP')
PlotTypeOptions.grid(row=1,column=1,sticky="W")

b = tk.Button(master=window, text="PLOT", command=PlotHeatPumpEnvelope, font=("Times",lfs))
b.grid(row=1, column=2,columnspan=2, rowspan=2,sticky="W", padx=5, pady=5)

label = tk.Label(master=window,text=" ", font=("Times",lfs), bd = 2,background= color)
label.grid(row=0,column=0,sticky="W")

plotfig_window = plt.Figure(figsize=(7, 5), dpi=100)
chart_type = FigureCanvasTkAgg(plotfig_window, window)
chart_type.get_tk_widget().grid(row=3,column=1,sticky="W")

label = tk.Label(master=window,text=" ", font=("Times",lfs), bd = 2,background= color)
label.grid(row=4,column=1,sticky="W")

window.mainloop()