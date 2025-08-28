import matplotlib.pyplot as plt
import h5py as h5
import yaml as yma
from pathlib import Path
import os,sys
import numpy as np
import matplotlib.pyplot as plt
loc = "/media/andrewhardy/9C33-6BBD/t_J/MFT/"
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
os.getcwd()

filename = "07.05.2025_kitaev"

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

#Create inset axes
inset_ax = inset_axes(ax_main, width="40%", height="40%", loc='lower left')

# Plot first plot data in the inset
for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
    hopping_group = data[hopping_key]
    
    # Extract the data
    xdata_Sz = hopping_group["xdata_Sz"][()]
    ydata_Sz = hopping_group["ydata_Sz"][()]
    J_value = hopping_group["J"][()][0]  # J is likely an array with one element
    
    # Plot the data with viridis colors in the inset
    inset_ax.plot(xdata_Sz[0:12], -1*ydata_Sz[0:12], marker='o', markersize=3, linewidth=1, 
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
plt.text(0.05, 0.9, 'a)', transform=plt.gcf().transFigure, 
         fontsize=24, fontweight='bold', verticalalignment='top', 
         horizontalalignment='right')
inset_ax.tick_params(labelsize=12)
inset_ax.set_ylim(-0.1, 0.1)
Nr = np.array([
0.7852985785045566,
0.7017786728615056,
0.8198897530185436,
0.7925999495433111,
0.7042318855356682,
0.806593198259663,
0.8130906716248895,
0.722431762174882,
0.795823860450341,
0.8278018807944046,
0.7090116217718526,
0.8193731755186654,
0.8232589621447876,
0.6995714044562747,
0.8362673046878776,
0.7934920809093132,
0.7151429497329354,
0.8343418175657263
], dtype=float)
Sz =  np.array([
-7.205705093812661e-9,
4.0250408994451085e-9,
7.290737425393828e-10,
-6.257067748444579e-10,
-2.248108466963753e-9,
4.71688802159242e-9,
2.6919384913397234e-9,
-5.772810036826713e-10,
-2.081526232115298e-9,
7.116739160887483e-11,
1.2209504020039438e-9,
-1.496875118103465e-9,
-2.658520059170352e-9,
4.908221396722541e-10,
-1.1601192524535512e-10,
4.554598766567072e-9,
-2.590758226025484e-9,
-4.300245960270727e-9
], dtype=float)
sizes = 180 * (Nr / Nr.mean())
s_min, s_max = 100.0, 1000.0
gamma = 2.5  # >1 amplifies differences
Nr_norm = (Nr - Nr.min()) / (Nr.max() - Nr.min() + 1e-12)
sizes = s_min + (s_max - s_min) * (Nr_norm ** gamma)


plot_lattice(Lx=6, Ly=3, pbcx=False, pbcy=False,sizes = sizes, ax=ax_lat, zoom = 1.2)

fig.tight_layout()
fig.savefig("Figure_2a_supp_triangle.pdf", format="pdf", bbox_inches='tight')
plt.show()