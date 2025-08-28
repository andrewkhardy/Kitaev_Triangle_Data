#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 09:07:16 2023

@author: andrewhardy
"""
import json, sys, os, re, h5
import numpy as np
os.chdir("/home/andrewhardy/Documents/Graduate/CCQ/SYK_yukawa/Plotting")
import pandas as pd
from collapse import collapse_arrays
from triqs.gf import *
from triqs.gf.tools import *
from triqs.operators import *
from triqs.gf.block_gf import *
from triqs.plot.mpl_interface import *
from triqs.gf.descriptors import Function
from triqs.utility import mpi
from scipy.optimize import curve_fit
#import triqs_ctseg as ctseg_new
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

os.getcwd()
sys.path.append(os.getcwd())
plt.rcParams.update(plt.rcParamsDefault)

plt.style.use("lake.mplstyle")
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Computer Modern Roman"] + plt.rcParams["font.serif"]
plt.rcParams.update({"text.usetex": True})

location = "/home/andrewhardy/Documents/Graduate/CCQ/"




def fitting(function,xdata,ydata, guess,extend = 1.0):
    fit_opt, fit_cov = curve_fit(function,xdata,ydata,p0 = guess,maxfev = 12000)
    xfit = np.linspace(np.nanmin(xdata), np.nanmax(xdata)*extend, 50)

    return xfit, function(xfit,*fit_opt), fit_opt, fit_cov

def linear(x,a):
    return a*x
def linear_offset(x,a,b,c):
    return a*x +np.abs(b)
def quadratic(x,a,b,c):
    
    return a*x+b*x**2 +c*x**3
def powerlaw(x,a,b,c):
    return a*x**b+c
def logmassfit(x,a,b,c):
    return a*(x)*np.log(b/x)+np.abs(c)
    #return a*x**(2/3)#+b
def logmassfit(x,a,b,c,d):
    return a*(x)*np.log(b/(c+x))+np.abs(d)

def squareroot(x,a,b):
    return a*np.sqrt(x)+b
inputname = "02.05.2024_SYK_U-2.0"
inputname = "03.15.2024_SYK_U-2.0"
#inputname = "02.15.2024_SYK_U-0.0"
inputname = "04.15.2024_SYK_U-2.0"
inputfile = location + "SYK_yukawa/Input/" + inputname + ".json"
outlocation = "/media/andrewhardy/9C33-6BBD/SYK_Yukawa/Data/"
fobj = open(inputfile, "r")
params = json.load(fobj)
fobj.close()
params["n_tau"] = 2 ** params["n_tau_power"] + 3
params["n_tau_D"] = 2 ** params["n_tau_D_power"] + 3

params["n_iw"] = 2 ** params["n_iw_power"] + 1
markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_']

betas = np.linspace(params["beta_min"], params["beta_max"], params["beta_length"])
betas_1 = np.linspace(5,50,10)
betas_2 = np.linspace(60, 140,9)
betas_3 = np.linspace(145, 200,12)

betas_1 = np.linspace(1,10,10)
betas_2 = np.linspace(10,60,11)
betas_3 = np.linspace(60, 150,10)

betas = np.concatenate((betas_1[:], betas_2[:],betas_3[:]))
betas = np.sort(betas)
beta = betas[0]
start = 0
end = 10
beta_start = 14
U_array = np.linspace(0,4,9)

inputname = f"04.15.2024_SYK_U-{U_array[4]:.1f}"

start = 0

end = 11
k_arr_1 = np.round(np.linspace(1.35, 1.45, end),4)# 11 U = 4.0
k_arr_1 = np.round(np.linspace(1.375, 1.475, end),4)# 11 U = 3.0
k_arr_1 = np.round(np.linspace(1.385, 1.485, end),4)# 11 U = 2.5
k_arr_1 = np.round(np.linspace(1.400, 1.500, end),4)# 11 U = 2.0
#k_arr_1 = np.round(np.linspace(1.415, 1.515, 11),4)# 11 U = 1.5
#k_arr_1 = np.round(np.linspace(1.425, 1.525, 11),4)# 11 U = 1.0
# k_arr_1 = np.round(np.linspace(1.435, 1.535, end),4)# 11 U = 0.5
# k_arr_1 = np.round(np.linspace(1.45, 1.55, 11),4)# 11 # U = 0

k_arr_2 = np.round(np.linspace(1.35, 1.45, end),4)# 11 U = 4.0
k_arr_2 = np.round(np.linspace(1.375, 1.475, end),4)# 11 U = 3.0
k_arr_2 = np.round(np.linspace(1.405, 1.415, end),4)# 11 U = 2.5
k_arr_2 = np.round(np.linspace(1.450, 1.460, end),4)# 11 U = 2.0
#k_arr_2 = np.round(np.linspace(1.48, 1.49, end),4)# 11 U = 1.5
#k_arr_2 = np.round(np.linspace(1.495, 1.505, 11),4)# 11 U = 1.0
# k_arr_2 = np.round(np.linspace(1.515, 1.525, end),4)# 11 U = 0.5
# k_arr_2 = np.round(np.linspace(1.525, 1.535, end),4)# 11 # U = 0


combined = np.concatenate((k_arr_1, k_arr_2))
#k_arr = k_arr_1
# # Keep only unique elements
k_arr = np.unique(combined)
k_arr = k_arr[:-4]

end = len(k_arr)


fig, ax = plt.subplots(1, figsize=(8, 8))
colorarr = np.linspace(0,1,2*end+2)
Tcolorarr = np.linspace(0,1,2*len(betas)+2)

ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
chubu = np.empty((len(betas), end)) # Chubukov test of Im(\Sigma) vs T. 
offsets = np.empty((len(betas), end))
constants = np.empty((len(betas), end))

wstar = np.empty((len(betas), end))
m_eff = np.empty((len(betas), end))
fit_param_eff = np.empty((len(betas), end, 4))
 

markers = ['^','d',  's',  'p', 'o', '+']
start = 0
#end = 15
inputname = "04.15.2024_SYK_U-2.0"
fig, ax = plt.subplots(1, figsize=(8, 8))
ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
axins = inset_axes(ax, width="45%", height="45%", loc='lower right',bbox_to_anchor=(0., 0.05, 1.0, 1.05), bbox_transform=ax.transAxes)
axins.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
axins.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
axins.tick_params(labelsize=10)
c = 0
j = 10 # test this
for i in range(start,end-1,3):

    known_name = inputname + f"_k-{k_arr[i]:.4f}_B-{150:.2f}"
    title = rf"$U$ - {params['U']:.2f}, $g^2$ - {params['g']:.2f},  $\beta$ - {150:.2f}"

    for filename in os.listdir(outlocation):
        #print(filename)
        if filename.startswith(known_name) and filename.endswith(".dat"):
            print(filename)
            savedata = np.loadtxt(os.path.join(outlocation, filename))
            pattern = r"M-\d+(?:\.\d+)?"
            match = re.search(pattern, filename)
            if match:
                number_str = match.group()
                try:
                    m_eff = float(number_str[2:])
                except ValueError:
                    m_eff = 1
            else:
                m_eff = 1
    idx = np.where(savedata[:,0] <= 1.3)

    fit_log = fitting(logmassfit , savedata[:,0][idx],-1*savedata[:,1][idx], guess = [0.4,4,0.1,1E-4])
    ax.plot(savedata[:,0][idx],-1*savedata[:,1][idx], markers[c], linewidth = 0.65, \
    markersize = 7,color = plt.cm.viridis(colorarr[2*(i+1)-1]), label = rf"$m^2$ = {np.round(m_eff,2):.2f} ")
    ax.legend(fontsize = 15)
    chubu[j,i] = -1*savedata[0,1]
    axins.plot(savedata[:,0][idx]*fit_log[2][0]*np.log(fit_log[2][1]/(savedata[:,0][idx]+fit_log[2][2]))+np.abs(fit_log[2][3]),-1*savedata[:,1][idx], markers[c], linewidth = 0.65, \
    markersize = 5,color = plt.cm.viridis(colorarr[2*(i+1)-1]), label = rf"$m^2$ = {np.round(m_eff,2):.2f} ")
    chubu[j,i] = -1*savedata[0,1]
    c += 1
axins.plot(np.linspace(0.0,0.6,100), np.linspace(0.0,0.6,100), linestyle = "dashed", color = "black")

#ax.set_title(title)
axins.set_ylabel(rf"-Im$\Sigma(i \omega_n) $", fontsize = 12)
axins.set_title(r"$ A \ \omega_n \log (B/(\omega_n+C))+D$", fontsize = 14)
ax.set_ylabel(rf"-Im$\Sigma(i \omega_n) $", fontsize =18)
ax.set_xlabel(r"$  \omega_n $", fontsize = 20)
axins.set_xlim(0.0,0.5)
axins.set_ylim(0.0,0.5)

plt.savefig(location+"SYK_yukawa/Plotting/Plots/"+inputname+"collapse.pdf",dpi=240, format = 'pdf')

plt.show() 
inputname = "02.15.2024_SYK_U-0.0"

outlocation = "/media/andrewhardy/9C33-6BBD/SYK_Yukawa/Data/"
inputfile = location + "SYK_yukawa/Input/" + inputname + ".json"

fobj = open(inputfile, "r")
params = json.load(fobj)
fobj.close()
df = pd.read_csv(outlocation + inputname+"_analysis.csv")