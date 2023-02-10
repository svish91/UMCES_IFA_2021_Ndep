from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp


shapefile = gp.read_file(r"99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
df_NOx_kgNha = pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2051,1))
df_NOx_kgNha = df_NOx_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_NHy_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2051,1))
df_NHy_kgNha = df_NHy_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_totNdep_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2051,1))
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2051,1))
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])
# NOx
for yr in np.arange(1961,2051,1):
    print(yr)
    if yr > 2015:
        yrcr = 2015
    else:
        yrcr = yr
    idx_yr = np.where(np.arange(1961, 2019, 1) == yr)[0]
    file_dir = r'.\Modified_Raster_Files\Ndep_ACCMIP'
    file_name = "NOx_yr{0}".format(yr)
    crfile_dir = r'.\Modified_Raster_Files\Cropland_LUH2'
    crfile_name = "Cropland_yr{0}_LUH".format(yrcr)
    xx_NOx_kgNkm = f_aggDataSimple(file_dir, file_name, crfile_dir, crfile_name)
    df_NOx_kgNha[yr] = xx_NOx_kgNkm[0] / 100
    # NHx
    file_dir = r'.\Modified_Raster_Files\Ndep_ACCMIP'
    file_name = "NHy_yr{0}".format(yr)
    crfile_dir = r'.\Modified_Raster_Files\Cropland_LUH2'
    crfile_name = "Cropland_yr{0}_LUH".format(yrcr)
    xx_NHy_kgNkm = f_aggDataSimple(file_dir, file_name, crfile_dir, crfile_name)
    df_NHy_kgNha[yr] = xx_NHy_kgNkm[0] / 100
    # cropland
    df_cropland_km2[yr] = xx_NOx_kgNkm[1]
    # total
    df_totNdep_kgNha[yr] = ((xx_NOx_kgNkm[0] * xx_NOx_kgNkm[1] + xx_NHy_kgNkm[0] * xx_NHy_kgNkm[1]) / xx_NHy_kgNkm[
        1]) / 100

df_totNdep_kgNha_trans = df_totNdep_kgNha.T
df_NOx_kgNha_trans = df_NOx_kgNha.T
df_NHy_kgNha_trans = df_NHy_kgNha.T
df_cropland_km2_trans = df_cropland_km2.T

# time series plot
for co in range(0,len(shapefile['CNTRY_NAME'])):
    plt.clf()
    #plt.figure()
    plt.plot(df_totNdep_kgNha_trans[shapefile['CNTRY_NAME'][co]],color = 'red')
    plt.xlim(1961,2050)
    plt.ylabel('Total N Deposition (kgN/ha)')
    plt.xlabel('Years')
    plt.title(shapefile['CNTRY_NAME'][co])
    plt.ylim([0,20])
    plt.savefig(r".\Results\ACCMIP\LUH2\Time_Series_1961_2050\TotNdep_{0}_kgNha.png".format(shapefile['CNTRY_NAME'][co]), dpi=200)

# to csv
df_totNdep_kgNha.to_csv("df_totNdep_kgNha_201950_EP.csv")
df_NOx_kgNha.to_csv("df_NOx_kgNha_201950_EP.csv")
df_NHy_kgNha.to_csv("df_NHy_kgNha_201950_EP.csv")
df_cropland_km2.to_csv("df_cropland_km2_201950_EP.csv")
#rslt_df.to_csv("Year_2000_m.csv")


df_totNdep_kgNha.loc['Taiwan'] = df_totNdep_kgNha.loc['China']
## plotting map: total N kgN/ha
#df_ndep = pd.DataFrame({'Ndep_kgN':xx_kgN,'ISO3':shapefile['ISO3']})
for yr_to_plot in np.arange(2019,2051,1):
    plt.clf()
    df_ndep_map_kgNha = pd.DataFrame({'Ndep_kgNha':np.array(df_totNdep_kgNha[yr_to_plot]),'CNTRY_NAME':shapefile['CNTRY_NAME']})

    #df_new = df_ndep.fillna(0)
    shapefile_m = shapefile.merge(df_ndep_map_kgNha,on='CNTRY_NAME')

    # plotting the map
    ax = shapefile_m.plot(color="grey")
    shapefile_m.dropna().plot(ax = ax, column = "Ndep_kgNha",legend = True, cmap ='jet', legend_kwds={'label': "N deposition (kgN/ha)",'orientation': "horizontal" }
                              ,vmax = 20, vmin = 0  )
    ax.set_title("N deposition (kgN/ha) {0} ".format(yr_to_plot))
    #(missing values \nare plotted in grey)
    plt.savefig(r".\Results\Yearly_Maps_2019_2050\TotalNdep\Ndep_{0}_kgNha_m.png".format(yr_to_plot), dpi=200)
