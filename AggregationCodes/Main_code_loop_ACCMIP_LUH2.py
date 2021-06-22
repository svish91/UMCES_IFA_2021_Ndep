from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp


shapefile = gp.read_file(r"D:\GoogleDrive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                             r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
df_NOx_kgNha = pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
df_NOx_kgNha = df_NOx_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_NHy_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
df_NHy_kgNha = df_NHy_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_totNdep_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])
# NOx
for yr in np.arange(1961,2019,1):
    print(yr)
    if yr > 2015:
        yrcr = 2015
    else:
        yrcr=yr
    idx_yr = np.where(np.arange(1961,2019,1)==yr)[0]
    file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Ndep_ACCMIP'
    file_name = "NOx_yr{0}".format(yr)
    crfile_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2'
    crfile_name = "Cropland_yr{0}_LUH".format(yrcr)
    xx_NOx_kgNkm = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    df_NOx_kgNha[yr] =xx_NOx_kgNkm[0]/100
    # NHx
    file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Ndep_ACCMIP'
    file_name = "NHy_yr{0}".format(yr)
    crfile_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2'
    crfile_name = "Cropland_yr{0}_LUH".format(yrcr)
    xx_NHy_kgNkm = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    df_NHy_kgNha[yr] = xx_NHy_kgNkm[0]/100
    # cropland
    df_cropland_km2[yr] = xx_NOx_kgNkm[1]
    # total
    df_totNdep_kgNha[yr] = ((xx_NOx_kgNkm[0]*xx_NOx_kgNkm[1]+xx_NHy_kgNkm[0]*xx_NHy_kgNkm[1])/xx_NHy_kgNkm[1])/100

df_totNdep_kgNha_trans = df_totNdep_kgNha.T
df_NOx_kgNha_trans = df_NOx_kgNha.T
df_NHy_kgNha_trans = df_NHy_kgNha.T
df_cropland_km2_trans = df_cropland_km2.T

# time seris plot
for co in range(0,len(shapefile['CNTRY_NAME'])):
    plt.clf()
    #plt.figure()
    plt.plot(df_totNdep_kgNha_trans[shapefile['CNTRY_NAME'][co]],color = 'red')
    plt.xlim(1961,2018)
    plt.ylabel('Total N Deposition (kgN/ha)')
    plt.xlabel('Years')
    plt.title(shapefile['CNTRY_NAME'][co])
    plt.ylim([0,20])
    plt.savefig(r"D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\LUH2\Time_Series_Co_1961_2018\TotNdep_{0}_kgNha.png".format(shapefile['CNTRY_NAME'][co]), dpi=200)

# to csv
df_totNdep_kgNha.to_csv("df_totNdep_kgNha.csv")
df_NOx_kgNha.to_csv("df_NOx_kgNha.csv")
df_NHy_kgNha.to_csv("df_NHy_kgNha.csv")
df_cropland_km2.to_csv("df_cropland_km2.csv")
#rslt_df.to_csv("Year_2000_m.csv")


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
    plt.savefig(r"D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\ACCMIP\LUH2\Yearly_maps_1961_2018_SameLim\Ndep_{0}_kgNha_m.png".format(yr_to_plot), dpi=200)


# nox
df_NOx_kgNha.loc['Taiwan'] = df_NOx_kgNha.loc['China']
## plotting map: total N kgN/ha
#df_ndep = pd.DataFrame({'Ndep_kgN':xx_kgN,'ISO3':shapefile['ISO3']})
for yr_to_plot in np.arange(1961,2019,1):
    plt.figure()
    df_ndep_map_kgNha = pd.DataFrame({'NOx_kgNha':np.array(df_NOx_kgNha[yr_to_plot]),'CNTRY_NAME':shapefile['CNTRY_NAME']})

    #df_new = df_ndep.fillna(0)
    shapefile_m = shapefile.merge(df_ndep_map_kgNha,on='CNTRY_NAME')

    # plotting the map
    ax = shapefile_m.plot(color="grey")
    shapefile_m.dropna().plot(ax = ax, column = "NOx_kgNha",legend = True, cmap ='jet', legend_kwds={'label': "NOx deposition (kgN/ha)",'orientation': "horizontal" }
                              ,vmax = 10, vmin = 0  )
    ax.set_title("NOx deposition (kgN/ha) {0} ".format(yr_to_plot))
    #(missing values \nare plotted in grey)
    plt.savefig(r"D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\LUH2\Yearly_Maps_1961_2018\NOx\NOx_{0}_kgNha_m.png".format(yr_to_plot), dpi=200)
    plt.close()

# nox
df_NHy_kgNha.loc['Taiwan'] = df_NHy_kgNha.loc['China']
## plotting map: total N kgN/ha
#df_ndep = pd.DataFrame({'Ndep_kgN':xx_kgN,'ISO3':shapefile['ISO3']})
for yr_to_plot in np.arange(1961,2019,1):
    plt.figure()
    df_ndep_map_kgNha = pd.DataFrame({'NHy_kgNha':np.array(df_NHy_kgNha[yr_to_plot]),'CNTRY_NAME':shapefile['CNTRY_NAME']})

    #df_new = df_ndep.fillna(0)
    shapefile_m = shapefile.merge(df_ndep_map_kgNha,on='CNTRY_NAME')

    # plotting the map
    ax = shapefile_m.plot(color="grey")
    shapefile_m.dropna().plot(ax = ax, column = "NHy_kgNha",legend = True, cmap ='jet', legend_kwds={'label': "NHy deposition (kgN/ha)",'orientation': "horizontal" }
                              ,vmax = 10, vmin = 0  )
    ax.set_title("NOx deposition (kgN/ha) {0} ".format(yr_to_plot))
    #(missing values \nare plotted in grey)
    plt.savefig(r"D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\LUH2\Yearly_Maps_1961_2018\NHy\NHy_{0}_kgNha_m.png".format(yr_to_plot), dpi=200)
    plt.close()


#cmap-Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r
