# plot cross section of air temperature averaged over all longtiude data, as a function of altitude and latitude

import iris
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# create dataframe for ease of sorting and naming files
def date_df(lst):
    
    time_list = []
    name_list = []
    for i in range(len(lst)):
        time_list.append(lst[i][-15:-3])
    for i in lst:
        name_list.append(i[-15:-3])
    df = pd.DataFrame({'date' : time_list, 'name' : name_list})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by = 'date')
    df['sorted_index'] = [i for i in range(len(time_list))]
    return df

TEMP = '/scratch/lt446/netscratch/bin_sum_nc_files/TEMPnc'
TEMP_file = os.listdir(TEMP)
TEMP_file.sort()
TEMP_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/TEMPnc/'

# sort files by date 
df = date_df(TEMP_file)

ccont_levels = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30] # colour bar parameters
cbar_ticks = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30]

for i in range(len(TEMP_file)):
    title = df['date'][i]
    
    TEMPcube = iris.load_cube(TEMP_dir + TEMP_file[i])
    TEMPdata = TEMPcube.data
    
    TEMPcube_lonmean = TEMPcube.collapsed('longitude', iris.analysis.MEAN) # TEMPcube_lonmean is 2D [altitude, latitude]
    TEMPdata_lonmean = TEMPcube_lonmean.data
    
    alt = TEMPcube.coord('altitude').points
    lat = TEMPcube.coord('latitude').points
    lon = TEMPcube.coord('longitude').points
    
    # plot air temperature averaged over longitude as a function of latitude and altitude
    x1, y1 = np.meshgrid(lat, alt)
    
    fig, ax = plt.subplots()
    ax.set_title('Air Temperature Altitude / Latitude Cross Section - ' + str(title), pad = 20)
    ax.set_xlabel('Latitude ($^\circ$ N)')
    ax.set_ylabel('Altitude (m asl)')
    cs = ax.contourf(x1, y1, TEMPdata_lonmean[:, :], cmap = 'RdBu_r', levels = ccont_levels)
    plt.colorbar(cs, ticks = cbar_ticks, label = 'Temperature ($^\circ$ C)')
    ax.plot(lat[271], 370, 'k^', label = 'Eyja Volcano')
    
    # plt.show()
    # save image as .png file, with format 'TEMPCROSSYYYYMMDDHHHH.png'
    fig.savefig('TEMPcross' + df['name'][i] + '.png')
