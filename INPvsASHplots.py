# plot cross sections of average INP and ASH concentrations over longitude, as a function of altitude and latitude, with temperature contours

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

# Import source files
ASHnumber = '/scratch/lt446/netscratch/bin_sum_nc_files/ASHnumbernc' # units # / L
ASHnumber_file = os.listdir(ASHnumber)
ASHnumber_file.sort()
ASHnumber_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/ASHnumbernc/'

INPnumber = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc' # units # / L
INPnumber_file = os.listdir(INPnumber)
INPnumber_file.sort()
INPnumber_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc/'

TEMP = '/scratch/lt446/netscratch/bin_sum_nc_files/TEMPnc' # units C
TEMP_file = os.listdir(TEMP)
TEMP_file.sort()
TEMP_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/TEMPnc/'

df = date_df(INP_file)

min_log_level = 0.001
max_log_level = 10000
cmap = 'PuBu' # colour scheme (blue)
norm = mcols.SymLogNorm(linthresh = min_log_level, vmin = 0, vmax = max_log_level) # logarithmic data normalisation
ccont_levels = [10**i for i in range(-4, 5)] # colour contour levels
cbar_ticks = [10** i for i in range(-4, 5)] # colour bar ticks

# Plot With Temperature Contours

for i in range(len(INPnumber_file)):
    title = df['date'][i]
    
    INPcube = iris.load_cube(INPnumber_dir + INPnumber_file[i])
    INPdata = INPcube.data
    
    ASHcube = iris.load_cube(ASHnumber_dir + ASHnumber_file[i])
    ASHdata = ASHcube.data
    
    TEMPcube = iris.load_cube(TEMP_dir + TEMP_file[i])
    TEMPdata = TEMPcube.data
    
    TEMPcube_lonmean = TEMPcube.collapsed('longitude', iris.analysis.MEAN) # TEMPcube_lonmean is 2D [altitude, latitude]
    TEMPdata_lonmean = TEMPcube_lonmean.data
    
    alt = INPcube.coord('altitude').points
    lat = INPcube.coord('latitude').points
    # lon = TEMPcube.coord('longitude').points
    
    INPcube_longSUM = INPcube.collapsed('longitude', iris.analysis.MEAN)
    INPdata_longSUM = INPcube_longSUM.data
    
    ASHcube_longSUM = ASHcube.collapsed('longitude', iris.analysis.MEAN)
    ASHdata_longSUM = ASHcube_longSUM.data
    
    # plot INP concentration as a function of latitude and altitude at longitude 5 degrees west
    x1, y1 = np.meshgrid(lat, alt)
    
    fig = plt.figure(figsize = (10, 10))
    ax1 = fig.add_subplot(1, 2, 1)
    fig.suptitle('Plots of Volcanic Ash and INP concentrations ' + str(title), y = 0.95)
    ax1.set_title('Volcanic Ash')
    ax1.set_xlabel('Latitude ($^\circ$ N)', fontsize = 13)
    ax1.set_ylabel('Altitude (m asl)', fontsize = 13)
    # plot data and colourbar 
    cs = ax1.contourf(x1[:, :], y1[:, :], ASHdata_longSUM[:, :], levels = ccont_levels, cmap = cmap, norm = norm, alpha = 0.9)
    plt.colorbar(cs, orientation = 'horizontal', ticks = cbar_ticks, label = '# / L')
    # plt.grid(axis='both') # plot grid
    pylab.xlim([30,90]) # define the x-axis limits
    # plot temperature contours
    csTEMP = ax1.contour(x1, y1, TEMPdata_lonmean[:, :], cmap = 'Greys_r', levels = ccont_levels_temp, alpha = 0.7) # plot temperature contours
    plt.clabel(csTEMP, inline = 1, fontsize = 10, colors = 'black') # label temperature contours
    ax1.plot(lat[271], 370, 'k^', label = 'Eyja Volcano')
    
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_title('INP')
    ax2.set_xlabel('Latitude ($^\circ$ N)', fontsize = 13)
    # ax2.set_ylabel('Altitude (m asl)', fontsize = 13)
    # plot data and colourbar 
    cs = ax2.contourf(x1[:, :], y1[:, :], INPdata_longSUM[:, :], levels = ccont_levels, cmap = cmap, norm = norm, alpha = 0.9)
    plt.colorbar(cs, orientation = 'horizontal', ticks = cbar_ticks, label = '# / L')
    # plt.grid(axis='both') # plot grid
    pylab.xlim([30,90]) # define the x-axis limits
    csTEMP = ax2.contour(x1, y1, TEMPdata_lonmean[:, :], cmap = 'Greys_r', levels = ccont_levels_temp, alpha = 0.7) # plot temperature contours
    plt.clabel(csTEMP, inline = 1, fontsize = 10, colors = 'black') # label temperature contours
    ax2.plot(lat[271], 370, 'k^', label = 'Eyja Volcano')
    
    plt.show()
    # save image as .png file, with format 'INPcrossYYYYMMDDHHHH.png'
    # fig.savefig('INPvsASHcrossTEMP' + df['name'][i] + '.png')
