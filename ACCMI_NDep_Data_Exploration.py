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
NHy_1861_2005=nc.Dataset(os.path.join(file_dir,'ndep_nhx_histsoc_annual_1861_2005.nc'))

NOx_2006_2099=nc.Dataset(os.path.join(file_dir,'ndep_noy_2005soc_annual_2006_2099.nc'))

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

# Plotting 1861-2005
NOx_1861_2005_mat = np.array(NOx_1861_2005['noy'][:])
idx_default = np.where(NOx_1861_2005_mat==1e+20)
NOx_1861_2005_mat[idx_default] = 0
plt.figure()
plt.imshow(NOx_1861_2005_mat[139,:,:]*1000)
plt.colorbar()
# Plotting 2006 - 2099
plt.figure()
NOx_2006_2099_mat = np.array(NOx_2006_2099['noy'][:])
idx_default = np.where(NOx_2006_2099_mat==1e+20)
NOx_2006_2099_mat[idx_default] = 0

plt.imshow(NOx_2006_2099_mat[0,:,:]*1000)
plt.colorbar()

# creating raster for one file
yrs = np.arange(1861,2006,1)
idx_yr = np.where(yrs == 2000)

transform = from_origin(-180, 90, 0.5, 0.5)

new_dataset = rasterio.open("NOx{0}.tif".format(np.int(yrs[idx_yr])), 'w',  driver='GTiff',height = NOx_1861_2005_mat.shape[1], width = NOx_1861_2005_mat.shape[2],
                                        count=1, dtype=str(NOx_1861_2005_mat.dtype),
                                        crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                        transform=transform)
outMatrix = np.reshape(1000*NOx_1861_2005_mat[idx_yr,:,:],(NOx_1861_2005_mat.shape[1],NOx_1861_2005_mat.shape[2]))
new_dataset.write(outMatrix,1)
new_dataset.close()


#NHy
NHy_1861_2005_mat = np.array(NHy_1861_2005['nhx'][:])
idx_default = np.where(NHy_1861_2005_mat==1e+20)
NHy_1861_2005_mat[idx_default] = 0
transform = from_origin(-180, 90, 0.5, 0.5)

new_dataset = rasterio.open("NHy{0}.tif".format(np.int(yrs[idx_yr])), 'w',  driver='GTiff',height = NHy_1861_2005_mat.shape[1], width = NHy_1861_2005_mat.shape[2],
                                        count=1, dtype=str(NHy_1861_2005_mat.dtype),
                                        crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                        transform=transform)
outMatrix = np.reshape(1000*NHy_1861_2005_mat[idx_yr,:,:],(NHy_1861_2005_mat.shape[1],NHy_1861_2005_mat.shape[2]))
new_dataset.write(outMatrix,1)
new_dataset.close()



#### plotting maps
