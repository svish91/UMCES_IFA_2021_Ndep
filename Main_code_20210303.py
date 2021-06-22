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

# NOx
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Test_output_files_Yr2000'
file_name = "NOx_yr2000"
crfile_name = "Cropland2000AD"
xx_NOx=f_aggDataSimple(file_dir,file_name, crfile_name)

# total for year 2000
yy = xx_NOx[0]*xx_NOx[1]
NOx2000_total = np.nansum(xx_NOx[0]*xx_NOx[1])*1e-9

plt.figure()
pts = plt.scatter(xx_NOx[1],xx_NOx[0])
for i in range(0,len(xx_NOx[0])):
    plt.annotate(shapefile['ISO3'][i],(xx_NOx[1][i],xx_NOx[0][i]))
pts.remove()
plt.xlabel('Cropland area (km2)')
plt.ylabel('NOx Deposition 2000 (kg N km-2 yr-1)')


# NHx
file_dir = r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Test_output_files_Yr2000'
file_name = "NHx2000"
crfile_name = "Cropland2000AD"
xx_NHy=f_aggDataSimple(file_dir,file_name, crfile_name)

# total for year 2000
yy = xx_NHy[0]*xx_NHy[1]
NOx2000_total = np.nansum(xx_NHy[0]*xx_NHy[1])*1e-9

plt.figure()
pts = plt.scatter(xx_NOx[1],xx_NOx[0])
for i in range(0,len(xx_NOx[0])):
    plt.annotate(shapefile['ISO3'][i],(xx_NHy[1][i],xx_NHy[0][i]))
pts.remove()
plt.xlabel('Cropland area (km2)')
plt.ylabel('NHy Deposition 2000 (kg N km-2 yr-1)')


## total N deposition
xx_kgN = xx_NOx[0]*xx_NOx[1]+xx_NHy[0]*xx_NHy[1]
xx_kgNkm = (xx_NOx[0]*xx_NOx[1]+xx_NHy[0]*xx_NHy[1])/xx_NHy[1]
df = pd.DataFrame({'Ndep_kgN':xx_kgN,'Ndep_kgNkm':xx_kgNkm,'NOx_kgNkm':xx_NOx[0],
                   'NHy_kgNkm':xx_NHy[0],'CroplandArea_NOx': xx_NOx[1],'CroplandArea_NHy': xx_NHy[1],'CNTRY_NAME':shapefile['CNTRY_NAME']})
rslt_df = df.sort_values(by = 'Ndep_kgNkm')
#rslt_df.to_csv("Year_2000_m.csv")

## plotting map: total N kgN
#df_ndep = pd.DataFrame({'Ndep_kgN':xx_kgN,'ISO3':shapefile['ISO3']})
df_ndep = pd.DataFrame({'Ndep_kgN':df['Ndep_kgN'],'ISO3':shapefile['ISO3']})

#df_new = df_ndep.fillna(0)
shapefile_m = shapefile.merge(df_ndep,on='ISO3')

# plotting the map
ax = shapefile_m.plot(color="grey")
shapefile_m.dropna().plot(ax = ax, column = "Ndep_kgN",legend = True, cmap ='jet', legend_kwds={'label': "N deposition (kgN)",'orientation': "horizontal" },
                )
ax.set_title("N deposition (kgN) 2000 (= missing values) \nare plotted in grey");

plt.savefig("Ndep_2000_kgN.png", dpi=200)


## plotting map: total N kgN/ha
#df_ndep = pd.DataFrame({'Ndep_kgN':xx_kgN,'ISO3':shapefile['ISO3']})
df_ndep_kgNha = pd.DataFrame({'Ndep_kgNha':df['Ndep_kgNkm']/100,'CNTRY_NAME':shapefile['CNTRY_NAME']})

#df_new = df_ndep.fillna(0)
shapefile_m = shapefile.merge(df_ndep_kgNha,on='CNTRY_NAME')

# plotting the map
ax = shapefile_m.plot(color="grey")
shapefile_m.dropna().plot(ax = ax, column = "Ndep_kgNha",legend = True, cmap ='jet', legend_kwds={'label': "N deposition (kgN/ha)",'orientation': "horizontal" },
                )
ax.set_title("N deposition (kgN/ha) 2000 (= missing values) \nare plotted in grey");

plt.savefig("Ndep_2000_kgNha.png", dpi=200)

# NOx map
## plotting map kg km2

#df = pd.read_csv('Year_2000.csv')
df_NOx = pd.DataFrame({'NOx_kgNkm':df['NOx_kgNkm'],'CNTRY_NAME':shapefile['CNTRY_NAME']})
#df_new = df_ndep.fillna(0)
shapefile_m = shapefile.merge(df_NOx,on='CNTRY_NAME')

# plotting the map
ax = shapefile_m.plot(color="grey")
shapefile_m.dropna().plot(ax = ax, column = "NOx_kgNkm",legend = True, cmap ='jet', legend_kwds={'label': "NOy deposition (kgN/km2)",'orientation': "horizontal" },
                )
ax.set_title("NOy deposition (kgN/km2) 2000 (= missing values) \nare plotted in grey")
#
## save fig
plt.savefig("NOy_2000_kgkm.png", dpi=200)


## plotting map kg ha

#df = pd.read_csv('Year_2000.csv')
df_NOx = pd.DataFrame({'NOx_kgNha':df['NOx_kgNkm']/100,'CNTRY_NAME':shapefile['CNTRY_NAME']})
#df_new = df_ndep.fillna(0)
shapefile_m = shapefile.merge(df_NOx,on='CNTRY_NAME')

# plotting the map
ax = shapefile_m.plot(color="grey")
shapefile_m.dropna().plot(ax = ax, column = "NOx_kgNha",legend = True, cmap ='jet', legend_kwds={'label': "NOy deposition (kgN/ha)",'orientation': "horizontal" },
                )
ax.set_title("NOy deposition (kgN/ha) 2000 (= missing values) \nare plotted in grey")
#
## save fig
plt.savefig("NOy_2000_kgha.png", dpi=200)

# kgN
#df = pd.read_csv('Year_2000.csv')
df_NOx = pd.DataFrame({'NOx_kgN':df['NOx_kgNkm']*df['CroplandArea_NOx'],'CNTRY_NAME':shapefile['CNTRY_NAME']})
#df_new = df_ndep.fillna(0)
shapefile_m = shapefile.merge(df_NOx,on='CNTRY_NAME')

# plotting the map
ax = shapefile_m.plot(color="grey")
shapefile_m.dropna().plot(ax = ax, column = "NOx_kgN",legend = True, cmap ='jet', legend_kwds={'label': "NOy deposition (kgN)",'orientation': "horizontal" },
                )
ax.set_title("NOy deposition (kgN) 2000 (= missing values) \nare plotted in grey");
#
## save fig
plt.savefig("NOy_2000_kgN.png", dpi=200)



# NHx kg km 2
df_NHy = pd.DataFrame({'NHy_kgN':df['NHx_kgNkm'],'CNTRY_NAME':shapefile['CNTRY_NAME']})
#df_new = df_ndep.fillna(0)
shapefile_m = shapefile.merge(df_NHy,on='CNTRY_NAME')

# plotting the map
ax = shapefile_m.plot(color="grey")
shapefile_m.dropna().plot(ax = ax, column = "NHy_kgN",legend = True, cmap ='jet', legend_kwds={'label': "NHy deposition (kgN/km2)",'orientation': "horizontal" },
                )
ax.set_title("NHy deposition (kgN/km2) 2000 (= missing values) \nare plotted in grey");
#
## save fig
plt.savefig("NHy_2000_kgkm.png", dpi=200)

# NHy kgN
df_NHy = pd.DataFrame({'NHy_kgN':df['NHy_kgNkm']*df['CroplandArea_NHy'],'CNTRY_NAME':shapefile['CNTRY_NAME']})
#df_new = df_ndep.fillna(0)
shapefile_m = shapefile.merge(df_NHy,on='CNTRY_NAME')

# plotting the map
ax = shapefile_m.plot(color="grey")
shapefile_m.dropna().plot(ax = ax, column = "NHy_kgN",legend = True, cmap ='jet', legend_kwds={'label': "NHy deposition (kgN)",'orientation': "horizontal" },
                )
ax.set_title("NHy deposition (kgN) 2000 (= missing values) \nare plotted in grey");
#
## save fig
plt.savefig("NHy_2000_kgN.png", dpi=200)


#cmap-Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r