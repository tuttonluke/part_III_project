# plot cross sections of INP concentrations at a spectific longitude, as a function of altitude and latitude

import iris
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcols
import pandas as pd
import pylab

# create DataFrame from list for ease of sorting and naming files
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

INPnumber = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc' # units # / L
INPnumber_file = os.listdir(INPnumber)
INPnumber_file.sort()
INPnumber_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc/'

df = date_df(INP_file)

min_log_level = 0.001
max_log_level = 10000
cmap = 'PuBu' # colour scheme (blue)
norm = mcols.SymLogNorm(linthresh = min_log_level, vmin = 0, vmax = max_log_level) # logarithmic data normalisation
ccont_levels = [10**i for i in range(-3, 5)] # colour contour levels
cbar_ticks = [10** i for i in range(-3, 5)] # colour bar ticks

for i in range(len(INP_file)):
    title = df['date'][i]
    
    INPcube = iris.load_cube(INPnumber_dir + INPnumber_file[i])
    INPdata = INPcube.data
    
    alt = INPcube.coord('altitude').points
    lat = INPcube.coord('latitude').points
    # lon = TEMPcube.coord('longitude').points
    
    # plot INP concentration as a function of latitude and altitude at longitude 5 degrees west
    x1, y1 = np.meshgrid(lat, alt)
    
    fig = plt.figure(figsize = (10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Profile of airborne INP concentration at 5 $^\circ$ W' + str(title), pad = 20)
    ax.set_xlabel('Latitude ($^\circ$ N)', fontsize = 13)
    ax.set_ylabel('Altitude (m asl)', fontsize = 13)
    # plot data and colourbar 
    cs = ax.contourf(x1, y1, INPdata[:, :, 498], levels = ccont_levels, cmap = cmap, norm = norm, alpha = 0.9)
    plt.colorbar(cs, orientation = 'horizontal', ticks = cbar_ticks, label = ' # / L')
    plt.grid(axis='both') # plot grid
    pylab.xlim([30,90]) # define the x-axis limits
    
    # plt.show()
    # save image as .png file, with format 'INPcross5westYYYYMMDDHHHH.png'
    fig.savefig('INPcross5west' + df['name'][i] + '.png')
