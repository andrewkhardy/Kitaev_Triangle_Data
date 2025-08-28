import h5py
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
# Load the HDF5 file
filename = "gap_chi_analysis.h5"
plt.style.use("lake.mplstyle")
plt.rcParams.update({"text.usetex": True})

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Computer Modern Roman"] + plt.rcParams["font.serif"]
plt.rcParams.update({"text.usetex": True})
with h5py.File(filename, 'r') as file:
    # Load original data
    delta_data = file['original_data/delta'][()]
    gap_data = file['original_data/gap'][()]
    chi_data = file['original_data/chi'][()]
    
    # Load fitted curves
    delta_fit = file['fitted_curves/delta'][()]
    gap_fit = file['fitted_curves/gap_fit'][()]
    chi_fit = file['fitted_curves/chi_fit'][()]
    
    # Load fit parameters
    gap_slope = file['fit_parameters/gap_slope'][()]
    gap_intercept = file['fit_parameters/gap_intercept'][()]
    chi_coefficient = file['fit_parameters/chi_coefficient'][()]
    chi_offset = file['fit_parameters/chi_offset'][()]
    
    # Load R-squared values
    gap_r2 = file['fit_statistics/gap_r_squared'][()]
    chi_r2 = file['fit_statistics/chi_r_squared'][()]
    
    # Load metadata
    original_filename = file['metadata/filename'][()].decode('utf-8')
    fit_range = file['metadata/fit_range'][()].decode('utf-8')

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Gap vs Delta
ax1.plot(delta_data, gap_data, 'o', markersize=8, label='Data', color='blue')
ax1.plot(delta_fit, gap_fit, '--', linewidth=2, color='red', 
         label=f'Linear fit: {gap_slope:.3f}δ + {gap_intercept:.3f}')
ax1.set_xlabel(r'$\gamma$', fontsize=24)
ax1.set_ylabel(r'$\epsilon_1$', fontsize=24, rotation=0, labelpad=20)
ax1.set_xlim(0.0, 0.2)
ax1.set_ylim(0.0, 0.4)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax1.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax2.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax2.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
# Plot 2: Chi vs Delta
ax2.plot(delta_data, 1/chi_data, 'o', markersize=8, label='Data', color='blue')
ax2.plot(delta_fit, chi_fit, '--', linewidth=2, color='red',
         label=f'Inverse fit: {chi_coefficient:.3f}/δ + {chi_offset:.3f}')
ax2.set_xlabel(r'$\gamma$', fontsize=28)
ax2.set_ylabel(r'$1/\xi$', fontsize=28, rotation=0, labelpad=20)
ax2.set_xlim(0.0, 0.2)
ax2.set_ylim(0.0, 0.6)
ax2.grid(True, alpha=0.3)

# Add overall title

# Adjust layout and save
plt.tight_layout()
plt.savefig('scaling.pdf', format='pdf', bbox_inches='tight')
plt.show()

# Print summary
print(f"Original filename: {original_filename}")
print(f"Fit range: {fit_range}")
print(f"Gap fit: slope = {gap_slope:.4f}, intercept = {gap_intercept:.4f}, R² = {gap_r2:.4f}")
print(f"Chi fit: coefficient = {chi_coefficient:.4f}, offset = {chi_offset:.4f}, R² = {chi_r2:.4f}")




# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Gap vs Delta
ax1.plot(delta_data, 1/gap_data, 'o', markersize=8, label='Data', color='blue')
ax1.plot(delta_data, chi_data, 'o', markersize=8, label='Data', color='blue')

ax1.set_xlabel(r'$\gamma$', fontsize=24)
ax1.set_ylabel(r'$1/\epsilon_1$', fontsize=24, rotation=0, labelpad=20)
ax1.set_xlim(0.0, 0.2)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax1.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax2.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
ax2.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(2))
# Plot 2: Chi vs Delta
ax2.plot(delta_data, 1/chi_data, 'o', markersize=8, label='Data', color='blue')
ax2.plot(delta_fit, 0.1*delta_fit, '--')
ax2.set_xlabel(r'$\gamma$', fontsize=28)
ax2.set_ylabel(r'$1/\xi$', fontsize=28, rotation=0, labelpad=20)
ax2.set_xlim(0.0, 0.2)
ax2.set_ylim(0.0, 0.6)
ax2.grid(True, alpha=0.3)

# Add overall title

# Adjust layout and save
plt.tight_layout()
plt.show()

# Print summary
print(f"Original filename: {original_filename}")
print(f"Fit range: {fit_range}")
print(f"Gap fit: slope = {gap_slope:.4f}, intercept = {gap_intercept:.4f}, R² = {gap_r2:.4f}")
print(f"Chi fit: coefficient = {chi_coefficient:.4f}, offset = {chi_offset:.4f}, R² = {chi_r2:.4f}")