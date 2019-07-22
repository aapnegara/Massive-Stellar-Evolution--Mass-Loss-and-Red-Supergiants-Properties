#!/usr/bin/env python
import mkipp
import kipp_data
import mesa_data
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
import numpy as np

#simple example (saves to default filename Kippenhahn.png)
# mkipp.kipp_plot(mkipp.Kipp_Args())

def init_plotting(x=9,y=7):
    plt.rcParams['figure.figsize'] = (x,y)
    plt.rcParams['font.size'] = 20
    plt.rcParams['figure.facecolor'] = '#dddddd'
    # plt.rcParams['font.family'] = 'Asana Math'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 0.75*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = 0.65*plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.fontsize'] = 13
    plt.rcParams['legend.loc'] = 'best'
    plt.rcParams['axes.linewidth'] = 1

init_plotting()

# In[]

fig = plt.figure()
axis = plt.gca()

history = mesa_data.mesa_data("../LOGS_00/history.data", read_data_cols = ["star_age","star_mass"])
max_age = max(history.get("star_age"))

kipp_plot = mkipp.kipp_plot(mkipp.Kipp_Args(logs_dirs=["../LOGS_00"],
    xaxis = "star_age",
    time_units = "yr",
    function_on_xaxis = lambda x: np.log10(max_age+0.01 - x),
    decorate_plot = False,
    save_file = False,
    show_conv = True, show_therm = True, show_semi = True, show_over = True,
    show_rot = False,
    contour_colormap = plt.get_cmap("inferno_r"),
    core_masses=["He","C","O"]), axis = axis)
bar = plt.colorbar(kipp_plot.contour_plot,pad=0.05)
bar.set_label("$log_{10}(\epsilon_{nuc}) \, \, [erg/g/s]$")
axis.plot(np.log10(max_age+0.01-history.get("star_age")),history.get("star_mass"),linewidth=2,c="k")
axis.invert_xaxis()
axis.set_title("Diagrama de Kippenhahn $| \, \Omega/\Omega_{crit} = 0.0$")
axis.set_xlabel("$log_{10}(t_{max}-t) \, \, [yrs]$")
axis.set_ylabel("$M \, \, [M_{\odot}$]")
axis.set_xlim([6.9,-2.01])
fig.savefig("kipp_00.png")


# In[]
fig = plt.figure()
axis = plt.gca()

history = mesa_data.mesa_data("../LOGS_03/history.data", read_data_cols = ["star_age","star_mass"])
max_age = max(history.get("star_age"))

kipp_plot = mkipp.kipp_plot(mkipp.Kipp_Args(logs_dirs=["../LOGS_03"],
    xaxis = "star_age",
    time_units = "yr",
    function_on_xaxis = lambda x: np.log10(max_age+0.01 - x),
    decorate_plot = False,
    save_file = False,
    show_conv = True, show_therm = True, show_semi = True, show_over = True,
    show_rot = False,
    contour_colormap = plt.get_cmap("inferno_r"),
    core_masses=["He","C","O"]), axis = axis)
bar = plt.colorbar(kipp_plot.contour_plot,pad=0.05)
bar.set_label("$log_{10}(\epsilon_{nuc}) \, \, [erg/g/s]$")
axis.plot(np.log10(max_age+0.01-history.get("star_age")),history.get("star_mass"),linewidth=2,c="k")
axis.set_title("Diagrama de Kippenhahn $| \, \Omega/\Omega_{crit} = 0.3$")
axis.invert_xaxis()
axis.set_xlabel("$log_{10}(t_{max}-t) \, \, [yrs]$")
axis.set_ylabel("$M \, \, [M_{\odot}$]")
axis.set_xlim([6.97,-2.02])
fig.savefig("kipp_03.png")
