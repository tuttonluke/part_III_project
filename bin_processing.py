# convert .txt files to more efficient .nc files
# calculate Ice Nucleating Particle (INP) concentrations from Volcanic Ash Concentrations
# save data of individual size bins

import iris
import math
import numpy as np
import glob
import pandas as pd

# function to calculate INP concentration
def INP_calc(VAdiam, VAmass, Temp): 
    VApvol = (4/3) * math.pi * (VAdiam / 2)**3 # ash particle volume assuming sphere
    VApsa = (4) * math.pi * (VAdiam / 2)**2 * 2 # ash particle SA - multiplied by 2 assuming ash sphericity is actually 0.5
    VAvol = VAmass / 2300000 # ash volume (mass/density)
    VApnum = VAvol / VApvol # ash particle number
    ns = np.where((Temp >= -35) & (Temp <= -12.5), np.power(10, (0.2663 - 0.183 * Temp)) * np.power(10, 4), 0) # parameterisation of ice-nucleating activity of Icelandic ash/dust
    INP = (1 - np.exp(-ns * VApsa)) * VApnum
    return INP # INP concentration in units # / m^3

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

 # sorted lists of relevant .nc files
field_file_list = sorted(glob.glob('/shared/netscratch/jd876/Fields_grid82*'))
met_file_list = sorted(glob.glob('/shared/netscratch/jd876/Met_Data1*'))

# average mass of ash particles for each size bin
VAdiams = ((6.34 * 10**-7), (2.85 * 10**-6), (5.63 * 10**-6), (1.13 * 10**-5), (2.25 * 10**-5), (4.51 * 10**-5), (9.02 * 10**-5))
VAmasses = (3.07 * 10**-13, 2.77 * 10**-11, 2.15 * 10**-10, 1.72 * 10**-9, 1.37 * 10**-8, 1.1 * 10**-7, 8.83 * 10**-7) # volcanic ash average masses for particle size bins

# save individual files for ash number size bins
for i in range(1):
    
    files = [field_file_list[i], met_file_list[i]]
    cubes = iris.load(files)

    # we assume only 5% of ash mass remains airborne distally
    # convert to # / m^3 by dividing my average mass of particle
    # convert to # / L
    cubeVA0 = ((cubes[0] * 0.05) / VAmasses[0]) / 1000
    cubeVA1 = ((cubes[1] * 0.05) / VAmasses[1]) / 1000
    cubeVA2 = ((cubes[2] * 0.05) / VAmasses[2]) / 1000
    cubeVA3 = ((cubes[3] * 0.05) / VAmasses[3]) / 1000
    cubeVA4 = ((cubes[4] * 0.05) / VAmasses[4]) / 1000
    cubeVA5 = ((cubes[5] * 0.05) / VAmasses[5]) / 1000
    cubeVA6 = ((cubes[6] * 0.05) / VAmasses[6]) / 1000

    cube_list = [cubeVA0, cubeVA1, cubeVA2, cubeVA3, cubeVA4, cubeVA5, cubeVA6]
    
    for j in range(len(cube_list)):
        cube_list[j].rename('ASH NUMBER CONENRTATION')
        cube_list[j].units = '# / L'
        # save as .nc file
        iris.fileformats.netcdf.save(cube_list[j],'Bin' + str(j + 1) + 'ASHnumber' + field_file_list[i][-16:-4] + '.nc', netcdf_format='NETCDF4')
        
# repeat for INP number
for i in range(len(field_file_list)):
    
    cubeT = cubes[7] - 273.15
    Temp =  cubeT.data
    
    INP0 = INP_calc(VAdiams[0],VAmasses[0], Temp)
    INP1 = INP_calc(VAdiams[1],VAmasses[1], Temp)
    INP2 = INP_calc(VAdiams[2],VAmasses[2], Temp)
    INP3 = INP_calc(VAdiams[3],VAmasses[3], Temp)
    INP4 = INP_calc(VAdiams[4],VAmasses[4], Temp)
    INP5 = INP_calc(VAdiams[5],VAmasses[5], Temp)
    INP6 = INP_calc(VAdiams[6],VAmasses[6], Temp)
    
    cube_list = [INP0, INP1, INP2, INP3, INP4, INP5, INP6]
    
    for j in range(1):
        new_cube = cubeT.copy()
        new_cube.rename('INP NUMBER CONENRTATION')
        new_cube.units = '# / L'
        new_cube.data = cube_list[j]
        
        iris.fileformats.netcdf.save(new_cube, 'Bin' + str(j + 1) + 'INPnumber' + field_file_list[i][-16:-4] + '.nc', netcdf_format='NETCDF4')
        

  
  
