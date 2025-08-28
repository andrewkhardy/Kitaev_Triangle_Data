import matplotlib.pyplot as plt
import h5py as h5
import yaml as yma
from pathlib import Path
import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
os.getcwd()

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

plt.figure(figsize=(10, 4))

# Get the number of hopping values for colormap
num_hoppings = len(data.keys())
colors = plt.cm.viridis_r(np.linspace(0, 1, num_hoppings+1))

for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
    hopping_group = data[hopping_key]
    
    # Extract the data
    xdata_singlet = hopping_group["xdata_singlet"][()]
    ydata_singlet = hopping_group["ydata_singlet"][()]
    #ydata_fit = hopping_group["ydata_fit"][()]
    K_value = hopping_group["J"][()][0]  # K is likely an array with one element

    # Plot the data with viridis colors
    plt.plot(xdata_singlet[1:-1], ydata_singlet[1:-1], marker='o', markersize=7, linewidth=1.5,
             color=colors[i], label=f'K = {K_value:.2f}')
    # plt.plot(xdata_singlet[1:-1], ydata_fit[1:-1], marker='o', markersize=0, linewidth=0.75, alpha=0.75, linestyle='--',
    #          color=colors[i], label="")

# Set plot properties
plt.xlabel(r'$r_1$')
plt.ylabel(r'$\langle \Delta_s^\dagger(r) \Delta_s(0) \rangle$')
plt.xlim(left=1)  # Set x-axis to start at 1
plt.ylim(bottom=1e-16, top=5e-1)
plt.yscale('log')
plt.xscale('symlog', base=2)
plt.legend(fontsize = 18, loc = "lower left")
plt.grid(True, alpha=0.3)
xticks = [2,4, 8, 16, 32,  64]  # Add or adjust as needed for your data range
plt.xticks(xticks, [str(x) for x in xticks])
plt.text(0.05, 0.95, 'a)', transform=plt.gcf().transFigure, 
         fontsize=24, fontweight='bold', verticalalignment='top', 
         horizontalalignment='right')
plt.tight_layout()

plt.savefig("Figure_3a_supp.pdf", format="pdf", bbox_inches='tight')
plt.show()



