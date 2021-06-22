import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from rasterio.windows import Window
from rasterio.transform import from_origin
import rasterio

# NOx
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\N_deposition\CCMI'
# NOx
dryNOx_1850_2014=nc.Dataset(os.path.join(file_dir,'drynoy_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc'))
wetNOx_1850_2014=nc.Dataset(os.path.join(file_dir,'wetnoy_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc'))
# NOy
dryNHy_1850_2014=nc.Dataset(os.path.join(file_dir,'drynhx_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc'))
wetNHy_1850_2014=nc.Dataset(os.path.join(file_dir,'wetnhx_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc'))
print(dryNOx_1850_2014)
# <class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF3_CLASSIC data model, file format NETCDF3):
#     variable_id: drynoy
#     Conventions: CF-1.6
#     activity_id: input4MIPs
#     contact: Douglas Kinnison (dkin@ucar.edu); Michaela Hegglin (m.i.hegglin@reading.ac.uk)
#     creation_date: 2016-11-15T12:00:00Z
#     dataset_category: surfaceFluxes
#     dataset_version_number: 2.0
#     grid: 1p9x2 degree latitude x longitude
#     grid_label: gn
#     grid_resolution: 1p9x2 degree
#     further_info_url: http://blogs.reading.ac.uk/ccmi/forcing-databases-in-support-of-cmip6/
#     institution: National Center for Atmospheric Research, Boulder, CO 80307, USA
#     institution_id: NCAR
#     mip_era: CMIP6
#     source: CCMI nitrogen deposition dataset from CAM-Chem simulations
#     source_id: NCAR-CCMI-2-0
#     target_mip: CMIP
#     title: CCMI v2.0 nitrogen deposition dataset prepared for input4MIPs
#     references: Hegglin, M. I., D. Kinnison, J.-F. Lamarque, et al., Historical and future Nitrogen deposition database (1850-2100) in support of CMIP6, GMD, in preparation.
#     license: CCMI data produced by NCAR is licensed under a Creative Commons Attribution \"Share Alike\" 4.0 International License (http://creativecommons.org/licenses/by/4.0/). The data producers and data providers make no warranty, either express or implied, including but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law.
#     history: v2.0 has removed negative values found in v1.0 nitrogen deposition fields
#     comment: Data product from CAM-Chem.
#     tracking_id: hdl:21.14100/531ef352-a685-46f6-823a-c89121887d26
#     nominal_resolution: 250 km
#     frequency: mon
#     dimensions(sizes): lon(144), lat(96), time(1980), bnds(2)
#     variables(dimensions): float32 lon(lon), float32 lat(lat), float64 time(time), float64 time_bnds(time,bnds), float32 drynoy(time,lat,lon)
#     groups:

dryNOx_1850_2014.variables.keys()
# odict_keys(['lon', 'lat', 'time', 'time_bnds', 'drynoy'])
# units: kg m-2 s-1

