import numpy as np
import geopandas as gp
import os
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping

# this function estimates the weighted mean of the N deposition data with weights being equal to the cropland area grids

def f_aggDataSimple(file_dir, file_name, crfile_dir,crfile_name):

    shapefile = gp.read_file(r"99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
    # columns: OBJECTID	CNTRY_NAME
    geoms = shapefile.geometry.values  # list of shapely geometries

    # matrix for countries
    avgData = np.empty(len(shapefile['OBJECTID']))
    TotCrArea = np.empty(len(shapefile['OBJECTID']))

    for co in range(0,len(geoms)):
        # reading country boundary
        geoms1 = [mapping(geoms[co])]

        # reading the desired raster file
        with rasterio.open(os.path.join(file_dir,"{0}.tif".format(file_name))) as w_src:
            w_data, w_out_transform = mask(w_src, geoms1, crop=True)

        # reading cropland area data within boundary
        with rasterio.open(os.path.join(crfile_dir,"{0}.tif".format(crfile_name))) as ar_src:
            ar_data, ar_out_transform = mask(ar_src, geoms1, crop=True)

        # aggregating the data with weights of cropland area
        numerator1 = np.nansum(w_data*ar_data)
        denominator1 = np.nansum(ar_data)

        # estimating average

        if denominator1 == 0:
            avgData[co] = np.nan
        else:
            avgData[co] = numerator1/denominator1

        TotCrArea[co] = denominator1
    return avgData, TotCrArea,
