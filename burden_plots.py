# Calculate total mass and number burdens for ash/INP and plot as timeseries

import numpy as np
import iris
import netCDF4
import pandas as pd
import matplotlib.pyplot as plt
import os

# Import relevant files
ASH = '/scratch/lt446/netscratch/bin_sum_nc_files/ASHnc' # units ug / m^3
ASH_file = os.listdir(ASH)
ASH_file.sort()
ASH_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/ASHnc/'

ASHnumber = '/scratch/lt446/netscratch/bin_sum_nc_files/ASHnumbernc' # units # / L
ASHnumber_file = os.listdir(ASHnumber)
ASHnumber_file.sort()
ASHnumber_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/ASHnumbernc/'

INPnumber = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc' # units # / L
INPnumber_file = os.listdir(INPnumber)
INPnumber_file.sort()
INPnumber_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc/'

# calculate volumes of 'boxes' in the atmosphere
delta_alt = 500 # altitude bin size
delta_lat = 0.234375 # latitude bin size
R = 6378100.0 # radius of the Earth / m
delta_lat_metre = delta_lat * 2 * np.pi * R/360 # latitude bin size in metres

delta_lon = 0.3515625 # longitude bin size
delta_lon_metre = np.zeros(385) # empty array with the same dimension as latitude
delta_lon_metre[:] = delta_lon * 2 * np.pi * R * np.cos(lat[:] * np.pi / 180) / 360 # longitude bin sizes in metres

volume_array = np.zeros([24, 385, 1025]) # create an empty array with the same dimensions as INPcube
for i in range(len(volume_array[:, 0, 0])): # loop over altitude
    for j in range(len(volume_array[0,:,0])): # loop over latitude
        for k in range(len(volume_array[0, 0, :])): # loop over longitude
            volume_array[i, j, k]= delta_alt * delta_lat_metre * delta_lon_metre[j] # fill the array with gridbox volumes in m^3
            
# ASH mass burden calculations
mass_burden_time = np.zeros(len(ASH_file)) # create an array to store the mass burden for each timestep
time_array1 = np.zeros(len(ASH_file), dtype = 'datetime64[s]') # create an array to store each timestep

for i in range(len(ASH_file)):
    ASHcube = iris.load_cube(ASH_dir + ASH_file[i])
    ASHdata = ASHcube.data
    # get the time from each ASH .nc file and save it in the time_array
    nc_ASH_file = netCDF4.Dataset(ASH_dir + ASH_file[i])
    time = nc_ASH_file['time']
    time_data = time[:].data
    time_string = pd.to_datetime(time_data / 24, unit = 'D', origin = pd.Timestamp('1970-01-01')) # convert time to the proper format
    time_array1[i] = time_string # fill the time_array at the given index with the time
    # calculate the ash mass burden
    mass = volume_array * ASHdata/10**9 #10^9 is to convert back from ug we used earlier to kg
    mass_burden = np.sum(mass)
    mass_burden_time[i] = mass_burden # fill the mass_burden_time array at the given index with the mass burden
	  
# plot ash mass burden timeseries
fig, ax = plt.subplots(figsize = (8, 5))
ax.plot(time_array1, mass_burden_time / 10**9, '-o', color = 'k', lw = 1)
plt.setp(ax.get_xticklabels(), rotation = 30, ha = 'right', rotation_mode = 'anchor')
plt.xticks(['2010-04-14 06:00:00', '2010-04-18 00:00:00', '2010-04-21 12:00:00', '2010-04-25 00:00:00', '2010-04-28 12:00:00', '2010-05-02 00:00:00', '2010-05-05 12:00:00', '2010-05-09 00:00:00', '2010-05-12 12:00:00', '2010-05-16 00:00:00', '2010-05-19 12:00:00', '2010-05-23 00:00:00', '2010-05-26 12:00:00', '2010-05-30 00:00:00'])
# plt.tick_params(axis='x', which='major', labelsize=__)
ax.set_xlim(pd.to_datetime('2010-04-14 06:00'), pd.to_datetime('2010-05-30 00:00'))
ax.set_ylim(0, 3.5)
ax.grid()
ax.set_ylabel('Ash mass burden (Tg)', fontsize = 12) # add y-axis label
ax.set_xlabel('Time (YYYY-MM-DD)', fontsize = 12) # add x-axis label
ax.set_title('Total Ash Mass Burden from NAME Simulation of Eyjafjallajokull Eruption', fontsize = 13) # add title
plt.tight_layout()

fig.savefig('ASHmassburden.png')
plt.show()

# ASH number calculations
ASHnumber_burden_time = np.zeros(len(ASHnumber_file)) # create an array to store the mass burden for each timestep
time_array2 = np.zeros(len(ASHnumber_file), dtype = 'datetime64[s]') # create an array to store each timestep

for i in range(len(ASHnumber_file)):
    ASHcube = iris.load_cube(ASHnumber_dir + ASHnumber_file[i])
    ASHdata = ASHcube.data * 1000 # in # / m^3 
    ASHdata[np.isinf(ASHdata)] = np.nan
    # get the time from each ASHnumber.nc file and save it in the time_array
    nc_ASH_file = netCDF4.Dataset(ASHnumber_dir + ASHnumber_file[i])
    time = nc_ASH_file['time']
    time_data = time[:].data
    time_string = pd.to_datetime(time_data / 24, unit = 'D', origin = pd.Timestamp('1970-01-01')) # convert time to the proper format
    time_array2[i] = time_string # fill the time_array at the given index with the time
    # calculate the ash number burden
    number = (volume_array * ASHdata)
    number_burden = np.nansum(number)
    ASHnumber_burden_time[i] = number_burden # fill the ASHnumber_burden_time array at the given index with the mass burden
    
# Plot ASH number burden
fig, ax = plt.subplots(figsize = (8, 5))
ax.plot(time_array2, ASHnumber_burden_time / 10**22, '-o', color = 'k', lw = 1)
plt.setp(ax.get_xticklabels(), rotation = 30, ha = 'right', rotation_mode = 'anchor')
plt.xticks(['2010-04-14 06:00:00', '2010-04-18 00:00:00', '2010-04-21 12:00:00', '2010-04-25 00:00:00', '2010-04-28 12:00:00', '2010-05-02 00:00:00', '2010-05-05 12:00:00', '2010-05-09 00:00:00', '2010-05-12 12:00:00', '2010-05-16 00:00:00', '2010-05-19 12:00:00', '2010-05-23 00:00:00', '2010-05-26 12:00:00', '2010-05-30 00:00:00'])
# plt.tick_params(axis='x', which='major', labelsize=__)
ax.set_xlim(pd.to_datetime('2010-04-14 06:00'), pd.to_datetime('2010-05-30 00:00'))
ax.set_ylim(0, 40)
ax.grid()
ax.set_ylabel('Ash particle number burden x $10^{22}$', fontsize = 12) # add y-axis label
ax.set_xlabel('Time (MM-DD HH)', fontsize = 12) # add x-axis label
ax.set_title('Total Ash Number Burden from NAME Simulation of Eyjafjallajokull Eruption', fontsize = 13) # add title
plt.tight_layout()

fig.savefig('ASHmassburden.png')
plt.show()

# INP number burden calculations
INPnumber_burden_time = np.zeros(len(INPnumber_file)) # create an array to store the mass burden for each timestep
time_array3 = np.zeros(len(INPnumber_file), dtype = 'datetime64[s]') # create an array to store each timestep

for i in range(len(INPnumber_file)):
    INPcube = iris.load_cube(INPnumber_dir + INPnumber_file[i])
    INPdata = INPcube.data * 1000 # in # / m^3 
    INPdata[np.isinf(INPdata)] = np.nan
    # get the time from each INPnumber.nc file and save it in the time_array
    nc_INP_file = netCDF4.Dataset(INPnumber_dir + INPnumber_file[i])
    time = nc_INP_file['time']
    time_data = time[:].data
    time_string = pd.to_datetime(time_data / 24, unit = 'D', origin = pd.Timestamp('1970-01-01')) # convert time to the proper format
    time_array3[i] = time_string # fill the time_array at the given index with the time
    # calculate the INP number burden
    INPnumber = (volume_array * INPdata)
    INPnumber_burden = np.nansum(INPnumber)
    INPnumber_burden_time[i] = INPnumber_burden # fill the INPnumber_burden_time array at the given index with the mass burden

# Plot INP number burden
fig, ax = plt.subplots(figsize = (8, 5))
ax.plot(time_array3, INPnumber_burden_time / 10**20, '-o', color = 'k', lw = 1)
plt.setp(ax.get_xticklabels(), rotation = 30, ha = 'right', rotation_mode = 'anchor')
plt.xticks(['2010-04-14 06:00:00', '2010-04-18 00:00:00', '2010-04-21 12:00:00', '2010-04-25 00:00:00', '2010-04-28 12:00:00', '2010-05-02 00:00:00', '2010-05-05 12:00:00', '2010-05-09 00:00:00', '2010-05-12 12:00:00', '2010-05-16 00:00:00', '2010-05-19 12:00:00', '2010-05-23 00:00:00', '2010-05-26 12:00:00', '2010-05-30 00:00:00'])
# plt.tick_params(axis='x', which='major', labelsize=__)
ax.set_xlim(pd.to_datetime('2010-04-14 06:00'), pd.to_datetime('2010-05-30 00:00'))
ax.set_ylim(0, 40)
ax.grid()
ax.set_ylabel('Ash particle number burden x $10^{20}$', fontsize = 12) # add y-axis label
ax.set_xlabel('Time (YYYY-MM-DD)', fontsize = 12) # add x-axis label
ax.set_title('Total INP Number Burden from NAME Simulation of Eyjafjallajokull Eruption', fontsize = 13) # add title
plt.tight_layout()

fig.savefig('ASHmassburden.png')
plt.show()
