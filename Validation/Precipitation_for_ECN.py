import netCDF4 as nc
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from rasterio.windows import Window
from rasterio.transform import from_origin
import rasterio
import pydap.client
from datetime import date, timedelta


file_dir = r'D:\GoogleDrive\Data_for_NetworkAnalysis\Network_analysis_files\Original Files from ERA-Reanalysis'
suffix = ".nc"
nc_f = os.path.join(file_dir,"TotalPrecip_RawData_1979toPresent" + suffix)
nc_fid_P = nc.Dataset(nc_f, 'r')  # Dataset is the class behavior to open the file
                             # and create an instance of the ncCDF4 class
P_lon = nc_fid_P.variables['longitude'][:]
P_lat = nc_fid_P.variables['latitude'][:]
P_time = nc_fid_P.variables['time'][:]
#tp = nc_fid_P.variables['tp'][:] # takes too long to load
tp_unit = nc_fid_P.variables['tp'].units

idx = np.arange(0,26298,2)
P_total = np.empty((len(idx),len(P_lat),len(P_lon)),)

for i in range(0,len(idx)):
    print(i)
    if i == (len(idx)-1):
        # finding non nan values. There will be false when NaN will be there. Otherwise, True will be there
        idxtmp = (nc_fid_P.variables['tp'][idx[i]:26298, :, :] >0)#!= -32767)
        # finding nan index
        idx_false = np.where(idxtmp == False)
        # temporary variable for precipitation
        tmp = nc_fid_P.variables['tp'][idx[i]:26298, :, :]
        # replacing nan with nan because nan is -32767
        tmp[idx_false] = 'nan'

        # finding sum
        P_total[i, :, :] = np.nansum(tmp, axis=0)
    else:
        # finding non nan values. There will be false when NaN will be there. Otherwise, True will be there
        idxtmp = (nc_fid_P.variables['tp'][idx[i]:idx[i+1],:,:] >0)#!= -32767)
        # finding nan index
        idx_false = np.where(idxtmp == False)
        # temporary variable for precipitation
        tmp = nc_fid_P.variables['tp'][idx[i]:idx[i+1],:,:]
        # replacing nan with nan because nan is -32767
        tmp[idx_false] = 'nan'

        P_total[i,:,:] = np.nansum(tmp, axis = 0)

P_total_mmday = P_total*1000
precip_total_mmday = np.zeros((P_total_mmday.shape[0],P_total_mmday.shape[1],P_total_mmday.shape[2]), dtype = "float")
precip_total_mmday[:,:,0:240] = P_total_mmday[:,:,240:480]
precip_total_mmday[:,:,240:480] = P_total_mmday[:,:,0:240]

precip_total_inchday = precip_total_mmday*0.0393701

# checking the data
# dates
sdate = date(1979,1,1)
edate = date(2014,12,31)
delta = edate - sdate       # as timedelta

date_precip = pd.date_range(sdate,edate-timedelta(days=1),freq='d')


# T01: lat: 50:51, lon: 238:239
# T03: Lat: 47:48, lon: 231:232
# T05: lat: 52:53, lon: 235:236
# T06: lat: 51:52, lon: 239:240
# T08: lat: 51:52, lon: 238:239
# T10: lat: 51:52, lon: 238:239


# ECN data
ECN_station = pd.read_csv(r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Station DATA\ECN_UK\precipitation chemistry data 1992_2015\18b7c387-037d-4949-98bc-e8db5ef4264c\supporting-documents\ECN_QC1.csv')
NH4N_ECN_T01 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NH4N') & (ECN_station['SITECODE'] =='T01')]
NH4N_ECN_T03 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NH4N') & (ECN_station['SITECODE'] =='T03')]
NH4N_ECN_T05 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NH4N') & (ECN_station['SITECODE'] =='T05')]
NH4N_ECN_T06 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NH4N') & (ECN_station['SITECODE'] =='T06')]
NH4N_ECN_T08 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NH4N') & (ECN_station['SITECODE'] =='T08')]
NH4N_ECN_T10 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NH4N') & (ECN_station['SITECODE'] =='T10')]

NO3N_ECN_T01 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NO3N') & (ECN_station['SITECODE'] =='T01')]
NO3N_ECN_T03 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NO3N') & (ECN_station['SITECODE'] =='T03')]
NO3N_ECN_T05 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NO3N') & (ECN_station['SITECODE'] =='T05')]
NO3N_ECN_T06 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NO3N') & (ECN_station['SITECODE'] =='T06')]
NO3N_ECN_T08 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NO3N') & (ECN_station['SITECODE'] =='T08')]
NO3N_ECN_T10 = ECN_station.loc[(ECN_station['FIELDNAME'] =='NO3N') & (ECN_station['SITECODE'] =='T10')]

TotalN_ECN_T01 = ECN_station.loc[(ECN_station['FIELDNAME'] =='TOTALN') & (ECN_station['SITECODE'] =='T01')]
TotalN_ECN_T03 = ECN_station.loc[(ECN_station['FIELDNAME'] =='TOTALN') & (ECN_station['SITECODE'] =='T03')]
TotalN_ECN_T05 = ECN_station.loc[(ECN_station['FIELDNAME'] =='TOTALN') & (ECN_station['SITECODE'] =='T05')]
TotalN_ECN_T06 = ECN_station.loc[(ECN_station['FIELDNAME'] =='TOTALN') & (ECN_station['SITECODE'] =='T06')]
TotalN_ECN_T08 = ECN_station.loc[(ECN_station['FIELDNAME'] =='TOTALN') & (ECN_station['SITECODE'] =='T08')]
TotalN_ECN_T10 = ECN_station.loc[(ECN_station['FIELDNAME'] =='TOTALN') & (ECN_station['SITECODE'] =='T10')]

#TotalN_ECN_T01.loc[TotalN_ECN_T01['SDATE']=='23-Aug-12']
#ECN_station["SDATE"]= pd.to_datetime(ECN_station.SDATE)

# T01
TotalN_ECN_T01["SDATE"]= pd.to_datetime(TotalN_ECN_T01['SDATE'])#,format='%Y%m%d')
#idx = TotalN_ECN_T01.loc[(TotalN_ECN_T01['SDATE']==date_precip[0])]

idx_commonT01 = date_precip.intersection(TotalN_ECN_T01["SDATE"])
TotalN_ECN_T01_kgNhaday = np.empty(idx_commonT01.shape)

for dd in range(0,len(idx_commonT01)):
    idx_precip = np.where(date_precip==idx_commonT01[dd])
    idx_Ndep_T01 = np.where(TotalN_ECN_T01["SDATE"]==idx_commonT01[dd])
    precip_T01 = np.nanmean(precip_total_inchday[idx_precip[0], 50:51,238:239])
    TotalN_ECN_T01_kgNhaday[dd] = np.nanmean(TotalN_ECN_T01.loc[(TotalN_ECN_T01["SDATE"]==idx_commonT01[dd])]['VALUE'])*precip_T01*0.253

plt.boxplot(TotalN_ECN_T01_kgNhaday)

TotalN_ECN_T01_kgNhayr = np.empty(np.unique(idx_commonT01.year).shape)
for y in range(0,len(np.unique(idx_commonT01.year))):
    idx_yr = np.where(idx_commonT01.year==np.unique(idx_commonT01.year)[y])
    TotalN_ECN_T01_kgNhayr[y] = 365*np.nanmean(TotalN_ECN_T01_kgNhaday[idx_yr[0]])
plt.boxplot(TotalN_ECN_T01_kgNhayr)

# T03
TotalN_ECN_T03["SDATE"]= pd.to_datetime(TotalN_ECN_T03['SDATE'])#,format='%Y%m%d')
idx = TotalN_ECN_T03.loc[(TotalN_ECN_T03['SDATE']==date_precip[0])]

idx_commonT03 = date_precip.intersection(TotalN_ECN_T03["SDATE"])
TotalN_ECN_T03_kgNhaday = np.empty(idx_commonT03.shape)

for dd in range(0,len(idx_commonT03)):
    idx_precip = np.where(date_precip==idx_commonT03[dd])
    precip_T03 = np.nanmean(precip_total_inchday[idx_precip[0], 47:48,231:232])
    TotalN_ECN_T03_kgNhaday[dd] = np.nanmean(TotalN_ECN_T03.loc[(TotalN_ECN_T03["SDATE"]==idx_commonT03[dd])]['VALUE'])*precip_T03*0.253

plt.boxplot(TotalN_ECN_T03_kgNhaday)

TotalN_ECN_T03_kgNhayr = np.empty(np.unique(idx_commonT03.year).shape)
for y in range(0,len(np.unique(idx_commonT03.year))):
    idx_yr = np.where(idx_commonT03.year==np.unique(idx_commonT03.year)[y])
    TotalN_ECN_T03_kgNhayr[y] = 365*np.nanmean(TotalN_ECN_T03_kgNhaday[idx_yr[0]])
plt.boxplot(TotalN_ECN_T03_kgNhayr)


# T05
TotalN_ECN_T05["SDATE"]= pd.to_datetime(TotalN_ECN_T05['SDATE'])#,format='%Y%m%d')
idx_commonT05 = date_precip.intersection(TotalN_ECN_T05["SDATE"])
TotalN_ECN_T05_kgNhaday = np.empty(idx_commonT05.shape)

for dd in range(0,len(idx_commonT05)):
    idx_precip = np.where(date_precip==idx_commonT05[dd])
    precip_T05 = np.nanmean(precip_total_inchday[idx_precip[0], 47:48,231:232])
    TotalN_ECN_T05_kgNhaday[dd] = np.nanmean(TotalN_ECN_T05.loc[(TotalN_ECN_T05["SDATE"]==idx_commonT05[dd])]['VALUE'])*precip_T05*0.253

plt.boxplot(TotalN_ECN_T05_kgNhaday)


TotalN_ECN_T05_kgNhayr = np.empty(np.unique(idx_commonT05.year).shape)
for y in range(0,len(np.unique(idx_commonT05.year))):
    idx_yr = np.where(idx_commonT05.year==np.unique(idx_commonT05.year)[y])
    TotalN_ECN_T05_kgNhayr[y] = 365*np.nanmean(TotalN_ECN_T05_kgNhaday[idx_yr[0]])
plt.boxplot(TotalN_ECN_T05_kgNhayr)


# T06
TotalN_ECN_T06["SDATE"]= pd.to_datetime(TotalN_ECN_T06['SDATE'])#,format='%Y%m%d')
idx_commonT06 = date_precip.intersection(TotalN_ECN_T06["SDATE"])
TotalN_ECN_T06_kgNhaday = np.empty(idx_commonT06.shape)

for dd in range(0,len(idx_commonT06)):
    idx_precip = np.where(date_precip==idx_commonT06[dd])
    precip_T06 = np.nanmean(precip_total_inchday[idx_precip[0], 51:52,239:240])
    TotalN_ECN_T06_kgNhaday[dd] = np.nanmean(TotalN_ECN_T06.loc[(TotalN_ECN_T06["SDATE"]==idx_commonT06[dd])]['VALUE'])*precip_T06*0.253

plt.boxplot(TotalN_ECN_T06_kgNhaday)

TotalN_ECN_T06_kgNhayr = np.empty(np.unique(idx_commonT06.year).shape)
for y in range(0,len(np.unique(idx_commonT06.year))):
    idx_yr = np.where(idx_commonT06.year==np.unique(idx_commonT06.year)[y])
    TotalN_ECN_T06_kgNhayr[y] = 365*np.nanmean(TotalN_ECN_T06_kgNhaday[idx_yr[0]])
plt.boxplot(TotalN_ECN_T06_kgNhayr)


# T08
TotalN_ECN_T08["SDATE"]= pd.to_datetime(TotalN_ECN_T08['SDATE'])#,format='%Y%m%d')
idx_commonT08 = date_precip.intersection(TotalN_ECN_T08["SDATE"])
TotalN_ECN_T08_kgNhaday = np.empty(idx_commonT08.shape)

for dd in range(0,len(idx_commonT08)):
    idx_precip = np.where(date_precip==idx_commonT08[dd])
    precip_T08 = np.nanmean(precip_total_inchday[idx_precip[0], 51:52,238:239])
    TotalN_ECN_T08_kgNhaday[dd] = np.nanmean(TotalN_ECN_T08.loc[(TotalN_ECN_T08["SDATE"]==idx_commonT08[dd])]['VALUE'])*precip_T08*0.253

plt.boxplot(TotalN_ECN_T08_kgNhaday)

TotalN_ECN_T08_kgNhayr = np.empty(np.unique(idx_commonT08.year).shape)
for y in range(0,len(np.unique(idx_commonT08.year))):
    idx_yr = np.where(idx_commonT08.year==np.unique(idx_commonT08.year)[y])
    TotalN_ECN_T08_kgNhayr[y] = 365*np.nanmean(TotalN_ECN_T08_kgNhaday[idx_yr[0]])
plt.boxplot(TotalN_ECN_T08_kgNhayr)


# T10
TotalN_ECN_T10["SDATE"]= pd.to_datetime(TotalN_ECN_T10['SDATE'])#,format='%Y%m%d')
idx_commonT10 = date_precip.intersection(TotalN_ECN_T10["SDATE"])
TotalN_ECN_T10_kgNhaday = np.empty(idx_commonT10.shape)

for dd in range(0,len(idx_commonT10)):
    idx_precip = np.where(date_precip==idx_commonT10[dd])
    precip_T10 = np.nanmean(precip_total_inchday[idx_precip[0], 51:52,238:239])
    TotalN_ECN_T10_kgNhaday[dd] = np.nanmean(TotalN_ECN_T10.loc[(TotalN_ECN_T10["SDATE"]==idx_commonT10[dd])]['VALUE'])*precip_T10*0.253

plt.boxplot(TotalN_ECN_T10_kgNhaday)

TotalN_ECN_T10_kgNhayr = np.empty(np.unique(idx_commonT10.year).shape)
for y in range(0,len(np.unique(idx_commonT10.year))):
    idx_yr = np.where(idx_commonT10.year==np.unique(idx_commonT10.year)[y])
    TotalN_ECN_T10_kgNhayr[y] = 365*np.nanmean(TotalN_ECN_T10_kgNhaday[idx_yr[0]])
plt.boxplot(TotalN_ECN_T10_kgNhayr)


### plotting


# idx_commonT01.year : 1996 - 2012
# idx_commonT05.year : 2003 - 2014
# idx_commonT06.year : 2005 - 2007
# idx_commonT08.year : 1996 - 2012

df_totNdep_kgNhayr_Stn = pd.DataFrame(np.nan, index=np.arange(4), columns=np.arange(1961,2019,1))
df_totNdep_kgNhayr_Stn.loc[0,np.unique(idx_commonT01.year)] = TotalN_ECN_T01_kgNhayr
df_totNdep_kgNhayr_Stn.loc[1,np.unique(idx_commonT05.year)] = TotalN_ECN_T05_kgNhayr
df_totNdep_kgNhayr_Stn.loc[2,np.unique(idx_commonT06.year)] = TotalN_ECN_T06_kgNhayr
df_totNdep_kgNhayr_Stn.loc[3,np.unique(idx_commonT08.year)] = TotalN_ECN_T08_kgNhayr
df_totNdep_kgNhayr_Stn.to_csv('ECN_station_kgNhayr_m.csv')

df_totNdep_kgNhayr_Stn = pd.read_csv('ECN_station_kgNhayr.csv').iloc[:, 1:]
# 230 is the index for united kingdom
df_totNdep_ACCMIP_Hyde = pd.read_csv(r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\ACCMIP\HYDE\df_totNdep_kgNha.csv').iloc[:, 1:]
df_totNdep_ACCMIP_LUH2 = pd.read_csv(r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\ACCMIP\LUH2\df_totNdep_kgNha.csv').iloc[:, 1:]
df_totNdep_Zhou_LUH2 = pd.read_csv(r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\ZhouFeng\LUH2\df_totNdep_kgNha.csv').iloc[:, 1:]
df_totNdep_Zhou_Hyde = pd.read_csv(r'D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Results\ZhouFeng\HYDE\df_totNdep_kgNha.csv').iloc[:, 1:]

df_totNdep_ACCMIP_Hyde_UK = pd.DataFrame(df_totNdep_ACCMIP_Hyde.loc[230,:])
df_totNdep_ACCMIP_Hyde_UK.reset_index(inplace=True)
df_totNdep_ACCMIP_Hyde_UK.columns= ['Year', 'UK']

df_totNdep_ACCMIP_LUH2_UK = pd.DataFrame(df_totNdep_ACCMIP_LUH2.loc[230,:])
df_totNdep_ACCMIP_LUH2_UK.reset_index(inplace=True)
df_totNdep_ACCMIP_LUH2_UK.columns= ['Year', 'UK']

df_totNdep_Zhou_LUH2_UK = pd.DataFrame(df_totNdep_Zhou_LUH2.loc[230,:])
df_totNdep_Zhou_LUH2_UK.reset_index(inplace=True)
df_totNdep_Zhou_LUH2_UK.columns= ['Year', 'UK']

df_totNdep_Zhou_Hyde_UK = pd.DataFrame(df_totNdep_Zhou_Hyde.loc[230,:])
df_totNdep_Zhou_Hyde_UK.reset_index(inplace=True)
df_totNdep_Zhou_Hyde_UK.columns= ['Year', 'UK']

df_concat_totNdep = pd.concat([df_totNdep_ACCMIP_Hyde_UK['UK'],df_totNdep_ACCMIP_LUH2_UK['UK'],df_totNdep_Zhou_LUH2_UK['UK'],df_totNdep_Zhou_Hyde_UK['UK']], axis = 1)
df_concat_totNdep.columns = ['ACCMIP HYDE','ACCMIP LUH2','Zhou LUH2','Zhou HYDE']

import seaborn as sns
#fig, ax = sns.plt.subplots()
plt.figure(figsize=(10,8))

g = sns.boxplot(x="variable", y="value", data=pd.melt(df_totNdep_kgNhayr_Stn),color ='white')
g.set_xticklabels(g.get_xticklabels(),rotation=90)
plt.setp(g.artists, edgecolor = 'k', facecolor='w')
plt.setp(g.lines, color='k')

p1 = sns.scatterplot(x='Year',y='UK', data = df_totNdep_ACCMIP_Hyde_UK)
p2 = sns.scatterplot(x='Year',y='UK', data = df_totNdep_ACCMIP_LUH2_UK)
p3 = sns.scatterplot(x='Year',y='UK', data = df_totNdep_Zhou_LUH2_UK)
p4 = sns.scatterplot(x='Year',y='UK', data = df_totNdep_Zhou_Hyde_UK)
g.set(xlabel='Year', ylabel='N Deposition ($kg N ha^{-1}$)')

#l = plt.legend(p1.get_legend_handles_labels(), 'xx', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
plt.savefig(r"D:\GoogleDrive\N_deposition_project\Gridded DATA\Data_Organization\Station DATA\ECN_UK\precipitation chemistry data 1992_2015\18b7c387-037d-4949-98bc-e8db5ef4264c\supporting-documents\TotNdep_kgNhayr_stn.pdf", dpi=300)
plt.close()
