import netCDF4 as nc
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
#from f_changingResolution import f_changingResolution
#from f_aggDataSimple import f_aggDataSimple
from rasterio.windows import Window
from rasterio.transform import from_origin
import rasterio



file_names = ['1960AD_lu','1970AD_lu','1980AD_lu','1990AD_lu','2000AD_lu','2001AD_lu','2002AD_lu','2003AD_lu','2004AD_lu','2005AD_lu','2006AD_lu','2007AD_lu',
              '2008AD_lu','2009AD_lu','2010AD_lu','2011AD_lu','2012AD_lu','2013AD_lu','2014AD_lu','2015AD_lu','2016AD_lu','2017AD_lu']
file_names1 = ['1960AD','1970AD','1980AD','1990AD','2000AD','2001AD','2002AD','2003AD','2004AD','2005AD','2006AD','2007AD',
              '2008AD','2009AD','2010AD','2011AD','2012AD','2013AD','2014AD','2015AD','2016AD','2017AD']
idx_yr = 4
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Cropland_area\HYDE3.2\baseline\baseline\zip'
Crplnd_mat = np.loadtxt(os.path.join(file_dir,file_names[idx_yr],'cropland{0}.asc'.format(file_names1[idx_yr])), skiprows=6)


print(Crplnd_mat)
idx_neg = np.where(Crplnd_mat<0)
Crplnd_mat[idx_neg] = 0
plt.imshow(Crplnd_mat)
plt.colorbar()
plt.title(file_names[idx_yr])

# changing resolution
lat = np.arange(0, Crplnd_mat.shape[0], 6)
lon = np.arange(0, Crplnd_mat.shape[1], 6)
outMatrix = np.zeros((360,720), dtype="float")

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
transform = from_origin(-180, 90, 0.5, 0.5)

new_dataset = rasterio.open("Cropland{0}.tif".format(file_names1[idx_yr]), 'w',  driver='GTiff',height = outMatrix.shape[0], width = outMatrix.shape[1],
                                        count=1, dtype=str(outMatrix.dtype),
                                        crs='+init=epsg:4326',#'+proj=utm +ellps=WGS84 +datum=WGS84  +units=degrees +no_defs',
                                        transform=transform)

new_dataset.write(outMatrix,1)
new_dataset.close()

