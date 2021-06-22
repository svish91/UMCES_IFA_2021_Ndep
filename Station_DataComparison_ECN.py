from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp
import rasterio
from shapely.geometry import mapping
from rasterio.mask import mask

## Grabbing my number
data_tot_Ndep_ACCMIP = pd.read_csv('df_totNdep_kgNha.csv', index_col=0)
yr = 2009
plt.boxplot(data_tot_Ndep_ACCMIP.iloc[230])

# N flux deposition model
# Service type	Service	 Indicator variable (units) 	Variable_ID	Variable_Number	ALI	CAI	DRA	GLE	MOO	NOR	POR	ROT	SNO	SOU	WYT
# Regulating	Air quality regulation 	 N flux per hectare from national deposition model (kg N ha-1) 	R_N_flux	19	36.82074268	6.9381691	4.406546474	10.15685637	18.79975145	18.26610229	7.598443563	8.148057296	18.94330303	17.28361242	22.57264474

Nflux_ECN = [4.406546474,18.26610229,7.598443563,8.148057296,22.57264474]
Nflux_siteName = ['DRA','NOR','POR','ROT','WYT']

plt.boxplot(Nflux_ECN)
plt.plot(1,data_tot_Ndep_ACCMIP.loc[['United Kingdom'],['2009']],marker='*',markersize=20, color='black' )
plt.title(' N flux per hectare from national deposition model 2009')
plt.ylabel('kg N ha-1')
plt.savefig('N_flux_deposition_model_2009_comparison.png')

# NOx: kg N km-2 yr-1
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Ndep'
file_name = "NOx_yr{0}.tif".format(yr)
NOx_mat = np.reshape(rasterio.open(os.path.join(file_dir,file_name)).read(),(360,720))
# NHy: kg N km-2 yr-1
file_name = "NHy_yr{0}.tif".format(yr)
NHy_mat = np.reshape(rasterio.open(os.path.join(file_dir,file_name)).read(),(360,720))

# cropland: km2
if yr > 1960 and yr <= 1965:
    yrcr = 1960
elif yr > 1965 and yr <= 1975:
    yrcr = 1970
elif yr > 1975 and yr <= 1985:
    yrcr = 1980
elif yr > 1985 and yr <= 1995:
    yrcr = 1990
elif yr > 1995 and yr <= 2000:
    yrcr = 2000
elif yr == 2018:
    yrcr = 2017
else:
    yrcr = yr

crfile_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland'
crfile_name = "Cropland{0}AD.tif".format(yrcr)
CrL_mat = np.reshape(rasterio.open(os.path.join(crfile_dir,crfile_name)).read(),(360,720))


# # testing on one station
# T01	Drayton
# 52° 11' 37.95" N
# 1° 45' 51.95" W
# minutes	'	to degree multiply by	1/60 or	0.016667
# seconds	"	to degree multiply by	1/3600 or	2.777778 e-4
print("Latitude:", round(52+(11/60)+(37.95/3600),2))
#Latitude: 52.19
lat = round(52+(11/60)+(37.95/3600),2)
print("Longitude:", round(1+(45/60)+(51.95/3600),2))
# Longitude: 1.76
lon = round(1+(45/60)+(51.95/3600),2)
# rows 360: -90 to 90 -- 0.5 degree
# colums 720: -180 to 180 -- 0.5 degree
# corresponding to T01: 52 degree N and 1 degree W - (52.19+90)/0.5, (180-1.76)/0.5
rr = 360-round((lat+90)/0.5)-1
cc = round((180-lon)/0.5)-1
print('NOx:',NOx_mat[rr,cc])
print('NHy:',NHy_mat[rr,cc])
print('Crop land:',CrL_mat[rr,cc])
print("Tot_KgNha:",((NOx_mat[rr,cc]*CrL_mat[rr,cc]+NHy_mat[rr,cc]*CrL_mat[rr,cc])/CrL_mat[rr,cc])/100)



# checking data by plot
shapefile = gp.read_file(r"D:\GoogleDrive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                             r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
shapefile_m = np.array(shapefile)
geoms = shapefile.geometry.values
co=230
geoms1 = [mapping(geoms[co])]

# reading the desired raster file
file_name = "NOx_yr{0}".format(yr)

with rasterio.open(os.path.join(file_dir,"{0}.tif".format(file_name))) as w_src:
    w_data, w_out_transform = mask(w_src, geoms1, crop=True)

# reading cropland area data within boundary
crfile_name = "Cropland{0}AD".format(yrcr)

with rasterio.open(os.path.join(crfile_dir,"{0}.tif".format(crfile_name))) as ar_src:
    ar_data, ar_out_transform = mask(ar_src, geoms1, crop=True)

plt.figure()
plt.imshow(np.reshape(w_data,(23,21)))
plt.title('NOx')
plt.colorbar()

plt.figure()
plt.imshow(np.reshape(ar_data,(23,21)))
plt.title('Crop Land')
plt.colorbar()


