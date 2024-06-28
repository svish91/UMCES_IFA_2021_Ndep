import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from rasterio.windows import Window
from rasterio.transform import from_origin
import rasterio
import pydap.client
from osgeo import gdal
from PIL import Image
import fiona
import rasterio.plot
from descartes import PolygonPatch
from scipy.interpolate import interp1d
from f_interpolate_extrapolate_Zhou import f_interpolate_extrapolate_Zhou
import time
from skimage.transform import resize
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import seaborn as sns
from scipy.interpolate import griddata

############# these are preprocessing steps in for the
## reading emission data from text file
# summing NOx and NH3 Unit: tons
# using different approach
x_yr = 0
for yr in range(1997,2019):
    print(yr)
    # nh3
    file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_Emission Data\Upto 2018\NH3 gridded map\TOTALS_txt'
    df_NH3_tonsyr = pd.read_csv(os.path.join(file_dir, "EDGARv6.1_NH3_{0}_TOTALS.txt".format(yr)), sep = ";", skiprows = 2)
    # nox
    file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_Emission Data\Upto 2018\NOx gridded map\TOTALS_txt'
    df_NOx_tonsyr = pd.read_csv(os.path.join(file_dir, "EDGARv6.1_NOx_{0}_TOTALS.txt".format(yr)), sep = ";", skiprows = 2)
    # total
    int_df = pd.merge(df_NH3_tonsyr, df_NOx_tonsyr, how ='outer', on =['lat', 'lon'])
    int_df.loc[:,'total_{0}'.format(yr)] = int_df.loc[:,['emission {0} (tons)_x'.format(yr),'emission {0} (tons)_y'.format(yr)]].sum(axis=1, min_count=1)
    int_df = int_df.drop(columns=['emission {0} (tons)_x'.format(yr),'emission {0} (tons)_y'.format(yr)])
    if yr == 1997:#1997:
        int_df_m = int_df
    if yr > 1997:#1997:
        int_df_m = pd.merge(int_df_m, int_df, how ='outer', on =['lat', 'lon'])
    x_yr += 1

# create coord ranges over the desired raster extension
rRes = 0.1
xRange = np.arange(int_df_m.lon.min(), int_df_m.lon.max() + rRes, rRes)
yRange = np.arange(int_df_m.lat.min(), int_df_m.lat.max() + rRes, rRes)
# create arrays of x,y over the raster extension
gridX, gridY = np.meshgrid(xRange, yRange)
Total_emissions_tons = np.empty((len(np.arange(1997,2019)),len(yRange),len(xRange)))

x_yr = 0
for yr in range(1997, 2019):
    print(yr)
    # interpolate over the grid
    Total_emissions_tons[x_yr, :, :] = griddata(list(zip(int_df_m.lon, int_df_m.lat)),
                                                                    int_df_m['total_{0}'.format(yr)], (gridX, gridY), method='linear')
    x_yr += 1

# writing data to a text file
file_dir_tm = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Total_emissions_tonsyr'
x_yr = 0
for yr in range(1997,2019):# change 1997 to 1970 if want files from beginning
    with open(os.path.join('TM_tonsyr_{0}.txt'.format(yr)), 'w') as testfile:
        for row in Total_emissions_tons[x_yr,:,:]:
            testfile.write(' '.join([str(a) for a in row]) + '\n')
    x_yr += 1


# reading data and adjusting resolution
file_txt = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Total_emissions_tonsyr'
rRes = 0.1
#xRange = np.arange(int_df_m.lon.min(), int_df_m.lon.max() + rRes, rRes)
#yRange = np.arange(int_df_m.lat.min(), int_df_m.lat.max() + rRes, rRes)
xRange = np.arange(-180.0, 179.9 + rRes, rRes)
yRange = np.arange(-90.0, 89.9 + rRes, rRes)

idx_y = np.arange(0,1800,12.5)
idx_x = np.arange(0,3600,25)
data_txt_all_m = np.empty((22,143,144))
data_txt_all_m[:] = np.nan
x_yr = 0
for yr in np.arange(1997,2019):
    print(yr)
    data_txt_c = np.empty((1800, 144))
    data_txt = np.loadtxt(os.path.join(file_txt,'TM_tonsyr_{0}.txt'.format(yr)))

    # summing columns
    for ii_x in range(0,len(idx_x)):
        if ii_x == (len(idx_x)-1):
            break
        else:
            data_txt_c[:,ii_x] = np.nansum(data_txt[:,idx_x[ii_x]:idx_x[ii_x+1]], axis = 1)

    # summing rows
    data_txt_r = np.empty((144,144))
    data_txt_r[:] = np.nan

    for ii_y in range(0, len(idx_y)):
        idx_y_tmp = np.around(idx_y).astype(int)
        if ii_y == len(idx_y)-1:
            break
        else:
            if (ii_y % 2) == 1:
                data_hlv = 0.5*data_txt_c[idx_y_tmp[ii_y],:]
                # next slice
                data_txt_r[ii_y, :] = data_hlv + np.nansum(data_txt_c[(idx_y_tmp[ii_y]+1):idx_y_tmp[ii_y + 1],:], axis=0)
                # previous slice
                data_txt_r[ii_y-1, :] = data_hlv + np.nansum(data_txt_c[(idx_y_tmp[ii_y-1]):idx_y_tmp[ii_y],:], axis=0)

    # flipping upside down and left to right
    data_txt_all = np.fliplr(np.flip(data_txt_r))
    data_txt_all_m[x_yr,:,:] = np.delete(data_txt_all, obj = 0, axis = 0)
    x_yr += 1


# regressing N deposition on emission data
## reading deposition data
yrN = np.arange(1997,2014)
# for 2030 use this file name '2030_RCP45'
file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
Ndep_kgkm2yr = np.empty((17,143,144))

for i in range(0,len(yrN)):
    xx = gdal.Open(os.path.join(file_dir,'ndep_{0}.tif'.format(yrN[i])))
    Ndep_kgkm2yr[i,:,:] = np.array(xx.GetRasterBand(1).ReadAsArray())

# creating variable for extrapolation
Ndep_etrplt = np.empty((5,143,144))
Ndep_etrplt[:] = np.nan

for lat in range(0,143):
    for lon in range(0,144):
        if np.sum(np.isnan(data_txt_all_m[:17,lat,lon])) == 17:
            continue
        else:
            df_reg = pd.DataFrame({'TM':data_txt_all_m[:17,lat,lon],
                                   'Ndep': Ndep_kgkm2yr[:,lat,lon]},
                                  index=np.arange(1997,2014))
            df_reg_pred = pd.DataFrame({'TM':data_txt_all_m[17:,lat,lon]},
                                       index=np.arange(2014,2019))
            df_reg_pred_m = df_reg_pred.dropna(axis = 0, how = 'any')
            x = np.array(df_reg.iloc[:,0])
            x = x.reshape(-1,1)
            y = np.array(df_reg.iloc[:,1])
            y = y.reshape(-1,1)
            linreg = LinearRegression()
            linreg.fit(x,y)
            print(linreg.intercept_, linreg.coef_, linreg.score(x, y))
            Ndep_etrplt[:,lat,lon] = np.reshape(linreg.predict(df_reg_pred_m),(5))

#plotting after converting to ha: this is just a test
tmp = Ndep_etrplt/100
tmp[np.where(tmp<0)] = np.nan
plt.imshow(tmp[1,:,:])
plt.colorbar()

# writing the dataset
transform = from_origin(-178.75, 89.3706, 2.48263888888888884, 1.249938872316494809)

file_dir_ep = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
x_yr =  0
Ndep_etrplt[Ndep_etrplt<0] = np.nan
for yr in np.arange(2014,2019):
    outMatrix = Ndep_etrplt[x_yr,:,:]
    new_dataset = rasterio.open(os.path.join(file_dir_ep,"ndep_ep_{0}.tif".format(yr)), 'w',  driver='GTiff',height = outMatrix.shape[0], width = outMatrix.shape[1],
                            count=1, dtype=str(outMatrix.dtype),
                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                            transform=transform)

    new_dataset.write(outMatrix,1)
    new_dataset.close()
    x_yr += 1

# considering negative values also and not ignoring them like last attempt
x_yr =  0
for yr in np.arange(2014,2019):
    outMatrix = Ndep_etrplt[x_yr,:,:]
    new_dataset = rasterio.open(os.path.join(file_dir_ep,"ndep_ep_{0}_wNeg.tif".format(yr)), 'w',  driver='GTiff',height = outMatrix.shape[0], width = outMatrix.shape[1],
                            count=1, dtype=str(outMatrix.dtype),
                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                            transform=transform)

    new_dataset.write(outMatrix,1)
    new_dataset.close()
    x_yr += 1


#################### interpolating between decades
# reading data and adjusting resolution
file_txt = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Total_emissions_tonsyr'
rRes = 0.1
#xRange = np.arange(int_df_m.lon.min(), int_df_m.lon.max() + rRes, rRes)
#yRange = np.arange(int_df_m.lat.min(), int_df_m.lat.max() + rRes, rRes)
xRange = np.arange(-180.0, 179.9 + rRes, rRes)
yRange = np.arange(-90.0, 89.9 + rRes, rRes)

idx_y = np.arange(0,1800,12.5)
idx_x = np.arange(0,3600,25)
data_txt_all_m = np.empty((len(np.arange(1970,1998)),143,144))
data_txt_all_m[:] = np.nan
x_yr = 0
for yr in np.arange(1970,1998):
    print(yr)
    data_txt_c = np.empty((1800, 144))
    data_txt = np.loadtxt(os.path.join(file_txt,'TM_tonsyr_{0}.txt'.format(yr)))

    # summing columns
    for ii_x in range(0,len(idx_x)):
        if ii_x == (len(idx_x)-1):
            break
        else:
            data_txt_c[:,ii_x] = np.nansum(data_txt[:,idx_x[ii_x]:idx_x[ii_x+1]], axis = 1)

    # summing rows
    data_txt_r = np.empty((144,144))
    data_txt_r[:] = np.nan

    for ii_y in range(0, len(idx_y)):
        idx_y_tmp = np.around(idx_y).astype(int)
        if ii_y == len(idx_y)-1:
            break
        else:
            if (ii_y % 2) == 1:
                data_hlv = 0.5*data_txt_c[idx_y_tmp[ii_y],:]
                # next slice
                data_txt_r[ii_y, :] = data_hlv + np.nansum(data_txt_c[(idx_y_tmp[ii_y]+1):idx_y_tmp[ii_y + 1],:], axis=0)
                # previous slice
                data_txt_r[ii_y-1, :] = data_hlv + np.nansum(data_txt_c[(idx_y_tmp[ii_y-1]):idx_y_tmp[ii_y],:], axis=0)

    # flipping upside down and left to right
    data_txt_all = np.fliplr(np.flip(data_txt_r))
    data_txt_all_m[x_yr,:,:] = np.delete(data_txt_all, obj = 0, axis = 0)
    x_yr += 1


# regressing N deposition on emission data
## reading deposition data
yrN = [1970,1980,1990,1997]
# for 2030 use this file name '2030_RCP45'
file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
Ndep_kgkm2yr = np.empty((4,143,144))

for i in range(0,len(yrN)):
    xx = gdal.Open(os.path.join(file_dir,'ndep_{0}.tif'.format(yrN[i])))
    Ndep_kgkm2yr[i,:,:] = np.array(xx.GetRasterBand(1).ReadAsArray())

# creating variable for extrapolation
Ndep_etrplt = np.empty((27,143,144))
Ndep_etrplt[:] = np.nan

idx_emi = [0, 10, 20, 27]

for ii_emi in range(0,len(idx_emi)-1):
    #idx_dep = 0
    for lat in range(0,143):
        for lon in range(0,144):
            if np.sum(np.isnan(data_txt_all_m[[idx_emi[ii_emi],idx_emi[ii_emi+1]],lat,lon])) == 2:
               continue
            else:
                df_reg = pd.DataFrame({'TM':data_txt_all_m[[idx_emi[ii_emi],idx_emi[ii_emi+1]],lat,lon],
                                       'Ndep': Ndep_kgkm2yr[ii_emi:(ii_emi+2),lat,lon]},
                                      index=[yrN[ii_emi],yrN[ii_emi+1]])
                df_reg_pred = pd.DataFrame({'TM':data_txt_all_m[np.arange((idx_emi[ii_emi]+1),idx_emi[ii_emi+1]),lat,lon]},
                                           index=np.arange(yrN[ii_emi]+1,yrN[ii_emi+1]))
                df_reg_pred_m = df_reg_pred.dropna(axis = 0, how = 'any')
                x = np.array(df_reg.iloc[:,0])
                x = x.reshape(-1,1)
                y = np.array(df_reg.iloc[:,1])
                y = y.reshape(-1,1)
                linreg = LinearRegression()
                linreg.fit(x,y)
                print(linreg.intercept_, linreg.coef_, linreg.score(x, y))
                Ndep_etrplt[np.arange((idx_emi[ii_emi]+1),idx_emi[ii_emi+1]),lat,lon] = np.reshape(linreg.predict(df_reg_pred_m),(len(np.arange(yrN[ii_emi]+1,yrN[ii_emi+1]))))
    #idx_dep += 1



# considering negative values also and not ignoring them like last attempt
transform = from_origin(-178.75, 89.3706, 2.48263888888888884, 1.249938872316494809)

file_dir_ep = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period'
yrN = np.concatenate((np.arange(1971,1980), np.arange(1981,1990), np.arange(1991,1997)))
for yr in yrN:
    idx_yr = np.where(np.arange(1970,1997)==yr)
    outMatrix = Ndep_etrplt[idx_yr[0],:,:].reshape((143,144))
    new_dataset = rasterio.open(os.path.join(file_dir_ep,"ndep_ep_{0}_wNeg_interp.tif".format(yr)), 'w',  driver='GTiff',height = outMatrix.shape[0], width = outMatrix.shape[1],
                            count=1, dtype=str(outMatrix.dtype),
                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                            transform=transform)

    new_dataset.write(outMatrix,1)
    new_dataset.close()


# checking values
from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp

shapefile = gp.read_file(r"G:\My Drive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                             r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
# df_NOx_kgNha = pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NOx_kgNha = df_NOx_kgNha.rename(index = shapefile['CNTRY_NAME'])
# df_NHy_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NHy_kgNha = df_NHy_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_totNdep_kgNha= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=yrN)
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=yrN)
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])

for yr in yrN:
    print(yr)
    if yr > 2013:
        yrcr = 2015
    else:
        yrcr = yr
    file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period'
    file_name = "ndep_ep_{0}_wNeg_interp".format(yr)
    crfile_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2\For_Zhou\Modified'
    crfile_name = "Cropland_yr{0}_LUH_Zhou".format(yrcr)
    Ndep_tmp = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    # cropland
    df_cropland_km2[yr] = Ndep_tmp[1]
    # total
    df_totNdep_kgNha[yr] = Ndep_tmp[0]/100

df_totNdep_kgNha_trans = df_totNdep_kgNha.T
#df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission.csv") # use this if using non-negative values for aggregation
df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission_wNeg_ZhouLUH2_interpolated.csv")

(df_totNdep_kgNha < 0).any().any()



## between 1960 and 1970
yrN = [1960, 1970]
# for 2030 use this file name '2030_RCP45'
file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
Ndep_kgkm2yr = np.empty((2,143,144))

for i in range(0,len(yrN)):
    xx = gdal.Open(os.path.join(file_dir,'ndep_{0}.tif'.format(yrN[i])))
    Ndep_kgkm2yr[i,:,:] = np.array(xx.GetRasterBand(1).ReadAsArray())

# creating variable for extrapolation
Ndep_etrplt = np.empty((9,143,144))
Ndep_etrplt[:] = np.nan

for lat in range(0,143):
    for lon in range(0,144):
        #if np.sum(np.isnan(data_txt_all_m[[idx_emi[ii_emi],idx_emi[ii_emi+1]],lat,lon])) == 2:
        #   continue
        # else:
        df_reg = pd.DataFrame({'Yr':yrN,
                               'Ndep': Ndep_kgkm2yr[:,lat,lon]},
                              index=yrN)
        df_reg_pred = pd.DataFrame({'Yr':np.arange(1961,1970)},
                                   index=np.arange(1961,1970))
        df_reg_pred_m = df_reg_pred.dropna(axis = 0, how = 'any')
        x = np.array(df_reg.iloc[:,0])
        x = x.reshape(-1,1)
        y = np.array(df_reg.iloc[:,1])
        y = y.reshape(-1,1)
        linreg = LinearRegression()
        linreg.fit(x,y)
        print(linreg.intercept_, linreg.coef_, linreg.score(x, y))
        Ndep_etrplt[:,lat,lon] = np.reshape(linreg.predict(df_reg_pred_m),(Ndep_etrplt.shape[0]))

# considering negative values also and not ignoring them like last attempt
transform = from_origin(-178.75, 89.3706, 2.48263888888888884, 1.249938872316494809)

file_dir_ep = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period'
yrN = np.arange(1961,1970)
for yr in yrN:
    idx_yr = np.where(np.arange(1961,1970)==yr)
    outMatrix = Ndep_etrplt[idx_yr[0],:,:].reshape((143,144))
    new_dataset = rasterio.open(os.path.join(file_dir_ep,"ndep_ep_{0}_wNeg_interp.tif".format(yr)), 'w',  driver='GTiff',height = outMatrix.shape[0], width = outMatrix.shape[1],
                            count=1, dtype=str(outMatrix.dtype),
                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                            transform=transform)

    new_dataset.write(outMatrix,1)
    new_dataset.close()


from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp

shapefile = gp.read_file(r"G:\My Drive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                             r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
# df_NOx_kgNha = pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NOx_kgNha = df_NOx_kgNha.rename(index = shapefile['CNTRY_NAME'])
# df_NHy_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NHy_kgNha = df_NHy_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_totNdep_kgNha= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=yrN)
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=yrN)
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])

for yr in yrN:
    print(yr)
    if yr > 2013:
        yrcr = 2015
    else:
        yrcr = yr
    file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period'
    file_name = "ndep_ep_{0}_wNeg_interp".format(yr)
    crfile_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2\For_Zhou\Modified'
    crfile_name = "Cropland_yr{0}_LUH_Zhou".format(yrcr)
    Ndep_tmp = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    # cropland
    df_cropland_km2[yr] = Ndep_tmp[1]
    # total
    df_totNdep_kgNha[yr] = Ndep_tmp[0]/100

df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission_wNeg_ZhouLUH2_inter_1961_69.csv")

###### interpolating between 1970 - 1997 using a different approach to avoid negative values in the extimates
# reading data and adjusting resolution
file_txt = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Total_emissions_tonsyr'
rRes = 0.1
#xRange = np.arange(int_df_m.lon.min(), int_df_m.lon.max() + rRes, rRes)
#yRange = np.arange(int_df_m.lat.min(), int_df_m.lat.max() + rRes, rRes)
xRange = np.arange(-180.0, 179.9 + rRes, rRes)
yRange = np.arange(-90.0, 89.9 + rRes, rRes)

idx_y = np.arange(0,1800,12.5)
idx_x = np.arange(0,3600,25)
data_txt_all_m = np.empty((len(np.arange(1970,1998)),143,144))
data_txt_all_m[:] = np.nan
x_yr = 0
for yr in np.arange(1970,1998):
    print(yr)
    data_txt_c = np.empty((1800, 144))
    data_txt = np.loadtxt(os.path.join(file_txt,'TM_tonsyr_{0}.txt'.format(yr)))

    # summing columns
    for ii_x in range(0,len(idx_x)):
        if ii_x == (len(idx_x)-1):
            break
        else:
            data_txt_c[:,ii_x] = np.nansum(data_txt[:,idx_x[ii_x]:idx_x[ii_x+1]], axis = 1)

    # summing rows
    data_txt_r = np.empty((144,144))
    data_txt_r[:] = np.nan

    for ii_y in range(0, len(idx_y)):
        idx_y_tmp = np.around(idx_y).astype(int)
        if ii_y == len(idx_y)-1:
            break
        else:
            if (ii_y % 2) == 1:
                data_hlv = 0.5*data_txt_c[idx_y_tmp[ii_y],:]
                # next slice
                data_txt_r[ii_y, :] = data_hlv + np.nansum(data_txt_c[(idx_y_tmp[ii_y]+1):idx_y_tmp[ii_y + 1],:], axis=0)
                # previous slice
                data_txt_r[ii_y-1, :] = data_hlv + np.nansum(data_txt_c[(idx_y_tmp[ii_y-1]):idx_y_tmp[ii_y],:], axis=0)

    # flipping upside down and left to right
    data_txt_all = np.fliplr(np.flip(data_txt_r))
    data_txt_all_m[x_yr,:,:] = np.delete(data_txt_all, obj = 0, axis = 0)
    x_yr += 1

# regressing N deposition on emission data
## reading deposition data
yrN = [1970,1980,1990,1997]
# for 2030 use this file name '2030_RCP45'
file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
Ndep_kgkm2yr = np.empty((4,143,144))

for i in range(0,len(yrN)):
    xx = gdal.Open(os.path.join(file_dir,'ndep_{0}.tif'.format(yrN[i])))
    Ndep_kgkm2yr[i,:,:] = np.array(xx.GetRasterBand(1).ReadAsArray())

# creating variable for extrapolation
Ndep_etrplt = np.empty((27,143,144))
Ndep_etrplt[:] = np.nan

idx_emi = [0, 10, 20, 27]
idx_emi_pred = np.concatenate((np.arange(1,10), np.arange(11,20), np.arange(21,27)))
yrN_pred = np.concatenate((np.arange(1971,1980), np.arange(1981,1990), np.arange(1991,1997)))


for lat in range(0,143):
    for lon in range(0,144):
        if np.sum(np.isnan(data_txt_all_m[idx_emi,lat,lon])) == 4:
            continue
        else:
            df_reg = pd.DataFrame({'TM':data_txt_all_m[idx_emi,lat,lon],
                                   'Ndep': Ndep_kgkm2yr[:,lat,lon]},
                                  index=yrN)
            df_reg_pred = pd.DataFrame({'TM':data_txt_all_m[idx_emi_pred,lat,lon]},
                                       index=yrN_pred)
            df_reg_pred_m = df_reg_pred.dropna(axis = 0, how = 'any')
            x = np.array(df_reg.iloc[:,0])
            x = x.reshape(-1,1)
            y = np.array(df_reg.iloc[:,1])
            y = y.reshape(-1,1)
            linreg = LinearRegression()
            linreg.fit(x,y)
            print(linreg.intercept_, linreg.coef_, linreg.score(x, y))
            Ndep_etrplt[idx_emi_pred,lat,lon] = np.reshape(linreg.predict(df_reg_pred_m),(len(idx_emi_pred)))
#idx_dep += 1



# considering negative values also and not ignoring them like last attempt
transform = from_origin(-178.75, 89.3706, 2.48263888888888884, 1.249938872316494809)

file_dir_ep = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period_newApproach'
yrN = np.concatenate((np.arange(1971,1980), np.arange(1981,1990), np.arange(1991,1997)))
for yr in yrN:
    idx_yr = np.where(np.arange(1970,1997)==yr)
    outMatrix = Ndep_etrplt[idx_yr[0],:,:].reshape((143,144))
    new_dataset = rasterio.open(os.path.join(file_dir_ep,"ndep_ep_{0}_wNeg_interp_na.tif".format(yr)), 'w',  driver='GTiff',height = outMatrix.shape[0], width = outMatrix.shape[1],
                            count=1, dtype=str(outMatrix.dtype),
                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                            transform=transform)

    new_dataset.write(outMatrix,1)
    new_dataset.close()


# checking values
from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp

shapefile = gp.read_file(r"G:\My Drive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                             r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
# df_NOx_kgNha = pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NOx_kgNha = df_NOx_kgNha.rename(index = shapefile['CNTRY_NAME'])
# df_NHy_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NHy_kgNha = df_NHy_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_totNdep_kgNha= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=yrN_pred)
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=yrN_pred)
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])

for yr in yrN_pred:
    print(yr)
    if yr > 2013:
        yrcr = 2015
    else:
        yrcr = yr
    file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period_newApproach'
    file_name = "ndep_ep_{0}_wNeg_interp_na".format(yr)
    crfile_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2\For_Zhou\Modified'
    crfile_name = "Cropland_yr{0}_LUH_Zhou".format(yrcr)
    Ndep_tmp = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    # cropland
    df_cropland_km2[yr] = Ndep_tmp[1]
    # total
    df_totNdep_kgNha[yr] = Ndep_tmp[0]/100

df_totNdep_kgNha_trans = df_totNdep_kgNha.T
#df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission.csv") # use this if using non-negative values for aggregation
df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission_wNeg_ZhouLUH2_interpolated_na.csv")

(df_totNdep_kgNha < 0).any().any()