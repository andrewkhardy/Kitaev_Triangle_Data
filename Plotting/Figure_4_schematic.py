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
filename = "06.26.2025_kitaev"

plt.style.use("lake.mplstyle")
plt.rcParams.update({"text.usetex": True})

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Computer Modern Roman"] + plt.rcParams["font.serif"]
plt.rcParams.update({"text.usetex": True})
#file = "./Plotting/Data/"+filename+"_spin_data.jld2"
file = "./Data/"+filename+"_superconduct_data.h5"

f =  h5.File(file, "r") 

data = f["hopping_data"]

plt.figure(figsize=(10, 5))

# Get the number of hopping values for colormap
num_hoppings = len(data.keys())
colors = plt.cm.viridis(np.linspace(0, 1, num_hoppings+3))
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

v_arr = np.zeros(num_hoppings)
k_arr = np.zeros(num_hoppings)

for i, hopping_key in enumerate(list(reversed(data.keys()))[0:-1]):
    hopping_group = data[hopping_key]
    
    # Extract the data
    xdata_singlet = hopping_group["xdata_singlet"][()]
    ydata_singlet = hopping_group["ydata_singlet"][()]
    ydata_fit = hopping_group["ydata_fit"][()]
    V_value = hopping_group["V"][()][0]  # V is likely an array with one element
    K_value = hopping_group["kappasc"][()][0]  # kappasc is likely an array with one element
    v_arr[i] = V_value /2
    k_arr[i] = K_value
    # Plot the data with viridis colors
    plt.plot(xdata_singlet[1:-10], ydata_singlet[1:-10], marker='o', markersize=7, linewidth=1.5,
             color=colors[i], label=f'V = {V_value/2:.2f}')
    plt.plot(xdata_singlet[1:-10], ydata_fit[1:-10], marker='o', markersize=0, linewidth=0.75, alpha=0.75, linestyle='--',
             color=colors[i], label="")

# Set plot properties
plt.xlabel(r'$r_1$')
plt.ylabel(r'$\langle \Delta^\dagger_s(r) \Delta_s(0) \rangle$')
plt.xlim(left=1)  # Set x-axis to start at 1

plt.yscale('log')
#plt.xscale('log')
plt.xscale('symlog', base=2)
plt.legend(fontsize = 14, loc = "upper left")
plt.grid(True, alpha=0.3)
xticks = [2,4, 8, 16, 32,  64, 128]  # Add or adjust as needed for your data range
plt.xticks(xticks, [str(x) for x in xticks])
ax_main = plt.gca()

# Create inset axes
inset_ax = inset_axes(ax_main, width="35%", height="42%", loc='lower left')
# inset_ax.text(0.3, 0.3, r'$K_{SC}$', transform=inset_ax.transAxes,
#               fontsize=16, verticalalignment='top', horizontalalignment='right')

# Plot the data with viridis colors in the inset
inset_ax.plot(v_arr[0:-1], k_arr[0:-1], marker='o', markersize=6, linewidth=1.5,
                color="purple")


inset_ax.yaxis.tick_right()
inset_ax.yaxis.set_label_position("right")
inset_ax.xaxis.set_label_position("top")
inset_ax.xaxis.tick_top()
inset_ax.set_xlabel(r'$V$', fontsize = 14)
inset_ax.set_ylabel(r'$K_{SC}$', fontsize = 14, rotation=0)
inset_ax.tick_params(labelsize=15)
plt.tight_layout()
# Second inset (right): draw d-wave schematic directly
dw_bbox  = (0.25, 0.01, 0.65, 0.65)  # right inset (d-wave schematic)

d_ax = inset_axes(
    ax_main, width="100%", height="100%",
    bbox_to_anchor=dw_bbox, bbox_transform=ax_main.transAxes, borderpad=0
)
# Coordinates for the lattice points
pts = {
    "center": (0.0, 0.0),
    "left": (-1.0, 0.0),
    "right": (1.0, 0.0),
    "nw": (-0.5, 0.5),
    "ne": (0.5, 0.5),
    "sw": (-0.5, -0.5),
    "se": (0.5, -0.5),
}

# Lines: dotted horizontal, dashed diagonals, solid diagonals
d_ax.plot([pts["left"][0], pts["right"][0]], [0, 0], linestyle=(0, (1, 3)), color="black", lw=1.5)
d_ax.plot([0, pts["nw"][0]], [0, pts["nw"][1]], linestyle=(0, (4, 2)), color="black", lw=1.5)
d_ax.plot([0, pts["se"][0]], [0, pts["se"][1]], linestyle=(0, (4, 2)), color="black", lw=1.5)
d_ax.plot([0, pts["ne"][0]], [0, pts["ne"][1]], color="black", lw=1.5)
d_ax.plot([0, pts["sw"][0]], [0, pts["sw"][1]], color="black", lw=1.5)
hex_order = ["nw", "ne", "right", "se", "sw", "left"]
for i in range(len(hex_order)):
    p1 = pts[hex_order[i]]
    p2 = pts[hex_order[(i + 1) % len(hex_order)]]
    d_ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black", lw=1.5)
# Open circles
for (x, y) in pts.values():
    d_ax.scatter(x, y, s=25, facecolor="white", edgecolor="slateblue", linewidth=1.6, zorder=3)
# Labels on bonds (place at midpoints of bonds from center)
def midpoint(a, b):
    return ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)

m_left = midpoint(pts["center"], pts["left"])
m_right = midpoint(pts["center"], pts["right"])
m_nw = midpoint(pts["center"], pts["nw"])
m_ne = midpoint(pts["center"], pts["ne"])
m_sw = midpoint(pts["center"], pts["sw"])
m_se = midpoint(pts["center"], pts["se"])

# d-wave signs: + on NE and SW (solid diagonals), − on NW and SE (dashed diagonals), 0 on horizontal bonds
d_ax.text(m_nw[0]+0.175, m_nw[1]+0.1, r'$-$', color="black", ha="center", va="center", fontsize=20, zorder=4)
d_ax.text(m_ne[0]+0.2, m_ne[1]+0.05, r'$+$', color="black", ha="center", va="center", fontsize=20, zorder=4)
d_ax.text(m_sw[0]-0.15, m_sw[1]+0.0, r'$+$', color="black", ha="center", va="center", fontsize=20, zorder=4)
d_ax.text(m_se[0]-0.175, m_se[1]+0.0, r'$-$', color="black", ha="center", va="center", fontsize=20, zorder=4)
d_ax.text(m_left[0], m_left[1]+0.1, r'$0$', color="black", ha="center", va="center", fontsize=20, zorder=4)
d_ax.text(m_right[0], m_right[1]-0.125, r'$0$', color="black", ha="center", va="center", fontsize=20, zorder=4)

# Aesthetics for the inset
d_ax.set_aspect("equal", adjustable="box")
d_ax.set_xlim(-1.25, 1.25)
d_ax.set_ylim(-1.2, 1.2)
d_ax.axis("off")

plt.tight_layout()
plt.savefig("Figure_4.pdf", format="pdf", bbox_inches='tight')
plt.show()
