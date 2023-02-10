library(R.matlab)
library(reshape2)
library(readxl)
data <- readMat('G:/My Drive/N_deposition_project/Gridded DATA/Data_Organization/From_Tan_ForComparison/Ndeposition_Srishti_24-Feb-2021.mat')

#for(i in 1:length(data)) assign(names(data)[i], data[[i]]); rm(data)
for(i in c(1,4,5,6)) assign(names(data)[i], data[[i]]); rm(data)

data <- readMat('G:/My Drive/N_deposition_project/Gridded DATA/Data_Organization/From_Tan_ForComparison/Ndeposition_kgNha_Srishti_25-Feb-2021.mat')
for(i in c(1,4,5,6)) assign(names(data)[i], data[[i]]); rm(data)

uniYr = 1961:2015
idx_yr = which(uniYr==2008)
comp_Data = test.ndep.3d.kgNha[,,idx_yr]#ndep.3d.Z[,,idx_yr]

# finding the range of data in a particular year
quantile(test.ndep.3d.kgNha, na.rm=T)

# countries in Tan's data
Co_t = read.csv('Co_group_name.csv', header = FALSE)

# 115 countries
data <- readMat('C:/Users/svishwakarma/Documents/Research_Work/NitrogenBudgetData/Main_NInputYield2016_Apr2020_115Co_Apr2020.mat')
for(i in 1:length(data)) assign(names(data)[i], data[[i]]); rm(data)



# 218 countries
data <- readMat('C:/Users/svishwakarma/Documents/Research_Work/NitrogenBudgetData/Nbudget_01-Nov-2019.mat')
assign(names(data)[4], data[[4]]); rm(data)

## loading N deposition data 
file_path_dryad = 'G:/My Drive/N_deposition_project/Gridded DATA/Data_Organization/Data files for repository/Adjusting missing values using FAO/Submission filles'
WL = read_excel(paste0(file_path_dryad,'/4_WL.xlsx'))

# common m49 countries as 115
m49_115  = c(8, 12, 24, 36, 40, 50, 204, 64, 68, 72, 76, 100,854,108, 120, 124, 140, 148, 152, 156, 170, 
            174, 178, 188, 192, 384, 180, 208, 214, 218, 818, 222, 242, 246, 250, 266,270, 276, 288, 300, 320, 
            324, 624, 328, 340, 348, 356, 360, 364, 376, 380, 392, 400, 404, 418, 422, 426, 430, 450, 454, 458, 
            466, 478, 484, 496, 504, 508, 516, 524, 528, 554, 558, 562, 566, 578, 586, 591, 598, 600, 604, 
            608, 616, 620, 410, 642, 646, 682, 686, 694, 710, 724, 144, 729, 748, 752, 756, 760, 764, 768, 
            788, 792, 800, 784, 826, 834, 840, 858, 862, 704, 887, 894, 716, 231,'', 32)

# ussr merging
WL$Countries[!is.na(match(WL$Countries, unlist(FAOSTAT.CoName.15USSR)))]
WL_fsu = colMeans(WL[!is.na(match(WL$Countries, unlist(FAOSTAT.CoName.15USSR))), 3:62], na.rm = T)

#WL_subset = matrix(nrow = 115, ncol = 62)
WL_subset = WL[!is.na(match(WL$m49,m49_115)),]

WL_subset[nrow(WL_subset)+1, ]  <- NA
WL_subset[115,1] = 'USSR'
WL_subset[115,3:62] = list(WL_fsu)

## ISO to match with spatial variation
file_path_iso = 'C:/Users/svishwakarma/Documents/Research_Work/NitrogenBudgetData/'
data = readMat(paste0(file_path_iso,'FAOSTAT_CoABR_ISO.mat'))
for(i in 1:length(data)) assign(names(data)[i], data[[i]]); rm(data)
ISO_common115 = unlist(FAOSTAT.CoABR.ISO[Co.ID.group.X])
ISO_common115[114] = 'FSU' 

## plotting map
library(rworldmap)
library(RColorBrewer)
# merging FSU

MergeCo <- unlist(FAOSTAT.CoABR.ISO)[match(c("Armenia","Azerbaijan","Belarus", "Estonia", "Georgia", "Kazakhstan",
                                             "Kyrgyzstan", "Latvia" ,"Lithuania", "Republic of Moldova","Tajikistan",
                                             'Russian Federation', "Turkmenistan",
                                             "Ukraine","Uzbekistan" ), unlist(FAOSTAT.CoName.FAO))]


tmpL <- data.frame(ISO = c(unlist(ISO_common115),MergeCo), N_dep = c(comp_Data[,1], rep(comp_Data[114,1],length(MergeCo))))


tmpL <- tmpL[order(tmpL$ISO),]

sPDF <- joinCountryData2Map( tmpL
                             ,joinCode = "ISO3"
                             ,nameJoinColumn = "ISO")
clrs = brewer.pal(9,"YlOrRd")

sdm<-mapCountryData(sPDF
                    ,nameColumnToPlot = 'N_dep ',colourPalette = clrs, addLegend = F
                    , oceanCol = "lightskyblue", missingCountryCol = "lightgrey"
                    , catMethod = quantile(test.ndep.3d.kgNha[,,idx_yr], na.rm = T )#seq(0,100,20)
                    )
do.call(addMapLegend
        ,c(sdm
           ,legendLabels="all"
           ,legendWidth=0.5
           ,legendIntervals="data"
           ,legendMar = 2))
