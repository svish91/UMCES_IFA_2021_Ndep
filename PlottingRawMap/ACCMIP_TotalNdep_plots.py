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

yrN = np.arange(1961,2019,1)
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Ndep_ACCMIP\TotalN'

for i in range(0,len(yrN)):
    plt.clf()
    xx = gdal.Open(os.path.join(file_dir,'totalN_yr{0}_ACCMIP.tif'.format(yrN[i])))
    Ndep_kgha = np.array(xx.GetRasterBand(1).ReadAsArray())/100
    #plt.imshow(Ndep_kgha)
    #plt.colorbar()
    src = rasterio.open(os.path.join(file_dir,'totalN_yr{0}_ACCMIP.tif'.format(yrN[i])))

    with fiona.open(r"D:\GoogleDrive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                                 r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp", "r") as shapefile:
        features = [feature["geometry"] for feature in shapefile]



    rasterio.plot.show((src, 1), cmap='jet')
    ax = mpl.pyplot.gca()

    N=21
    cmap = plt.get_cmap('jet',N)
    norm = mpl.colors.Normalize(vmin=0,vmax=np.max(Ndep_kgha))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ticks=np.arange(0,np.max(Ndep_kgha),5),#np.linspace(0,np.max(Ndep_kgha),N),
                  boundaries=np.arange(0,np.max(Ndep_kgha),0.1),
                 label = "N Deposition $(kgN ha^{-1})$",shrink = 0.7)

    patches = [PolygonPatch(feature) for feature in features]
    ax.add_collection(mpl.collections.PatchCollection(patches, facecolors = "None", edgecolor = "grey"))

    figure = plt.gcf()

    figure.set_size_inches(7, 4)
    plt.savefig(r"D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Ndep_ACCMIP\TotalN\Plots_wShapefile\TotNdep_{0}_kgNha_ACCMIP.png".format(yrN[i]), dpi=200)

