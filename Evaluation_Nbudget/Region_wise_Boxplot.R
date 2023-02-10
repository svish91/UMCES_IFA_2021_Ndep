rm(list = ls())
library(readxl)
library(ggplot2)
library(R.matlab)
library(reshape2)
library(gridExtra)
library(lemon)

AH = read_excel('./Using_Matlab/1_AH_115Comparison_UQ_wRgn.xlsx')
AL = read_excel('./Using_Matlab/2_AL_115Comparison_UQ_wRgn.xlsx')
WH = read_excel('./Using_Matlab/3_WH_115Comparison_UQ_wRgn.xlsx')
WL = read_excel('./Using_Matlab/4_WL_115Comparison_UQ_wRgn.xlsx')

# Zhang et al. 2021
data <- readMat('./Ndeposition_kgNha_Srishti_25-Feb-2021.mat')
for(i in c(1,4,5,6)) assign(names(data)[i], data[[i]]); rm(data)
uniYr = 1961:2015
for (yr in uniYr){
    idx_yr = which(uniYr==yr)
    comp_Data = test.ndep.3d.kgNha[,,idx_yr]#ndep.3d.Z[,,idx_yr]
    
    # names 
    data <- readMat('./Ndeposition_Srishti_24-Feb-2021.mat')
    for(i in 4) assign(names(data)[i], data[[i]]); rm(data)
    
    colnames(comp_Data) = unlist(DataSource4)
    
    df_toplot_subset_yr = data.frame(Country = WL$Country, Region = WL$Region, #WL = WL$`2000`,
                                     Ndep_115 = comp_Data)
    df_toplot_subset_yr_melt = melt(df_toplot_subset_yr)
    # df_toplot_subset_yr_asia = df_toplot_subset_yr_melt[df_toplot_subset_yr_melt$Region=='Asia',]
    
    
    # data from dryad
    df_dryad_AH = data.frame(Country = WL$Country, Region = WL$Region, AH = eval(parse(text=paste0("AH$",'`',yr,'`'))))
    df_dryad_AL = data.frame(Country = WL$Country, Region = WL$Region, AL = eval(parse(text=paste0("AL$",'`',yr,'`'))))
    df_dryad_WH = data.frame(Country = WL$Country, Region = WL$Region, WH = eval(parse(text=paste0("WH$",'`',yr,'`'))))
    df_dryad_WL = data.frame(Country = WL$Country, Region = WL$Region, WL = eval(parse(text=paste0("WL$",'`',yr,'`'))))
    
    df_dryad_all = data.frame(df_dryad_AH, AL = df_dryad_AL$AL, WH =  df_dryad_WH$WH, WL = df_dryad_WL$WL)
    df_dryad_all_melt = melt(df_dryad_all)
    # df_dryad_asia = df_dryad[df_dryad$Region=='Asia',]
    
    # ggplot(NULL)+
    #     geom_boxplot(data = df_toplot_subset_yr_asia, aes(y = Country, x = value),fill = "white", colour = "darkgrey")+
    #     geom_point(data = df_dryad_asia, aes(y = Country, x = WL), color = 'black', shape = 18, size = 2)+
    #     scale_y_discrete(limits=rev)+
    #     theme_bw()
    
    jpeg(paste0('BoxPLot_AH_14comp_rgn_yr',yr,'.jpeg'),width = 16, height = 10, units = 'in', res = 400)
    print(ggplot(NULL)+
        geom_boxplot(data = df_toplot_subset_yr_melt, aes(y = Country, x = value),fill = "white", colour = "darkgrey",
                     size = 0.5)+
        geom_point(data = df_dryad_AH, aes(y = Country, x = AH, col = 'black'),  shape = 18, size = 2.5)+
        scale_y_discrete(limits=rev)+
        facet_wrap(~Region,scales = "free") +
        scale_color_manual(values = "black", label = "AH")+
        guides(color = guide_legend(title = "N deposition product"))+
        xlab(bquote('N deposition (kg N'~ ha^-1~yr^-1~')'))+
        theme_bw()+ theme(legend.position = c(0.8,0.3), 
                          #        legend.title =element_blank(), 
                          legend.text = element_text(size = 10)))
    dev.off()
    
    jpeg(paste0('BoxPLot_AL_14comp_rgn_yr',yr,'.jpeg'),width = 16, height = 10, units = 'in', res = 400)
    
    print( ggplot(NULL)+
        geom_boxplot(data = df_toplot_subset_yr_melt, aes(y = Country, x = value),fill = "white", colour = "darkgrey",
                     size = 0.5)+
        geom_point(data = df_dryad_AL, aes(y = Country, x = AL, col = 'black'), shape = 18, size = 2.5)+
        scale_y_discrete(limits=rev)+
        facet_wrap(~Region,scales = "free") +
        scale_color_manual(values = "black", label = "AL")+
        guides(color = guide_legend(title = "N deposition product"))+
        xlab(bquote('N deposition (kg N'~ ha^-1~yr^-1~')'))+
        theme_bw()+ theme(legend.position = c(0.8,0.3), 
                          #        legend.title =element_blank(), 
                          legend.text = element_text(size = 10)))
    dev.off()
    
    jpeg(paste0('BoxPLot_WH_14comp_rgn_yr',yr,'.jpeg'),width = 16, height = 10, units = 'in', res = 400)
    
    print(ggplot(NULL)+
        geom_boxplot(data = df_toplot_subset_yr_melt, aes(y = Country, x = value),fill = "white", colour = "darkgrey",
                     size = 0.5)+
        geom_point(data = df_dryad_WH, aes(y = Country, x = WH, col = 'black'), shape = 18, size = 2.5)+
        scale_y_discrete(limits=rev)+
        facet_wrap(~Region,scales = "free") +
        scale_color_manual(values = "black", label = "WH")+
        guides(color = guide_legend(title = "N deposition product"))+
        xlab(bquote('N deposition (kg N'~ ha^-1~yr^-1~')'))+
        theme_bw()+ theme(legend.position = c(0.8,0.3), 
                          #        legend.title =element_blank(), 
                          legend.text = element_text(size = 10)))
    dev.off()
    
    jpeg(paste0('BoxPLot_WL_14comp_rgn_yr',yr,'.jpeg'),width = 16, height = 10, units = 'in', res = 400)
    
    print(ggplot(NULL)+
        geom_boxplot(data = df_toplot_subset_yr_melt, aes(y = Country, x = value),fill = "white", colour = "darkgrey",
                     size = 0.5)+
        geom_point(data = df_dryad_WL, aes(y = Country, x = WL, col = 'black'), shape = 18, size = 2.5)+
        scale_y_discrete(limits=rev)+
        facet_wrap(~Region,scales = "free") +
        scale_color_manual(values = "black", label = "WL")+
        guides(color = guide_legend(title = "N deposition product"))+
        xlab(bquote('N deposition (kg N'~ ha^-1~yr^-1~')'))+
        theme_bw()+ theme(legend.position = c(0.8,0.3), 
                          #        legend.title =element_blank(), 
                          legend.text = element_text(size = 10)))
    dev.off()
}

