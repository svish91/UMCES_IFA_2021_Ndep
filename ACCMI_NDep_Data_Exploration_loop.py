import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from rasterio.windows import Window
from rasterio.transform import from_origin
import rasterio
import pydap.client

# DODS file
# file_dir_dods = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\N_deposition\Lamarque_ACCMIP\DODS'
# xx =pydap.client.open(os.path.join(file_dir_dods,'ndep_noy_histsoc_annual_1861_2005.nc.dods'))
# xx.read()
### NETCDF file
# NOx
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\N_deposition\Lamarque_ACCMIP'
NOx_1861_2005=nc.Dataset(os.path.join(file_dir,'ndep_noy_histsoc_annual_1861_2005.nc'))
NOx_2006_2099=nc.Dataset(os.path.join(file_dir,'ndep_noy_2005soc_annual_2006_2099.nc'))

NHy_1861_2005=nc.Dataset(os.path.join(file_dir,'ndep_nhx_histsoc_annual_1861_2005.nc'))
NHy_2006_2099=nc.Dataset(os.path.join(file_dir,'ndep_nhx_2005soc_annual_2006_2099.nc'))

print(NOx_1861_2005)
# <class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF4_CLASSIC data model, file format HDF5):
#     Conventions: None
#     contact: Hanqin Tian, tianhan@auburn.edu
#     creation_date: 2018-07-13T12:35:31Z
#     project: isimip2b
#     product: input
#     world_region: Global land
#     country: ALL
#     time_frequency: yr
#     publisher: ISIMIP coordination team <info@isimip.org>
#     description: N-Deposition input data set prepared for ISIMIP2b. Data Set Details: https://www.isimip.org/gettingstarted/details/24, ISIMIP Terms of Use: https://www.isimip.org/protocol/terms-of-use/, Published under CC BY 4.0 licence.
#     doi: NA
#     licence: CC BY 4.0
#     creator: ISIMIP Coordination Team <info@isimip.org>
#     tracking_id: f72b1556-67dc-449d-83d1-143fd36acdd5
#     dataset_type: Nitrogen deposition
#     bias_correction: NoBC
#     dimensions(sizes): lon(720), lat(360), time(145)
#     variables(dimensions): float32 lon(lon), float32 lat(lat), float64 time(time), float32 nhx(time,lat,lon)
#     groups:

NOx_1861_2005.variables.keys()
NOx_2006_2099.variables.keys()
#odict_keys(['lon', 'lat', 'time', 'noy'])
# units: g N m - 2 yr - 1 = 1000 kg N km-2 yr-1

# Merging two files
yrs_to_consider = np.arange(1961,2019,1)
yrs_avail = np.arange(1861,2100,1)
idx_yrs_to_consider = np.zeros(yrs_to_consider.shape)
for i in range(0,len(yrs_to_consider)):
    idx_yrs_to_consider[i]=np.where(yrs_avail== yrs_to_consider[i])[0]
idx_yrs_to_consider = idx_yrs_to_consider.astype('int')

# NOx
NOx_1861_2005_mat = np.array(NOx_1861_2005['noy'][:])
idx_default = np.where(NOx_1861_2005_mat==1e+20)
NOx_1861_2005_mat[idx_default] = 0
NOx_2006_2099_mat = np.array(NOx_2006_2099['noy'][:])
idx_default = np.where(NOx_2006_2099_mat==1e+20)
NOx_2006_2099_mat[idx_default] = 0

NOx_concat_tmp = np.concatenate((NOx_1861_2005_mat,NOx_2006_2099_mat),axis=0)
NOx_1961_2018_concat = NOx_concat_tmp[idx_yrs_to_consider,:,:]
# NHy
NHy_1861_2005_mat = np.array(NHy_1861_2005['nhx'][:])
idx_default = np.where(NHy_1861_2005_mat==1e+20)
NHy_1861_2005_mat[idx_default] = 0
NHy_2006_2099_mat = np.array(NHy_2006_2099['nhx'][:])
idx_default = np.where(NHy_2006_2099_mat==1e+20)
NHy_2006_2099_mat[idx_default] = 0

NHy_concat_tmp = np.concatenate((NHy_1861_2005_mat,NHy_2006_2099_mat),axis=0)
NHy_1961_2018_concat = NHy_concat_tmp[idx_yrs_to_consider,:,:]
# changing units
#units: g N m - 2 yr - 1 = 1000 kg N km-2 yr-1
NOx_1961_2018_concat_kgNkm = 1000*NOx_1961_2018_concat
NHy_1961_2018_concat_kgNkm = 1000*NHy_1961_2018_concat

totalN_1961_2018_concat_kgNkm = NOx_1961_2018_concat_kgNkm + NHy_1961_2018_concat_kgNkm
# use for loop here

for yr1 in range(0,len(yrs_to_consider)):
    transform = from_origin(-180, 90, 0.5, 0.5)
    new_dataset = rasterio.open("NOx_yr{0}.tif".format(np.int(yrs_to_consider[yr1])), 'w',  driver='GTiff',
                                height = NOx_1961_2018_concat_kgNkm.shape[1], width = NOx_1961_2018_concat_kgNkm.shape[2],
                                            count=1, dtype=str(NOx_1961_2018_concat_kgNkm.dtype),
                                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                            transform=transform)
    outMatrix = np.reshape(NOx_1961_2018_concat_kgNkm[yr1,:,:],(NOx_1961_2018_concat_kgNkm.shape[1],NOx_1961_2018_concat_kgNkm.shape[2]))
    new_dataset.write(outMatrix,1)
    new_dataset.close()
    #NHy
    transform = from_origin(-180, 90, 0.5, 0.5)

    new_dataset = rasterio.open("NHy_yr{0}.tif".format(np.int(yrs_to_consider[yr1])), 'w',  driver='GTiff',
                                height = NHy_1961_2018_concat_kgNkm.shape[1], width = NHy_1961_2018_concat_kgNkm.shape[2],
                                            count=1, dtype=str(NHy_1961_2018_concat_kgNkm.dtype),
                                            crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                            transform=transform)
    outMatrix = np.reshape(NHy_1961_2018_concat_kgNkm[yr1,:,:],(NHy_1961_2018_concat_kgNkm.shape[1],NHy_1961_2018_concat_kgNkm.shape[2]))
    new_dataset.write(outMatrix,1)
    new_dataset.close()

# total N
for yr1 in range(0,len(yrs_to_consider)):
    transform = from_origin(-180, 90, 0.5, 0.5)

    new_dataset = rasterio.open("totalN_yr{0}_ACCMIP.tif".format(np.int(yrs_to_consider[yr1])), 'w', driver='GTiff',
                                height=totalN_1961_2018_concat_kgNkm.shape[1], width=totalN_1961_2018_concat_kgNkm.shape[2],
                                count=1, dtype=str(totalN_1961_2018_concat_kgNkm.dtype),
                                crs='+init=epsg:4326',
                                # '+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                transform=transform)
    outMatrix = np.reshape(totalN_1961_2018_concat_kgNkm[yr1, :, :],
                           (totalN_1961_2018_concat_kgNkm.shape[1], totalN_1961_2018_concat_kgNkm.shape[2]))
    new_dataset.write(outMatrix, 1)
    new_dataset.close()
# plt.figure()
# plt.imshow(NOx_1861_2005_mat[139,:,:]*1000)
# plt.colorbar()
# Plotting 2006 - 2099