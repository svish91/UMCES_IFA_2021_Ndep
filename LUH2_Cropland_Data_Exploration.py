import netCDF4 as nc
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
#from f_changingResolution import f_changingResolution
#from f_aggDataSimple import f_aggDataSimple
from rasterio.windows import Window
from rasterio.transform import from_origin
from skimage.transform import resize
import rasterio
from PIL import Image
import json
import pandas as pd

fpath = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Cropland_area\UofMD-landState-2-1-h'
Crplnd_mat = nc.Dataset(os.path.join(fpath,'states.nc'))
Crplnd_mat.variables.keys()
#(['time', 'lat', 'lon', 'primf', 'primn', 'secdf', 'secdn', 'urban', 'c3ann', 'c4ann', 'c3per', 'c4per', 'c3nfx', 'pastr', 'range', 'secmb', 'secma', 'lat_bounds', 'lon_bounds'])
# temporal scale: 0850-2015; grid size = (720, 1440)

# combining: 'c3ann', 'c4ann', 'c3per', 'c4per', 'c3nfx',
fval = 1.e+20 # fill value
yrs_to_consider = np.arange(1961,2019,1)
yrs_avail = np.arange(850,2016,1)
idx_yrs_to_consider = np.zeros(yrs_to_consider.shape)
for i in range(0,len(yrs_to_consider)):
    if yrs_to_consider[i] == 2016:
        break
    idx_yrs_to_consider[i]=np.where(yrs_avail== yrs_to_consider[i])[0]

#idx_yrs_to_consider = idx_yrs_to_consider.astype('int')


Crplnd_mat_c3ann = np.empty((1166,720,1440))
Crplnd_mat_c3per = np.empty((1166,720,1440))
Crplnd_mat_c4ann = np.empty((1166,720,1440))
Crplnd_mat_c4per = np.empty((1166,720,1440))
Crplnd_mat_c3nfx = np.empty((1166,720,1440))
Crplnd_combined = np.empty((55,720,1440))
# initializing matrix
for i in range(0,len(yrs_avail)):
    tmp1 = np.ma.getdata(Crplnd_mat['c3ann'][i,:,:])
    Crplnd_mat_c3ann[i,:,:]  = tmp1
    tmp2 = np.ma.getdata(Crplnd_mat['c3per'][i,:,:])
    Crplnd_mat_c3per[i,:,:]  = tmp2
    tmp3 = np.ma.getdata(Crplnd_mat['c4ann'][i,:,:])
    Crplnd_mat_c4ann[i,:,:]  = tmp3
    tmp4 = np.ma.getdata(Crplnd_mat['c4per'][i,:,:])
    Crplnd_mat_c4per[i,:,:]  = tmp4
    tmp5 = np.ma.getdata(Crplnd_mat['c3nfx'][i,:,:])
    Crplnd_mat_c3nfx[i,:,:]  = tmp5
# alloting filled value with nan
for i in range(0,len(yrs_avail)):
    print(i)
    idx_fillv = np.where(Crplnd_mat_c3ann[i,:,:]>1)
    Crplnd_mat_c3ann[i,:,:][idx_fillv] = np.nan
    idx_fillv = np.where(Crplnd_mat_c3per[i,:,:]>1)
    Crplnd_mat_c3per[i,:,:][idx_fillv] = np.nan
    idx_fillv = np.where(Crplnd_mat_c4ann[i,:,:]>1)
    Crplnd_mat_c4ann[i,:,:][idx_fillv] = np.nan
    idx_fillv = np.where(Crplnd_mat_c4per[i,:,:]>1)
    Crplnd_mat_c4per[i,:,:][idx_fillv] = np.nan
    idx_fillv = np.where(Crplnd_mat_c3nfx[i,:,:]>1)
    Crplnd_mat_c3nfx[i,:,:][idx_fillv] = np.nan
# combining datasets
idx_yrs_to_consider1 = [ int(x) for x in idx_yrs_to_consider[idx_yrs_to_consider>0]]
Crplnd_mat_c3ann_m = Crplnd_mat_c3ann[idx_yrs_to_consider1,:,:]
Crplnd_mat_c3per_m = Crplnd_mat_c3per[idx_yrs_to_consider1,:,:]
Crplnd_mat_c4ann_m = Crplnd_mat_c4ann[idx_yrs_to_consider1,:,:]
Crplnd_mat_c4per_m = Crplnd_mat_c4per[idx_yrs_to_consider1,:,:]
Crplnd_mat_c3nfx_m = Crplnd_mat_c3nfx[idx_yrs_to_consider1,:,:]

for i in range(0,len(idx_yrs_to_consider1)):
    tmp = np.nanmax([Crplnd_mat_c3ann_m[i,:,:], Crplnd_mat_c3per_m[i,:,:],Crplnd_mat_c4ann_m[i,:,:],Crplnd_mat_c4per_m[i,:,:], Crplnd_mat_c3nfx_m[i,:,:]], axis = 0)
    Crplnd_combined[i,:,:] = tmp
# grid cell resolution: 0.25 x 0.25 degre; 0.1 degee = 11.1 km; 0.25 degree =  27.75 km and 770.0625 km2
# grid cell resolution: 0.5 x 0.5 degre; 0.1 degee = 11.1 km; 0.5 degree =  55.5 km and 3080.25 km2
# converting matrix to raster

for yr1 in range(0,len(yrs_to_consider)-3):
    transform = from_origin(-180, 90, 0.5, 0.5)
    # resizing the matrix
    Crplnd_combined_rsz = resize(Crplnd_combined[yr1,:,:],(360,720))
    # converting percentage grid cell to area in km2
    Crplnd_combined_km2 = Crplnd_combined_rsz*3080.25
    # replacing nan with fill value
    idx_nan = np.where(np.isnan(Crplnd_combined_rsz))
    Crplnd_combined_rsz[idx_nan] = fval
    # writing raster
    new_dataset = rasterio.open("Cropland_yr{0}_LUH.tif".format(np.int(yrs_to_consider[yr1])), 'w',  driver='GTiff',
                                height = Crplnd_combined_km2.shape[0], width = Crplnd_combined_km2.shape[1],
                                            count=1, dtype=str(Crplnd_combined_km2.dtype),
                                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                            transform=transform)
    outMatrix = np.reshape(Crplnd_combined_km2,(Crplnd_combined_km2.shape[0],Crplnd_combined_km2.shape[1]))
    new_dataset.write(outMatrix,1)
    new_dataset.close()



## conversion for Zhou
for yr1 in range(0,len(yrs_to_consider)):
    transform = from_origin(-178.75,89.3706, 2.48263888888888884,1.249938872316494809)
    # resizing the matrix
    Crplnd_combined_rsz = resize(Crplnd_combined[yr1,:,:],(143,144), order = 1, mode='wrap')
    # converting percentage grid cell to area in km2
    Crplnd_combined_km2 = Crplnd_combined_rsz*2.48263888888888884*1.249938872316494809*(11.1/0.1)**2
    # replacing nan with fill value
    idx_nan = np.where(np.isnan(Crplnd_combined_rsz))
    Crplnd_combined_rsz[idx_nan] = fval
    # writing raster
    new_dataset = rasterio.open("Cropland_yr{0}_LUH_Zhou.tif".format(np.int(yrs_to_consider[yr1])), 'w',  driver='GTiff',
                                height = Crplnd_combined_km2.shape[0], width = Crplnd_combined_km2.shape[1],
                                            count=1, dtype=str(Crplnd_combined_km2.dtype),
                                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                            transform=transform)
    outMatrix = np.reshape(Crplnd_combined_km2,(Crplnd_combined_km2.shape[0],Crplnd_combined_km2.shape[1]))
    new_dataset.write(outMatrix,1)
    new_dataset.close()

## other initial investigation
Crplnd_df = pd.DataFrame(Crplnd_mat['primf'][1165,:,:])
Crplnd_df.to_csv(os.path.join(fpath,'LUH_datacheck.csv'))

plt.imshow(Crplnd_mat['primf'][1165,:,:])
plt.colorbar()
plt.title('Forested primary land')
plt.savefig(os.path.join(fpath,'Forested_primary_land.png'))

plt.imshow(Crplnd_mat['primn'][1165,:,:])
plt.colorbar()
plt.title('Non-forested primary land')
plt.savefig(os.path.join(fpath,'Non_forested_primary_land.png'))

plt.imshow(Crplnd_mat['c3ann'][1165,:,:])
plt.colorbar()
plt.title('C3 annual crops')
plt.savefig(os.path.join(fpath,'C3_annual_crops.png'))

fval = 1.e+20
idx_fillv = np.where(Crplnd_mat['primn'][1165,:,:]==fval)
Crplnd_mat['primn'][1165,:,:][idx_fillv] = np.nan
plt.imshow(Crplnd_mat['primn'][1165,:,:])
plt.colorbar()

print(Crplnd_mat)
# class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF4_CLASSIC data model, file format HDF5):
#     host: UMD College Park
#     comment: LUH2
#     contact: gchurtt@umd.edu, lchini@umd.edu, steve.frolking@unh.edu, ritvik@umd.edu
#     creation_date: 2016-10-12T18:26:36Z
#     title: Land-Use Harmonization Data Sets
#     activity_id: input4MIPs
#     Conventions: CF-1.6
#     data_structure: grid
#     source: LUH2 v2h: Land-Use Harmonization Data Set
#     source_id: LUH2 v2h
#     license: MIT
#     further_info_url: http://luh.umd.edu
#     frequency: yr
#     institution_id: UofMD
#     institution: University of Maryland College Park
#     realm: land
#     references: Hurtt, Chini et al. 2011
#     dimensions(sizes): time(1166), lat(720), lon(1440), bounds(2)
#     variables(dimensions): float64 time(time), float64 lat(lat), float64 lon(lon), float32 primf(time,lat,lon), float32 primn(time,lat,lon), float32 secdf(time,lat,lon), float32 secdn(time,lat,lon), float32 urban(time,lat,lon), float32 c3ann(time,lat,lon), float32 c4ann(time,lat,lon), float32 c3per(time,lat,lon), float32 c4per(time,lat,lon), float32 c3nfx(time,lat,lon), float32 pastr(time,lat,lon), float32 range(time,lat,lon), float32 secmb(time,lat,lon), float32 secma(time,lat,lon), float64 lat_bounds(lat,bounds), float64 lon_bounds(lon,bounds)
#     groups:

## changing grid resolution manually
transform = from_origin(-178.75, 89.3706, 2.48263888888888884, 1.249938872316494809)

# changing resolution
for idx_yr in range(0,len(yrs_to_consider)):
    Crplnd_mat = Crplnd_combined[idx_yr,:,:]*770.0625
    #print(Crplnd_mat)
    idx_neg = np.where(Crplnd_mat<0)
    Crplnd_mat[idx_neg] = 0
    #plt.imshow(Crplnd_mat)
    #plt.colorbar()
    #plt.title(file_names[idx_yr])

    # changing resolution
    lat = np.arange(0, Crplnd_mat.shape[0], 5)
    lon = np.arange(0, Crplnd_mat.shape[1], 10)
    outMatrix = np.zeros((143,144), dtype="float")

    for lat1 in range(1, len(lat)):
        for lon1 in range(1, len(lon)):
            if lon1 == len(lon) - 1:
                outMatrix[lat1-1, lon1-1] = np.nansum(Crplnd_mat[lat[lat1-1]:lat[lat1], lon[lon1-1]:Crplnd_mat.shape[1]-1])

            elif lat1 == len(lat) - 1:
                outMatrix[lat1-1, lon1-1] = np.nansum(Crplnd_mat[lat[lat1-1]:Crplnd_mat.shape[0]-1, lon[lon1-1]:lon[lon1]])

            elif lon1 == len(lon) - 1 and lat1 == len(lat) - 1:
                outMatrix[lat1-1, lon1-1] = np.nansum(Crplnd_mat[lat[lat1-1]:Crplnd_mat.shape[0]-1, lon[lon1-1]:Crplnd_mat.shape[1]-1])

            else:
                outMatrix[lat1-1, lon1-1] = np.nansum(Crplnd_mat[lat[lat1-1]:lat[lat1], lon[lon1-1]:lon[lon1]])

    plt.imshow(outMatrix)

    # writing to tif file

    new_dataset = rasterio.open("Cropland_yr{0}_LUH_Zhou.tif".format(np.int(yrs_to_consider[idx_yr])), 'w',  driver='GTiff',height = outMatrix.shape[0], width = outMatrix.shape[1],
                                count=1, dtype=str(outMatrix.dtype),
                                crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                transform=transform)

    new_dataset.write(outMatrix,1)
    new_dataset.close()





# Crplnd_mat['primf'][0]
# trans_mat = nc.Dataset(os.path.join(fpath,'transitions.nc'))
# trans_mat.variables.keys()
#
# mgmt_mat = nc.Dataset(os.path.join(fpath,'management.nc'))
# mgmt_mat.variables.keys()
#
# print(Crplnd_mat)
# with open(os.path.join(fpath,'UofMD_yr_UofMD-landState-MESSAGE-ssp245-2-1-f_added-tree-cover_gn_v20190124.json'), 'r') as myfile:
#     data=myfile.read()
# obj = json.loads(data)
# print(obj)
# print(obj['input4MIPs-ScenarioMIP-RitvikSahajpal'])


# fpath1 = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2'
# im = Image.open('Cropland_yr1961_LUH.tif')