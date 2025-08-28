import matplotlib.pyplot as plt
import h5py as h5
import yaml as yma
from pathlib import Path
import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

loc = "/media/andrewhardy/9C33-6BBD/t_J/MFT/"
#loc = "/home/andrewhardy/Documents/Graduate/CCQ/Data/t_J_Data/"
os.getcwd()

filename = "05.07-3.2025_kitaev"
#filename = "06.26.2025_triangle"
filename = "07.05.2025_kitaev"

plt.style.use("lake.mplstyle")
plt.rcParams.update({"text.usetex": True})

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Computer Modern Roman"] + plt.rcParams["font.serif"]
plt.rcParams.update({"text.usetex": True})
#file = "./Plotting/Data/"+filename+"_spin_data.jld2"
file = "./Data/"+filename+"_superconduct_data.h5"

f =  h5.File(file, "r") 

data = f["hopping_data"]

plt.figure(figsize=(10,4))
plt.text(0.05, 0.95, 'b)', transform=plt.gcf().transFigure, 
         fontsize=24, fontweight='bold', verticalalignment='top', 
         horizontalalignment='right')
# Get the number of hopping values for colormap
num_hoppings = len(data.keys())
colors = plt.cm.viridis_r(np.linspace(0, 1, num_hoppings+1))

# # Iterate through each hopping value
# for i, hopping_key in enumerate(list(reversed(data.keys()))):
#     hopping_group = data[hopping_key]
    
#     # Extract the data
#     xdata_Sz = hopping_group["xdata_Sz"][()]
#     ydata_Sz = hopping_group["ydata_Sz"][()]
#     J_value = hopping_group["J"][()][0]  # J is likely an array with one element
    
#     # Plot the data with viridis colors
#     plt.plot(xdata_Sz[0:10], ydata_Sz[0:10], marker='o', markersize=5, linewidth=1.5, 
#              color=colors[i], label=f'J = {J_value:.2f}')

# # Set plot properties
# plt.xlabel(r'$r_1$')
# plt.ylabel(r'$S_z$')
# #plt.title('$S_z$ Data vs Position')
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()
# plt.figure(figsize=(10, 6))


for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
    hopping_group = data[hopping_key]
    
    # Extract the data
    xdata_triplet = hopping_group["xdata_triplet"][()]
    ydata_triplet = hopping_group["ydata_triplet"][()]
    #ydata_fit = hopping_group["ydata_fit"][()]
    K_value = hopping_group["J"][()][0]  # K is likely an array with one element

    # Plot the data with viridis colors
    plt.plot(xdata_triplet[1:-1], ydata_triplet[1:-1], marker='o', markersize=7, linewidth=1.5,
             color=colors[i], label=f'K = {K_value:.2f}')
    # plt.plot(xdata_triplet[1:-1], ydata_fit[1:-1], marker='o', markersize=0, linewidth=0.75, alpha=0.75, linestyle='--',
    #          color=colors[i], label="")

# Set plot properties
plt.xlabel(r'$r_1$')
plt.ylabel(r'$\langle \Delta_t^\dagger(r) \Delta_t(0) \rangle$')
plt.xlim(left=1)  # Set x-axis to start at 1
plt.ylim(bottom=1e-16, top=5e-1)

plt.yscale('log')
plt.xscale('symlog', base=2)
plt.legend(fontsize = 18, loc = "lower left")
plt.grid(True, alpha=0.3)
xticks = [2,4, 8, 16, 32,  64]  # Add or adjust as needed for your data range
plt.xticks(xticks, [str(x) for x in xticks])
plt.tight_layout()
plt.savefig("Figure_3x_supp.pdf", format="pdf", bbox_inches='tight')
plt.show()

# # Main plot - second plot data
# for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
#     hopping_group = data[hopping_key]
    
#     # Extract the data
#     xdata_Sz = hopping_group["xdata_SzSz"][()]
#     ydata_Sz = hopping_group["ydata_SzSz"][()]
#     J_value = hopping_group["J"][()][0]  # J is likely an array with one element
    
#     # Plot the data with viridis colors
#     plt.plot(xdata_Sz, ydata_Sz, marker='o', markersize=5, linewidth=1.5, 
#              color=colors[i], label=f'J = {J_value:.2f}')

# # Set plot properties for main plot
# plt.xlabel(r'$r_1$')
# plt.ylabel(r'$ \langle S^z(r) S^z(0) \rangle$')
# plt.xlim(left=1)  # Set x-axis to start at 1
# plt.yscale('log')
# plt.xscale('symlog', base=2)
# plt.legend()
# plt.grid(True, alpha=0.3)

# # Create inset axes
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# inset_ax = inset_axes(plt.gca(), width="40%", height="40%", loc='lower left')

# # Plot first plot data in the inset
# for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
#     hopping_group = data[hopping_key]
    
#     # Extract the data
#     xdata_Sz = hopping_group["xdata_Sz"][()]
#     ydata_Sz = hopping_group["ydata_Sz"][()]
#     J_value = hopping_group["J"][()][0]  # J is likely an array with one element
    
#     # Plot the data with viridis colors in the inset
#     inset_ax.plot(xdata_Sz[0:12], ydata_Sz[0:12], marker='o', markersize=3, linewidth=1, 
#                   color=colors[i])

# # Set inset properties
# # inset_ax.set_xlabel(r'$r_1$', fontsize=10)
# # inset_ax.set_ylabel(r'$S_z$', fontsize=10)
# # inset_ax.grid(False, alpha=0.3)
# #inset_ax.tick_params(labelsize=8)
# inset_ax.yaxis.tick_right()
# inset_ax.yaxis.set_label_position("right")
# inset_ax.xaxis.set_label_position("top")
# inset_ax.xaxis.tick_top()

# inset_ax.tick_params(labelsize=12)
# plt.tight_layout()
# plt.savefig("Figure_2a.pdf", format="pdf", bbox_inches='tight')
# plt.show()