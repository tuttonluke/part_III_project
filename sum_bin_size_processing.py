# convert .txt files to more efficient .nc files
# calculate Ice Nucleating Particle (INP) concentrations from Volcanic Ash Concentrations
# sum all particle size bins for total concentration

import iris
import math
import numpy as np

text_dir = '*' # directory of source files

field_file = ['Fields_grid82_C1_T100_201005090600.txt', 'Fields_grid82_C1_T125_201005151200.txt', 'Fields_grid82_C1_T2_201004141800.txt', 'Fields_grid82_C1_T48_201004260600.txt', 'Fields_grid82_C1_T74_201005021800.txt', 'Fields_grid82_C1_T101_201005091200.txt', 'Fields_grid82_C1_T126_201005151800.txt', 'Fields_grid82_C1_T22_201004191800.txt', 'Fields_grid82_C1_T49_201004261200.txt', 'Fields_grid82_C1_T75_201005030000.txt', 'Fields_grid82_C1_T10_201004161800.txt', 'Fields_grid82_C1_T127_201005160000.txt', 'Fields_grid82_C1_T23_201004200000.txt', 'Fields_grid82_C1_T50_201004261800.txt', 'Fields_grid82_C1_T76_201005030600.txt', 'Fields_grid82_C1_T102_201005091800.txt', 'Fields_grid82_C1_T128_201005160600.txt', 'Fields_grid82_C1_T24_201004200600.txt', 'Fields_grid82_C1_T51_201004270000.txt', 'Fields_grid82_C1_T77_201005031200.txt', 'Fields_grid82_C1_T103_201005100000.txt', 'Fields_grid82_C1_T129_201005161200.txt', 'Fields_grid82_C1_T25_201004201200.txt', 'Fields_grid82_C1_T5_201004151200.txt', 'Fields_grid82_C1_T78_201005031800.txt', 'Fields_grid82_C1_T104_201005100600.txt', 'Fields_grid82_C1_T130_201005161800.txt', 'Fields_grid82_C1_T26_201004201800.txt', 'Fields_grid82_C1_T52_201004270600.txt', 'Fields_grid82_C1_T79_201005040000.txt', 'Fields_grid82_C1_T105_201005101200.txt', 'Fields_grid82_C1_T131_201005170000.txt', 'Fields_grid82_C1_T27_201004210000.txt', 'Fields_grid82_C1_T53_201004271200.txt', 'Fields_grid82_C1_T80_201005040600.txt', 'Fields_grid82_C1_T106_201005101800.txt', 'Fields_grid82_C1_T13_201004171200.txt', 'Fields_grid82_C1_T28_201004210600.txt', 'Fields_grid82_C1_T54_201004271800.txt', 'Fields_grid82_C1_T81_201005041200.txt', 'Fields_grid82_C1_T107_201005110000.txt', 'Fields_grid82_C1_T132_201005170600.txt', 'Fields_grid82_C1_T29_201004211200.txt', 'Fields_grid82_C1_T55_201004280000.txt', 'Fields_grid82_C1_T8_201004160600.txt', 'Fields_grid82_C1_T108_201005110600.txt', 'Fields_grid82_C1_T133_201005171200.txt', 'Fields_grid82_C1_T30_201004211800.txt', 'Fields_grid82_C1_T56_201004280600.txt', 'Fields_grid82_C1_T82_201005041800.txt', 'Fields_grid82_C1_T109_201005111200.txt', 'Fields_grid82_C1_T134_201005171800.txt', 'Fields_grid82_C1_T31_201004220000.txt', 'Fields_grid82_C1_T57_201004281200.txt', 'Fields_grid82_C1_T83_201005050000.txt', 'Fields_grid82_C1_T110_201005111800.txt', 'Fields_grid82_C1_T135_201005180000.txt', 'Fields_grid82_C1_T3_201004150000.txt', 'Fields_grid82_C1_T58_201004281800.txt', 'Fields_grid82_C1_T84_201005050600.txt', 'Fields_grid82_C1_T111_201005120000.txt', 'Fields_grid82_C1_T136_201005180600.txt', 'Fields_grid82_C1_T32_201004220600.txt', 'Fields_grid82_C1_T59_201004290000.txt', 'Fields_grid82_C1_T85_201005051200.txt', 'Fields_grid82_C1_T11_201004170000.txt', 'Fields_grid82_C1_T137_201005181200.txt', 'Fields_grid82_C1_T33_201004221200.txt', 'Fields_grid82_C1_T60_201004290600.txt', 'Fields_grid82_C1_T86_201005051800.txt', 'Fields_grid82_C1_T112_201005120600.txt', 'Fields_grid82_C1_T138_201005181800.txt', 'Fields_grid82_C1_T34_201004221800.txt', 'Fields_grid82_C1_T61_201004291200.txt', 'Fields_grid82_C1_T87_201005060000.txt', 'Fields_grid82_C1_T113_201005121200.txt', 'Fields_grid82_C1_T139_201005190000.txt', 'Fields_grid82_C1_T35_201004230000.txt', 'Fields_grid82_C1_T6_201004151800.txt', 'Fields_grid82_C1_T88_201005060600.txt', 'Fields_grid82_C1_T114_201005121800.txt', 'Fields_grid82_C1_T140_201005190600.txt', 'Fields_grid82_C1_T36_201004230600.txt', 'Fields_grid82_C1_T62_201004291800.txt', 'Fields_grid82_C1_T89_201005061200.txt', 'Fields_grid82_C1_T115_201005130000.txt', 'Fields_grid82_C1_T141_201005191200.txt', 'Fields_grid82_C1_T37_201004231200.txt', 'Fields_grid82_C1_T63_201004300000.txt', 'Fields_grid82_C1_T90_201005061800.txt', 'Fields_grid82_C1_T116_201005130600.txt', 'Fields_grid82_C1_T14_201004171800.txt', 'Fields_grid82_C1_T38_201004231800.txt', 'Fields_grid82_C1_T64_201004300600.txt', 'Fields_grid82_C1_T91_201005070000.txt', 'Fields_grid82_C1_T117_201005131200.txt', 'Fields_grid82_C1_T142_201005191800.txt', 'Fields_grid82_C1_T39_201004240000.txt', 'Fields_grid82_C1_T65_201004301200.txt', 'Fields_grid82_C1_T9_201004161200.txt', 'Fields_grid82_C1_T118_201005131800.txt', 'Fields_grid82_C1_T143_201005200000.txt', 'Fields_grid82_C1_T40_201004240600.txt', 'Fields_grid82_C1_T66_201004301800.txt', 'Fields_grid82_C1_T92_201005070600.txt', 'Fields_grid82_C1_T119_201005140000.txt', 'Fields_grid82_C1_T144_201005200600.txt', 'Fields_grid82_C1_T41_201004241200.txt', 'Fields_grid82_C1_T67_201005010000.txt', 'Fields_grid82_C1_T93_201005071200.txt', 'Fields_grid82_C1_T1_201004141200.txt', 'Fields_grid82_C1_T15_201004180000.txt', 'Fields_grid82_C1_T4_201004150600.txt', 'Fields_grid82_C1_T68_201005010600.txt', 'Fields_grid82_C1_T94_201005071800.txt', 'Fields_grid82_C1_T120_201005140600.txt', 'Fields_grid82_C1_T16_201004180600.txt', 'Fields_grid82_C1_T42_201004241800.txt', 'Fields_grid82_C1_T69_201005011200.txt', 'Fields_grid82_C1_T95_201005080000.txt', 'Fields_grid82_C1_T121_201005141200.txt', 'Fields_grid82_C1_T17_201004181200.txt', 'Fields_grid82_C1_T43_201004250000.txt', 'Fields_grid82_C1_T70_201005011800.txt', 'Fields_grid82_C1_T96_201005080600.txt', 'Fields_grid82_C1_T12_201004170600.txt', 'Fields_grid82_C1_T18_201004181800.txt', 'Fields_grid82_C1_T44_201004250600.txt', 'Fields_grid82_C1_T71_201005020000.txt', 'Fields_grid82_C1_T97_201005081200.txt', 'Fields_grid82_C1_T122_201005141800.txt', 'Fields_grid82_C1_T19_201004190000.txt', 'Fields_grid82_C1_T45_201004251200.txt', 'Fields_grid82_C1_T7_201004160000.txt', 'Fields_grid82_C1_T98_201005081800.txt', 'Fields_grid82_C1_T123_201005150000.txt', 'Fields_grid82_C1_T20_201004190600.txt', 'Fields_grid82_C1_T46_201004251800.txt', 'Fields_grid82_C1_T72_201005020600.txt', 'Fields_grid82_C1_T99_201005090000.txt', 'Fields_grid82_C1_T124_201005150600.txt', 'Fields_grid82_C1_T21_201004191200.txt', 'Fields_grid82_C1_T47_201004260000.txt', 'Fields_grid82_C1_T73_201005021200.txt']
met1_file = ['Met_Data1_C1_T100_201005090600.txt', 'Met_Data1_C1_T121_201005141200.txt', 'Met_Data1_C1_T142_201005191800.txt', 'Met_Data1_C1_T34_201004221800.txt', 'Met_Data1_C1_T56_201004280600.txt', 'Met_Data1_C1_T78_201005031800.txt', 'Met_Data1_C1_T101_201005091200.txt', 'Met_Data1_C1_T12_201004170600.txt', 'Met_Data1_C1_T143_201005200000.txt', 'Met_Data1_C1_T35_201004230000.txt', 'Met_Data1_C1_T57_201004281200.txt', 'Met_Data1_C1_T79_201005040000.txt', 'Met_Data1_C1_T10_201004161800.txt', 'Met_Data1_C1_T122_201005141800.txt', 'Met_Data1_C1_T144_201005200600.txt', 'Met_Data1_C1_T36_201004230600.txt', 'Met_Data1_C1_T58_201004281800.txt', 'Met_Data1_C1_T80_201005040600.txt', 'Met_Data1_C1_T102_201005091800.txt', 'Met_Data1_C1_T123_201005150000.txt', 'Met_Data1_C1_T15_201004180000.txt', 'Met_Data1_C1_T37_201004231200.txt', 'Met_Data1_C1_T59_201004290000.txt', 'Met_Data1_C1_T81_201005041200.txt', 'Met_Data1_C1_T103_201005100000.txt', 'Met_Data1_C1_T124_201005150600.txt', 'Met_Data1_C1_T16_201004180600.txt', 'Met_Data1_C1_T38_201004231800.txt', 'Met_Data1_C1_T60_201004290600.txt', 'Met_Data1_C1_T8_201004160600.txt', 'Met_Data1_C1_T104_201005100600.txt', 'Met_Data1_C1_T125_201005151200.txt', 'Met_Data1_C1_T17_201004181200.txt', 'Met_Data1_C1_T39_201004240000.txt', 'Met_Data1_C1_T61_201004291200.txt', 'Met_Data1_C1_T82_201005041800.txt', 'Met_Data1_C1_T105_201005101200.txt', 'Met_Data1_C1_T126_201005151800.txt', 'Met_Data1_C1_T18_201004181800.txt', 'Met_Data1_C1_T40_201004240600.txt', 'Met_Data1_C1_T6_201004151800.txt', 'Met_Data1_C1_T83_201005050000.txt', 'Met_Data1_C1_T106_201005101800.txt', 'Met_Data1_C1_T127_201005160000.txt', 'Met_Data1_C1_T19_201004190000.txt', 'Met_Data1_C1_T41_201004241200.txt', 'Met_Data1_C1_T62_201004291800.txt', 'Met_Data1_C1_T84_201005050600.txt', 'Met_Data1_C1_T107_201005110000.txt', 'Met_Data1_C1_T128_201005160600.txt', 'Met_Data1_C1_T20_201004190600.txt', 'Met_Data1_C1_T4_201004150600.txt', 'Met_Data1_C1_T63_201004300000.txt', 'Met_Data1_C1_T85_201005051200.txt', 'Met_Data1_C1_T108_201005110600.txt', 'Met_Data1_C1_T129_201005161200.txt', 'Met_Data1_C1_T21_201004191200.txt', 'Met_Data1_C1_T42_201004241800.txt', 'Met_Data1_C1_T64_201004300600.txt', 'Met_Data1_C1_T86_201005051800.txt', 'Met_Data1_C1_T109_201005111200.txt', 'Met_Data1_C1_T130_201005161800.txt', 'Met_Data1_C1_T2_201004141800.txt', 'Met_Data1_C1_T43_201004250000.txt', 'Met_Data1_C1_T65_201004301200.txt', 'Met_Data1_C1_T87_201005060000.txt', 'Met_Data1_C1_T110_201005111800.txt', 'Met_Data1_C1_T131_201005170000.txt', 'Met_Data1_C1_T22_201004191800.txt', 'Met_Data1_C1_T44_201004250600.txt', 'Met_Data1_C1_T66_201004301800.txt', 'Met_Data1_C1_T88_201005060600.txt', 'Met_Data1_C1_T111_201005120000.txt', 'Met_Data1_C1_T13_201004171200.txt', 'Met_Data1_C1_T23_201004200000.txt', 'Met_Data1_C1_T45_201004251200.txt', 'Met_Data1_C1_T67_201005010000.txt', 'Met_Data1_C1_T89_201005061200.txt', 'Met_Data1_C1_T11_201004170000.txt', 'Met_Data1_C1_T132_201005170600.txt', 'Met_Data1_C1_T24_201004200600.txt', 'Met_Data1_C1_T46_201004251800.txt', 'Met_Data1_C1_T68_201005010600.txt', 'Met_Data1_C1_T90_201005061800.txt', 'Met_Data1_C1_T112_201005120600.txt', 'Met_Data1_C1_T133_201005171200.txt', 'Met_Data1_C1_T25_201004201200.txt', 'Met_Data1_C1_T47_201004260000.txt', 'Met_Data1_C1_T69_201005011200.txt', 'Met_Data1_C1_T91_201005070000.txt', 'Met_Data1_C1_T113_201005121200.txt', 'Met_Data1_C1_T134_201005171800.txt', 'Met_Data1_C1_T26_201004201800.txt', 'Met_Data1_C1_T48_201004260600.txt', 'Met_Data1_C1_T70_201005011800.txt', 'Met_Data1_C1_T9_201004161200.txt', 'Met_Data1_C1_T114_201005121800.txt', 'Met_Data1_C1_T135_201005180000.txt', 'Met_Data1_C1_T27_201004210000.txt', 'Met_Data1_C1_T49_201004261200.txt', 'Met_Data1_C1_T71_201005020000.txt', 'Met_Data1_C1_T92_201005070600.txt', 'Met_Data1_C1_T115_201005130000.txt', 'Met_Data1_C1_T136_201005180600.txt', 'Met_Data1_C1_T28_201004210600.txt', 'Met_Data1_C1_T50_201004261800.txt', 'Met_Data1_C1_T7_201004160000.txt', 'Met_Data1_C1_T93_201005071200.txt', 'Met_Data1_C1_T116_201005130600.txt', 'Met_Data1_C1_T137_201005181200.txt', 'Met_Data1_C1_T29_201004211200.txt', 'Met_Data1_C1_T51_201004270000.txt', 'Met_Data1_C1_T72_201005020600.txt', 'Met_Data1_C1_T94_201005071800.txt', 'Met_Data1_C1_T117_201005131200.txt', 'Met_Data1_C1_T138_201005181800.txt', 'Met_Data1_C1_T30_201004211800.txt', 'Met_Data1_C1_T5_201004151200.txt', 'Met_Data1_C1_T73_201005021200.txt', 'Met_Data1_C1_T95_201005080000.txt', 'Met_Data1_C1_T118_201005131800.txt', 'Met_Data1_C1_T139_201005190000.txt', 'Met_Data1_C1_T31_201004220000.txt', 'Met_Data1_C1_T52_201004270600.txt', 'Met_Data1_C1_T74_201005021800.txt', 'Met_Data1_C1_T96_201005080600.txt', 'Met_Data1_C1_T119_201005140000.txt', 'Met_Data1_C1_T140_201005190600.txt', 'Met_Data1_C1_T3_201004150000.txt', 'Met_Data1_C1_T53_201004271200.txt', 'Met_Data1_C1_T75_201005030000.txt', 'Met_Data1_C1_T97_201005081200.txt', 'Met_Data1_C1_T1_201004141200.txt', 'Met_Data1_C1_T141_201005191200.txt', 'Met_Data1_C1_T32_201004220600.txt', 'Met_Data1_C1_T54_201004271800.txt', 'Met_Data1_C1_T76_201005030600.txt', 'Met_Data1_C1_T98_201005081800.txt', 'Met_Data1_C1_T120_201005140600.txt', 'Met_Data1_C1_T14_201004171800.txt', 'Met_Data1_C1_T33_201004221200.txt', 'Met_Data1_C1_T55_201004280000.txt', 'Met_Data1_C1_T77_201005031200.txt', 'Met_Data1_C1_T99_201005090000.txt']

fields_with_dir = []
met_with_dir = []

# add the shared directory string to file names
for i in range(len(field_file)):
    fields_with_dir.append(text_dir + field_file[i])
    met_with_dir.append(text_dir + met1_file[i])
    
for i in range(len(fields_with_dir)):

    file_names = [fields_with_dir[i], met_with_dir[i]]
    cubes = iris.load(file_names) 

    cubeVA0 = cubes[0] * 0.05 # we assume only 5% of ash mass remains airborne distally
    cubeVA1 = cubes[1] * 0.05
    cubeVA2 = cubes[2] * 0.05
    cubeVA3 = cubes[3] * 0.05
    cubeVA4 = cubes[4] * 0.05
    cubeVA5 = cubes[5] * 0.05
    cubeVA6 = cubes[6] * 0.05

    ashtotcube = (cubeVA0 + cubeVA1 + cubeVA2 + cubeVA3 + cubeVA4 + cubeVA5 + cubeVA6) * 1000000 # sum particle size bins and convert to ug / m^3
    ashtotcube.rename('ASH CONCENTRATION')
    ashtotcube.units = 'ug / m^3'

    iris.fileformats.netcdf.save(ashtotcube, 'ASH' + field_file[i][-16:-4] + '.nc', netcdf_format='NETCDF4')

    cubeT = cubes[7] - 273.15 # convert Kelvin to Celsius
    cubeT.rename('TEMPERTAURE')
    cubeT.units = 'Celsius'

    iris.fileformats.netcdf.save(cubeT,'TEMP' + met1_file[i][-16:-4] + '.nc', netcdf_format='NETCDF4')

    VAdiams = ((6.34 * 10**-7), (2.85 * 10**-6), (5.63 * 10**-6), (1.13 * 10**-5), (2.25 * 10**-5), (4.51 * 10**-5), (9.02 * 10**-5))
    VAmasses = (cubeVA0.data, cubeVA1.data, cubeVA2.data, cubeVA3.data, cubeVA4.data, cubeVA5.data, cubeVA6.data)
    
    # calculate INP concentration
    def INP_calc(VAdiam, VAmass): 
        VApvol = (4/3) * math.pi * (VAdiam / 2)**3 # ash particle volume assuming sphere
        VApsa = (4) * math.pi * (VAdiam / 2)**2 * 2 # ash particle SA - multiplied by 2 assuming ash sphericity is actually 0.5
        VAvol = VAmass / 2300000 # ash volume (mass/density)
        VApnum = VAvol / VApvol # ash particle number
        T =  cubeT.data
        ns = np.where((T >= -35) & (T <= -12.5), np.power(10, (0.2663 - 0.183 * T)) * np.power(10, 4), 0) # parameterisation of ice-nucleating activity of Icelandic ash/dust
        INP = (1 - np.exp(-ns * VApsa)) * VApnum
        return INP # INP concentration in units # / m^3
   
    INP0 = INP_calc(VAdiams[0],VAmasses[0]) 
    INP1 = INP_calc(VAdiams[1],VAmasses[1])
    INP2 = INP_calc(VAdiams[2],VAmasses[2])
    INP3 = INP_calc(VAdiams[3],VAmasses[3])
    INP4 = INP_calc(VAdiams[4],VAmasses[4])
    INP5 = INP_calc(VAdiams[5],VAmasses[5])
    INP6 = INP_calc(VAdiams[6],VAmasses[6])

    INPtot = (INP0 + INP1 + INP2 + INP3 + INP4 + INP5 + INP6)/1000 # sum particle size bins and convert from #/m^3 to #/L
    INPtotcube = cubeT.copy() 
    INPtotcube.rename('INP CONCENTRATION')
    INPtotcube.units = '# / L'
    INPtotcube.data = INPtot

    iris.fileformats.netcdf.save(INPtotcube,'INP' + field_file[i][-16:-4] + '.nc', netcdf_format='NETCDF4')
