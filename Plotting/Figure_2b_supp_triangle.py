import matplotlib.pyplot as plt
import h5py as h5
import yaml as yma
from pathlib import Path
import os,sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
os.getcwd()

filename = "05.06-3.2025_kitaev"

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
ax_main.set_xlabel(r'$r_1$', labelpad=0)
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
# inset_ax.set_xlabel(r'$r_1$', fontsize=10)
# inset_ax.set_ylabel(r'$S_z$', fontsize=10)
# inset_ax.grid(False, alpha=0.3)
#inset_ax.tick_params(labelsize=8)
inset_ax.yaxis.tick_right()
inset_ax.yaxis.set_label_position("right")
inset_ax.xaxis.set_label_position("top")
inset_ax.set_xlabel(r'$r_1$', fontsize = 15)
inset_ax.set_ylabel(r'$\langle S^z \rangle$', fontsize = 15, rotation=0, labelpad=10)
inset_ax.xaxis.tick_top()
plt.text(0.05, 0.9, 'b)', transform=plt.gcf().transFigure, 
         fontsize=24, fontweight='bold', verticalalignment='top', 
         horizontalalignment='right')
inset_ax.tick_params(labelsize=12)
Nr = np.array([
0.7836687512461021,
0.780140258194768,
0.7625122846612427,
0.766912225135322,
0.783523363700815,
0.7860086821878787,
0.7704677560892303,
0.763762821924603,
0.7770287745488091,
0.7855527806501887,
0.776916647867212,
0.7637480189572748,
0.7705532800943097,
0.7860648974499018,
0.7834225852261762,
0.7668215213954556,
0.762567388727211,
0.7803279375561442
], dtype=float)
Sz = np.array([
-0.1435661214895737,
-0.15863906233119457,
-0.17285745257658772,
-0.20282928008017517,
-0.2021215800833528,
-0.20306657313632795,
-0.07143069728742726,
-0.07204785365486155,
-0.07222585105277769,
0.07224844000102208,
0.07206999005698234,
0.07145170847438806,
0.20307095647690215,
0.20212241977494994,
0.2028268488280099,
0.1728422297098619,
0.15862045785287002,
0.1435477325523684
], dtype=float)
sizes = 180 * (Nr / Nr.mean())
s_min, s_max = 500.0, 800.0
gamma = 2.5  # >1 amplifies differences
Nr_norm = (Nr - Nr.min()) / (Nr.max() - Nr.min() + 1e-12)
sizes = s_min + (s_max - s_min) * (Nr_norm ** gamma)


plot_lattice(Lx=6, Ly=3, pbcx=False, pbcy=False,sizes = sizes, spins = Sz, ax=ax_lat, zoom = 1.2)

fig.tight_layout()
fig.savefig("Figure_2b_supp_triangle.pdf", format="pdf", bbox_inches='tight')
plt.show()

