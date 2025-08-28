import matplotlib.pyplot as plt
import h5py as h5
import yaml as yma
from pathlib import Path
import os,sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
os.getcwd()

filename = "05.04-3.2025_kitaev"

plt.style.use("lake.mplstyle")
plt.rcParams.update({"text.usetex": True})

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Computer Modern Roman"] + plt.rcParams["font.serif"]
plt.rcParams.update({"text.usetex": True})
#file = "./Plotting/Data/"+filename+"_spin_data.jld2"
file = "./Data/"+filename+"_spin_data.h5"

f =  h5.File(file, "r") 

data = f["hopping_data"]
num_hoppings = len(data.keys())

colors = plt.cm.viridis_r(np.linspace(0, 1, num_hoppings))


from triangle import plot_lattice

fig, (ax_main, ax_lat) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 2], 'hspace': 0.05})
#
#plt.figure(figsize=(10, 6))

# Main plot - second plot data
for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
    hopping_group = data[hopping_key]
    xdata_Sz = hopping_group["xdata_SzSz"][()]
    ydata_Sz = hopping_group["ydata_SzSz"][()]
    J_value = hopping_group["J"][()][0]
    ax_main.plot(xdata_Sz, ydata_Sz, marker='o', markersize=5, linewidth=1.5, 
                 color=colors[i], label=f'K = {J_value:.2f}')

# Set plot properties for main plot
ax_main.set_xlabel(r'$r_x$', labelpad=0)
ax_main.xaxis.set_label_coords(0.5, -0.025)  # x in [0,1], y below axis

ax_main.set_ylabel(r'$ \langle S^z(r) S^z(0) \rangle_c$')
ax_main.set_xlim(left=1)
ax_main.set_yscale('log')
ax_main.set_xscale('symlog', base=2)
ax_main.legend(fontsize=18, loc='upper right')
xticks = [2, 4, 8, 16, 32, 64, 128]
ax_main.set_xticks(xticks)
ax_main.set_xticklabels([str(x) for x in xticks])
ax_main.grid(True, alpha=0.3)

# Create inset axes
inset_ax = inset_axes(ax_main, width="40%", height="40%", loc='lower left')

# Plot first plot data in the inset
for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
    hopping_group = data[hopping_key]
    
    # Extract the data
    xdata_Sz = hopping_group["xdata_Sz"][()]
    ydata_Sz = hopping_group["ydata_Sz"][()]
    J_value = hopping_group["J"][()][0]  # J is likely an array with one element
    
    # Plot the data with viridis colors in the inset
    inset_ax.plot(xdata_Sz[0:12], ydata_Sz[0:12], marker='o', markersize=3, linewidth=1, 
                  color=colors[i])

# Set inset properties
# inset_ax.set_xlabel(r'$r_x$', fontsize=10)
# inset_ax.set_ylabel(r'$S_z$', fontsize=10)
# inset_ax.grid(False, alpha=0.3)
#inset_ax.tick_params(labelsize=8)
inset_ax.yaxis.tick_right()
inset_ax.yaxis.set_label_position("right")
inset_ax.xaxis.set_label_position("top")
inset_ax.set_xlabel(r'$r_x$', fontsize = 15)
inset_ax.set_ylabel(r'$\langle S^z \rangle$', fontsize = 15, rotation=0, labelpad=10)
inset_ax.xaxis.tick_top()
plt.text(0.05, 0.9, 'b)', transform=plt.gcf().transFigure, 
         fontsize=24, fontweight='bold', verticalalignment='top', 
         horizontalalignment='right')
inset_ax.tick_params(labelsize=12)
Nr = np.array([
    0.9006662282606225,
    0.8975929479059503,
    0.9169100575995464,
    0.8668162774387197,
    0.8687092462803484,
    0.868388327076888,
    0.8944745322153683,
    0.8941694536033505,
    0.8942037471524861,
    0.897274567171946,
    0.8973014897959928,
    0.8974867761905686,
    0.8679080787028131,
    0.8681721058460664,
    0.8659284552827201,
    0.9135956743144377,
    0.8937469483720247,
    0.8966551123440372
], dtype=float)
Sz = np.array([
    0.2877743797618545,
    0.2893226899692477,
    0.3041313953538505,
   -0.04077436885863283,
   -0.04194394299404386,
   -0.0434317219774416,
   -0.21438496643215252,
   -0.21389542718439594,
   -0.2137075289798184,
    0.22900347052040343,
    0.2293721218304247,
    0.22994616954475386,
    0.010549154163861684,
    0.008429515885409211,
    0.0071968228249837335,
   -0.2938893761602558,
   -0.27781691793593777,
   -0.27654036316937547
], dtype=float)
sizes = 180 * (Nr / Nr.mean())
s_min, s_max = 100.0, 1000.0
gamma = 2.5  # >1 amplifies differences
Nr_norm = (Nr - Nr.min()) / (Nr.max() - Nr.min() + 1e-12)
sizes = s_min + (s_max - s_min) * (Nr_norm ** gamma)


plot_lattice(Lx=6, Ly=3, pbcx=False, pbcy=False,sizes = sizes, spins = Sz, ax=ax_lat, zoom = 1.2)

fig.tight_layout()
fig.savefig("Figure_2b.pdf", format="pdf", bbox_inches='tight')
plt.show()
