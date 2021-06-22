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

yrN = [1970,1980,1990,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013]
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'

for i in range(0,len(yrN)):
    plt.clf()
    xx = gdal.Open(os.path.join(file_dir,'ndep_{0}.tif'.format(yrN[i])))
    Ndep_kgha = np.array(xx.GetRasterBand(1).ReadAsArray())/100
    #plt.imshow(Ndep_kgha)
    #plt.colorbar()
    src = rasterio.open(os.path.join(file_dir,'ndep_{0}.tif'.format(yrN[i])))

    with fiona.open(r"D:\GoogleDrive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                                 r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp", "r") as shapefile:
        features = [feature["geometry"] for feature in shapefile]



    rasterio.plot.show((src, 1), cmap='jet')
    ax = mpl.pyplot.gca()

    N=20
    cmap = plt.get_cmap('jet',N)
    norm = mpl.colors.Normalize(vmin=0,vmax=np.max(Ndep_kgha))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ticks=np.arange(0,np.max(Ndep_kgha),5),#np.linspace(0,np.max(Ndep_kgha),N),
                  boundaries=np.arange(0,np.max(Ndep_kgha),0.1),
                 label = "N Deposition $(kg N ha^{-1})$", shrink = 0.7)

    patches = [PolygonPatch(feature) for feature in features]
    ax.add_collection(mpl.collections.PatchCollection(patches, facecolors = "None", edgecolor = "grey"))

    figure = plt.gcf()

    figure.set_size_inches(7, 4)
    plt.savefig(r"D:\GoogleDrive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF\Ndep_map_modified\TotNdep_{0}_kgNha.png".format(yrN[i]), dpi=300)
    #plt.savefig(r"D:\GoogleDrive\N_deposition_project\GriddedDATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF\Ndep_map_sameLIM\TotNdep_{0}_kgNha.png".format(yrN[i]), dpi=200)

