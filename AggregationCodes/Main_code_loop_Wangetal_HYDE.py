from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp


shapefile = gp.read_file(r"99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
df_totNdep_kgNha= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])

#yrN = [1960,1970,1980,1990,1997,1998,1999,np.arange(2000,2014,1)]
yrN = [1970,1980,1990,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013]

for yr in yrN:
    print(yr)
    if yr > 1960 and yr <=1965:
        yrcr = 1960
    elif yr > 1965 and yr <=1975:
        yrcr=1970
    elif yr > 1975 and yr <= 1985:
        yrcr = 1980
    elif yr > 1985 and yr <=1995:
        yrcr = 1990
    elif yr > 1995 and yr <=2000:
        yrcr = 2000
    elif yr == 2018:
        yrcr = 2017
    else:
        yrcr=yr
    idx_yr = np.where(np.arange(1961,2019,1)==yr)[0]
    file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
    file_name = "ndep_{0}".format(yr)
    crfile_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_HYDE\For Zhou'
    crfile_name = "Cropland{0}AD_HYDE_Zhou".format(yrcr)
    Ndep_tmp = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    # cropland
    df_cropland_km2[yr] = Ndep_tmp[1]
    # total
    df_totNdep_kgNha[yr] = Ndep_tmp[0]/100

df_totNdep_kgNha_trans = df_totNdep_kgNha.T


# time seris plot
for co in range(0,len(shapefile['CNTRY_NAME'])):
    plt.clf()
    #plt.figure()
    plt.scatter(np.arange(1961,2019,1),df_totNdep_kgNha_trans[shapefile['CNTRY_NAME'][co]],color = 'red')
    plt.xlim(1961,2018)
    plt.ylabel('Total N Deposition (kgN/ha)')
    plt.xlabel('Years')
    plt.title(shapefile['CNTRY_NAME'][co])
    plt.ylim([0,40])
    plt.savefig(r"Time_Series_Co_1961_2018\TotNdep_{0}_kgNha.png".format(shapefile['CNTRY_NAME'][co]), dpi=200)


df_totNdep_kgNha.to_csv("df_totNdep_kgNha.csv")
df_cropland_km2.to_csv("df_cropland_km2.csv")

# plotting map
df_totNdep_kgNha.loc['Taiwan'] = df_totNdep_kgNha.loc['China']
## plotting map: total N kgN/ha
#df_ndep = pd.DataFrame({'Ndep_kgN':xx_kgN,'ISO3':shapefile['ISO3']})
for yr_to_plot in np.arange(1961,2019,1):
    plt.clf()
    df_ndep_map_kgNha = pd.DataFrame({'Ndep_kgNha':np.array(df_totNdep_kgNha[yr_to_plot]),'CNTRY_NAME':shapefile['CNTRY_NAME']})

    #df_new = df_ndep.fillna(0)
    shapefile_m = shapefile.merge(df_ndep_map_kgNha,on='CNTRY_NAME')

    # plotting the map
    ax = shapefile_m.plot(color="grey")
    shapefile_m.dropna().plot(ax = ax, column = "Ndep_kgNha",legend = True, cmap ='jet', legend_kwds={'label': "N deposition (kgN/ha)",'orientation': "horizontal" }
                              ,vmax = 30, vmin = 0  )
    ax.set_title("N deposition (kgN/ha) {0} ".format(yr_to_plot))
    #(missing values \nare plotted in grey)
    plt.savefig(r"Yearly_Maps_1961_2018\Ndep_{0}_kgNha.png".format(yr_to_plot), dpi=200)

