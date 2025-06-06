# Created By: Batsal Pudasaini
# Created On: 6/6/2025
# Create Heat Pump Web Based Application Tool
# python C:\Users\Batsalp\Documents\PythonPrograms\HPAppTool1.py
# C:\Users\Batsalp\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\pyinstaller --onefile --noconsole HPAppTool1.py
# HP Envelope Plot Streamlit Version
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

st.set_page_config(page_title="Heat Pump Tool", layout="centered")

def plot_heat_pump_envelope(plot_type):
    title_fs = 5
    label_fs = 4
    Tw_delta = 0
    Ta_delta = 20
    Tw_env = [105,105,120,150,165,165,139,105]
    Ta_env = [13,47,60,75,75,27,13,13]

    Ta_grid, Tw_grid = np.meshgrid(np.linspace(-10, 110, 500), np.linspace(20, 250, 500))

    SH = 20  # Superheat
    Hz = 60  # Compressor Speed
    FS = 45  # Fan Speed

    points = np.vstack((Ta_grid.flatten(), Tw_grid.flatten())).T
    polygon = Path(np.vstack((Ta_env, Tw_env)).T)
    in_mask = polygon.contains_points(points).reshape(Ta_grid.shape)

    fig, ax = plt.subplots(figsize=(1.6,1.1))
    ax.plot(Ta_env, Tw_env, linewidth=0.6)
    ax.set_xlabel('Ambient Temperature [°F]', fontsize=label_fs)
    ax.set_ylabel('Water Temperature [°F]', fontsize=label_fs)
    ax.set_xlim([5, 80])
    ax.set_ylim([100, 170])

    if plot_type == 'Heat Pump Envelope with Heating Capacity':
        ax.set_title('Heat Pump Envelope with Heating Capacity [Btu/Hr]', fontsize=title_fs)
        HeatOutput = (3581.89 * Ta_grid - 928.36 * Tw_grid -
                      1977.98 * SH + 3657.22 * Hz + 43428.64)
        HeatOutput[~in_mask] = np.nan
        levels = np.arange(100000, 350001, 12500)
        contour = ax.contourf(Ta_grid, Tw_grid, HeatOutput, levels=levels, cmap='viridis')
        cbar = fig.colorbar(contour, ax=ax)
        cbar.set_label('Heating Capacity [Btu/hr]', fontsize=label_fs)
        cbar.ax.tick_params(labelsize=label_fs)
        ax.tick_params(axis='both', labelsize=label_fs)  # axes tick labels
    elif plot_type == 'Heat Pump Envelope with COP':
        ax.set_title('Heat Pump Envelope with Heating COP', fontsize=title_fs)
        COP = (0.00012 * Tw_grid * Ta_grid - 0.02574 * Tw_grid +
               0.003015 * Ta_grid - 0.0142 * SH - 0.0065 * (FS - 50) + 5.2573)
        COP[~in_mask] = np.nan
        levels = np.arange(1.2, 3.1, 0.09)
        contour = ax.contourf(Ta_grid, Tw_grid, COP, levels=levels, cmap='plasma', linewidths=0.5)
        cbar = fig.colorbar(contour, ax=ax)
        cbar.set_label('COP', fontsize=label_fs)
        cbar.ax.tick_params(labelsize=label_fs)
        ax.tick_params(axis='both', labelsize=label_fs)  # axes tick labels
    else:
        Tw_env2 = [Tw_env[1], Tw_env[2], Tw_env[3], Tw_env[4], Tw_env[4], 130, Tw_env[1]]
        Ta_env2 = [Ta_env[1], Ta_env[2], Ta_env[3], Ta_env[4], Ta_env[4]+5, Ta_env[4]+5, 65]
        ax.fill(Ta_env2, Tw_env2, color=(0.7, 0.9, 1), alpha=0.6, edgecolor='none')
        label_Ta = np.mean(Ta_env2) + 2
        label_Tw = np.mean(Tw_env2) - 8
        ax.text(label_Ta, label_Tw, 'With\nAdditional\nComponents',
                ha='center', fontsize=2)
        ax.set_xlim([5, 85])
        ax.set_ylim([100, 170])
        ax.tick_params(axis='both', labelsize=label_fs)  # axes tick labels

    return fig

def main():
    st.title("Heat Pump Envelope Plot VER 1.0")
    st.write("Select plot type and click plot to generate the graph.")

    plot_type = st.selectbox("Plot Type", [
        'Heat Pump Envelope',
        'Heat Pump Envelope with Heating Capacity',
        'Heat Pump Envelope with COP'
    ])

    if st.button("Plot"):
        fig = plot_heat_pump_envelope(plot_type)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
