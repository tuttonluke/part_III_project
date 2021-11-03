# plot average INP concentrations, summed over entire vertical column, on a North Polar Stereo projection map 

import iris
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcols
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd

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

INPnumber = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc'
INPnumber_file = os.listdir(INPnumber)
INPnumber_file.sort()
INPnumber_dir = '/scratch/lt446/netscratch/bin_sum_nc_files/INPnc/'

df = date_df(INP_file)

minimum_log_level = 0.001
maximum_log_level = 10000
cmap = 'PuBu' #  color scheme, see https://matplotlib.org/stable/tutorials/colors/colormaps.html 
norm = mcols.SymLogNorm(linthresh = minimum_log_level, vmin = 0, vmax = maximum_log_level) # create a logarithmic data normalization
ccont_levels = [10**i for i in range(-3, 5)] # colour contour levels
cbar_ticks = [10** i for i in range(-3, 5)] # colour bar ticks

# plot data using North Polar Stereo Projection
for i in range(1):
    title = df['date'][i]
    
    INPcube = iris.load_cube(INPnumber_dir + INPnumber_file[i])
    INPdata = INPcube.data
    
    lat = INPcube[:, :383, :].coord('latitude').points # remove latitude = 0 data point (bug fix)
    lon = INPcube.coord('longitude').points
    
    # collapse data over altitude (mean concentration over entire vertical column)
    INPcube_altmean = INPcube[:, :383, :].collapsed('altitude', iris.analysis.MEAN)
    INPdata_altmean = INPcube_altmean.data
    
    x1, y1 = np.meshgrid(lon, lat)
    
    fig = plt.figure(figsize = (10, 10))
    ax = fig.add_subplot(1, 1, 1, projection = ccrs.NorthPolarStereo()) # https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html
    ax.patch.set_visible(False)
    extent = [-6600000, 6600000, -7000000, 7000000] # size of domain plotted
    ax.set_extent(extent, ccrs.NorthPolarStereo())
    ax.gridlines()
    ax.coastlines(resolution = '50m')
    ax.add_feature(cfeature.LAND.with_scale('50m'))
    ax.set_title('Mean INP Air Concentration Over Entire Vertical Column - ' + str(title), fontsize = 14, pad = 20)
    cs = ax.contourf(x1[:, :], y1[:, :], INPdata_altmean[:, :], levels = ccont_levels, transform = ccrs.PlateCarree(), cmap = cmap, norm = norm)
    plt.colorbar(cs, orientation = 'horizontal', ticks = cbar_ticks, label = '# / L', pad = 0.05, shrink = 0.7)
    
    plt.show()
    # save plots as .png files
    # fig.savefig('mean_INP' + df['name'][i] + '.png')
