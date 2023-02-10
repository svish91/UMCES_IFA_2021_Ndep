## aggregation to national scale
from f_aggDataSimple import f_aggDataSimple
import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gp

### aggregating Zhou F and LUH2
shapefile = gp.read_file(r"G:\My Drive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                             r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
# df_NOx_kgNha = pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NOx_kgNha = df_NOx_kgNha.rename(index = shapefile['CNTRY_NAME'])
# df_NHy_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NHy_kgNha = df_NHy_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_totNdep_kgNha= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=np.arange(1961,2021,1))
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=np.arange(1961,2021,1))
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])

yrN = np.arange(1961,2021)#[1970,1980,1990,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
#np.arange(1997, 2019)
for yr in yrN:
    print(yr)
    if yr > 2013:
        yrcr = 2015
    else:
        yrcr = yr
    #idx_yr = np.where(np.arange(1961,2021,1)==yr)[0]
    # adjusting file locations for N dep
    if (yr == 1970)  or (yr == 1980)  or (yr == 1990) or (yr == 1997):
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
        file_name = "ndep_{0}".format(yr)
    elif yr < 1970:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period'
        file_name = "ndep_ep_{0}_wNeg_interp".format(yr)
    elif (yr < 1997) and (yr > 1970):
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period_newApproach'
        file_name = "ndep_ep_{0}_wNeg_interp_na".format(yr)
    elif (yr > 2013) & (yr <=2018):
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
        file_name = "ndep_ep_{0}_wNeg_extrp".format(yr) # change this if not including negative values
    elif yr > 2018:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
        file_name = "ndep_ep_{0}_wNeg_extrp".format(2018)  # change this if not including negative values
    else:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
        file_name = "ndep_{0}".format(yr)

    crfile_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2\For_Zhou\Modified'
    crfile_name = "Cropland_yr{0}_LUH_Zhou".format(yrcr)
    Ndep_tmp = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    # cropland
    df_cropland_km2[yr] = Ndep_tmp[1]
    # total
    df_totNdep_kgNha[yr] = Ndep_tmp[0]/100

df_totNdep_kgNha_trans = df_totNdep_kgNha.T
#df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission.csv") # use this if using non-negative values for aggregation
df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission_wNeg_ZhouLUH2_fillGaps_na.csv")

df_cropland_km2.to_csv("df_cropland_km2_ExtendedPeriod_usingEmission_wNeg_ZhouLUH2_fillGaps_na.csv")

(df_totNdep_kgNha < 0).any().any()
# time seris plot
for co in range(0,len(shapefile['CNTRY_NAME'])):
    plt.clf()
    #plt.figure()
    plt.plot(np.arange(1961,2021,1),df_totNdep_kgNha_trans[shapefile['CNTRY_NAME'][co]],color = 'black')
    plt.xlim(1961,2020)
    plt.ylabel('Total N Deposition (kgN/ha)')
    plt.xlabel('Years')
    plt.title(shapefile['CNTRY_NAME'][co])
    plt.ylim([0,40])
    plt.savefig(r"G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Complete_TS\New_approach\TotNdep_{0}_kgNha_EP_Na.png".format(shapefile['CNTRY_NAME'][co]), dpi=200)



#### aggregating Zhou and HYDE map
shapefile = gp.read_file(r"G:\My Drive\Data_for_NetworkAnalysis\Country Boundaries\Longitude_Graticules_and_World_Countries_Boundaries-shp"
                             r"\99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp")
# columns: OBJECTID	CNTRY_NAME
# df_NOx_kgNha = pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NOx_kgNha = df_NOx_kgNha.rename(index = shapefile['CNTRY_NAME'])
# df_NHy_kgNha= pd.DataFrame(0, index=np.arange(len(shapefile)), columns=np.arange(1961,2019,1))
# df_NHy_kgNha = df_NHy_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_totNdep_kgNha= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=np.arange(1961,2021,1))
df_totNdep_kgNha = df_totNdep_kgNha.rename(index = shapefile['CNTRY_NAME'])
df_cropland_km2= pd.DataFrame(np.nan, index=np.arange(len(shapefile)), columns=np.arange(1961,2021,1))
df_cropland_km2 = df_cropland_km2.rename(index = shapefile['CNTRY_NAME'])

yrN = np.arange(1961,2021)

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
    elif yr >= 2018:
        yrcr = 2017
    else:
        yrcr=yr
    idx_yr = np.where(np.arange(1961,2021,1)==yr)[0]
    if (yr == 1970) or (yr == 1980) or (yr == 1990) or (yr == 1997):
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
        file_name = "ndep_{0}".format(yr)
    elif yr < 1970:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period'
        file_name = "ndep_ep_{0}_wNeg_interp".format(yr)
    elif (yr < 1997) and (yr > 1970):
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period_newApproach'
        file_name = "ndep_ep_{0}_wNeg_interp_na".format(yr)
    elif (yr > 2013) & (yr <= 2018):
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
        file_name = "ndep_ep_{0}_wNeg_extrp".format(yr)  # change this if not including negative values
    elif yr > 2018:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
        file_name = "ndep_ep_{0}_wNeg_extrp".format(2018)  # change this if not including negative values
    else:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
        file_name = "ndep_{0}".format(yr)

    crfile_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_HYDE\For Zhou'
    crfile_name = "Cropland{0}AD_HYDE_Zhou".format(yrcr)
    Ndep_tmp = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    # cropland
    df_cropland_km2[yr] = Ndep_tmp[1]
    # total
    df_totNdep_kgNha[yr] = Ndep_tmp[0]/100

df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission_wNeg_ZhouHYDE_fillGaps_na.csv")
df_cropland_km2.to_csv("df_Cropland_km2_ExtendedPeriod_usingEmission_wNeg_ZhouHYDE_fillGaps_na.csv")

(df_totNdep_kgNha < 0).any().any()
df_totNdep_kgNha_trans = df_totNdep_kgNha.T

# time seris plot
for co in range(0,len(shapefile['CNTRY_NAME'])):
    plt.clf()
    #plt.figure()
    plt.plot(np.arange(1961,2021,1),df_totNdep_kgNha_trans[shapefile['CNTRY_NAME'][co]],color = 'black')
    plt.xlim(1961,2020)
    plt.ylabel('Total N Deposition (kgN/ha)')
    plt.xlabel('Years')
    plt.title(shapefile['CNTRY_NAME'][co])
    plt.ylim([0,40])
    plt.savefig(r"G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Complete_TS\New_appraoch_Zhou_HYDE\TotNdep_{0}_kgNha_EP_Na.png".format(shapefile['CNTRY_NAME'][co]), dpi=200)

### base code: do no run now
yrN = [1970,1980,1990,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
#np.arange(1997, 2019)
for yr in yrN:
    print(yr)
    if yr > 2013:
        yrcr = 2015
    else:
        yrcr = yr
    idx_yr = np.where(np.arange(1961,2019,1)==yr)[0]
    if yr > 2013:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
        file_name = "ndep_ep_{0}_wNeg".format(yr) # change this if not including negative values
    else:
        file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
        file_name = "ndep_{0}".format(yr)
    crfile_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\Modified_Raster_Files\Cropland_LUH2\For_Zhou\Modified'
    crfile_name = "Cropland_yr{0}_LUH_Zhou".format(yrcr)
    Ndep_tmp = f_aggDataSimple(file_dir,file_name,crfile_dir, crfile_name)
    # cropland
    df_cropland_km2[yr] = Ndep_tmp[1]
    # total
    df_totNdep_kgNha[yr] = Ndep_tmp[0]/100

df_totNdep_kgNha_trans = df_totNdep_kgNha.T
#df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission.csv") # use this if using non-negative values for aggregation
#df_totNdep_kgNha.to_csv("df_totNdep_kgNha_ExtendedPeriod_usingEmission_wNeg.csv")


# if (yr == 1970) or (yr == 1980) or (yr == 1990):
#     file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
#     file_name = "ndep_{0}".format(yr)
# elif (yr < 1970) or ((yr > 1970) and (yr < 1980)) or ((yr > 1980) and (yr < 1990)) or ((yr > 1990) and (yr <= 1996)):
#     file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period\Interpolated_period_newApproach'
#     file_name = "ndep_ep_{0}_wNeg_interp".format(yr)
# elif (yr > 2013) & (yr <= 2018):
#     file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
#     file_name = "ndep_ep_{0}_wNeg_extrp".format(yr)  # change this if not including negative values
# elif yr > 2018:
#     file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\Data_Organization\N_emission_data_using_textfile\Raster_file_Zhou_extended_period'
#     file_name = "ndep_ep_{0}_wNeg_extrp".format(2018)  # change this if not including negative values
# else:
#     file_dir = r'G:\My Drive\N_deposition_project\Gridded DATA\N_deposition\N_deposition_global_ZHOUF\N_deposition_global_ZHOUF'
#     file_name = "ndep_{0}".format(yr)