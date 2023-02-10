
clear;clc;
%% ECN station data

opts = spreadsheetImportOptions("NumVariables", 6);

% Specify sheet and range
opts.Sheet = "Summary_Bulk_1980-2018";
opts.DataRange = "A3:F906";

% Specify column names and types
opts.VariableNames = ["Province", "site", "No", "Eo", "VarName5", "BulkNDeposition"];
opts.VariableTypes = ["categorical", "categorical", "double", "double", "double", "double"];

% Specify variable properties
opts = setvaropts(opts, ["Province", "site"], "EmptyFieldRule", "auto");

% Import the data
CroplandNDepinChina19802018 = readtable(".\Station DATA\Fusuo_Zhangs_group_at_CAU\Cropland N Dep_in China 1980-2018.xlsx", opts, "UseExcel", false);

stn_mat = nan(length(unique(CroplandNDepinChina19802018.site)),length(1961:2018));
site_unique = unique(CroplandNDepinChina19802018.site);
yr_unique = 1961:2018;
for yr=1:length(1961:2018)
    for site = 1:length(unique(CroplandNDepinChina19802018.site))
        idx_s = find(CroplandNDepinChina19802018.site==site_unique(site));
        idx_y = find(CroplandNDepinChina19802018.VarName5==yr_unique(yr));
        idx_common = intersect(idx_s,idx_y);
        if isempty(idx_common)
            continue
        else
            stn_mat(site,yr) = nanmean(CroplandNDepinChina19802018.BulkNDeposition(idx_common));
    
        end
    end
end
clear opts
%% ACCMIP
%% HYDE
opts = delimitedTextImportOptions("NumVariables", 59);

% Specify range and delimiter
opts.DataLines = [1, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["VarName1", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13", "VarName14", "VarName15", "VarName16", "VarName17", "VarName18", "VarName19", "VarName20", "VarName21", "VarName22", "VarName23", "VarName24", "VarName25", "VarName26", "VarName27", "VarName28", "VarName29", "VarName30", "VarName31", "VarName32", "VarName33", "VarName34", "VarName35", "VarName36", "VarName37", "VarName38", "VarName39", "VarName40", "VarName41", "VarName42", "VarName43", "VarName44", "VarName45", "VarName46", "VarName47", "VarName48", "VarName49", "VarName50", "VarName51", "VarName52", "VarName53", "VarName54", "VarName55", "VarName56", "VarName57", "VarName58", "VarName59"];
opts.VariableTypes = ["char", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, "VarName1", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "VarName1", "EmptyFieldRule", "auto");

% Import the data
[number, string, dftotNdepkgNha]= xlsread('.\Data files for repository\Adjusting missing values using FAO\Submission filles\1_AH.xlsx');
dftotNdepkgNha(1,:)=[];

df_totNdep_AH = cell2mat(dftotNdepkgNha(45,3:end));
clear opts
%% LUH
opts = delimitedTextImportOptions("NumVariables", 59);

% Specify range and delimiter
opts.DataLines = [1, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["VarName1", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13", "VarName14", "VarName15", "VarName16", "VarName17", "VarName18", "VarName19", "VarName20", "VarName21", "VarName22", "VarName23", "VarName24", "VarName25", "VarName26", "VarName27", "VarName28", "VarName29", "VarName30", "VarName31", "VarName32", "VarName33", "VarName34", "VarName35", "VarName36", "VarName37", "VarName38", "VarName39", "VarName40", "VarName41", "VarName42", "VarName43", "VarName44", "VarName45", "VarName46", "VarName47", "VarName48", "VarName49", "VarName50", "VarName51", "VarName52", "VarName53", "VarName54", "VarName55", "VarName56", "VarName57", "VarName58", "VarName59"];
opts.VariableTypes = ["char", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, "VarName1", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "VarName1", "EmptyFieldRule", "auto");

% Import the data
[number, string, dftotNdepkgNha]= xlsread('.\Data files for repository\Adjusting missing values using FAO\Submission filles\2_AL.xlsx');
dftotNdepkgNha(1,:)=[];

df_totNdep_AL = cell2mat(dftotNdepkgNha(45,3:end));
clear opts
%% Zhou
%% HYDE
opts = delimitedTextImportOptions("NumVariables", 59);

% Specify range and delimiter
opts.DataLines = [1, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["VarName1", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13", "VarName14", "VarName15", "VarName16", "VarName17", "VarName18", "VarName19", "VarName20", "VarName21", "VarName22", "VarName23", "VarName24", "VarName25", "VarName26", "VarName27", "VarName28", "VarName29", "VarName30", "VarName31", "VarName32", "VarName33", "VarName34", "VarName35", "VarName36", "VarName37", "VarName38", "VarName39", "VarName40", "VarName41", "VarName42", "VarName43", "VarName44", "VarName45", "VarName46", "VarName47", "VarName48", "VarName49", "VarName50", "VarName51", "VarName52", "VarName53", "VarName54", "VarName55", "VarName56", "VarName57", "VarName58", "VarName59"];
opts.VariableTypes = ["char", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, "VarName1", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "VarName1", "EmptyFieldRule", "auto");

% Import the data
[number, string, dftotNdepkgNha]= xlsread('.\Data files for repository\Adjusting missing values using FAO\Submission filles\3_WH.xlsx');
dftotNdepkgNha(1,:)=[];

df_totNdep_WH = cell2mat(dftotNdepkgNha(45,3:end));
clear opts
%% LUH

opts = delimitedTextImportOptions("NumVariables", 59);

% Specify range and delimiter
opts.DataLines = [1, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["VarName1", "VarName2", "VarName3", "VarName4", "VarName5", "VarName6", "VarName7", "VarName8", "VarName9", "VarName10", "VarName11", "VarName12", "VarName13", "VarName14", "VarName15", "VarName16", "VarName17", "VarName18", "VarName19", "VarName20", "VarName21", "VarName22", "VarName23", "VarName24", "VarName25", "VarName26", "VarName27", "VarName28", "VarName29", "VarName30", "VarName31", "VarName32", "VarName33", "VarName34", "VarName35", "VarName36", "VarName37", "VarName38", "VarName39", "VarName40", "VarName41", "VarName42", "VarName43", "VarName44", "VarName45", "VarName46", "VarName47", "VarName48", "VarName49", "VarName50", "VarName51", "VarName52", "VarName53", "VarName54", "VarName55", "VarName56", "VarName57", "VarName58", "VarName59"];
opts.VariableTypes = ["char", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, "VarName1", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "VarName1", "EmptyFieldRule", "auto");

% Import the data
[number, string, dftotNdepkgNha]= xlsread('.\Data files for repository\Adjusting missing values using FAO\Submission filles\4_WL.xlsx');
dftotNdepkgNha(1,:)=[];

df_totNdep_WL = cell2mat(dftotNdepkgNha(45,3:end));clear opts 


%% PLotting
% china :42
close all;clc;
stn_mat(:,59:60) = NaN;
hb = boxplot(stn_mat);
boxes = findobj(gca, 'Tag', 'Box');
[~, ind] = sort(cellfun(@mean, get(boxes, 'XData')));

hold on
h1 = plot(df_totNdep_AH,'-ok','markersize',6,'markerfacecolor','m');
hold on
h2 = plot(df_totNdep_AL,'-ok','markersize',6,'markerfacecolor','g');
hold on
h3 = plot(df_totNdep_WH,'-ok','markersize',6,'markerfacecolor',[0.5 0.5 0.5]);
hold on
h4 = plot(df_totNdep_WL,'-ok','markersize',6,'markerfacecolor','c');
legend([boxes(ind(1)) h2 h1 h4 h3],{'Station record','AH','AL','WH','WL'},...
    'location','best');
xlabel('Year')
ylabel('N deposition (kg N ha^{-1} yr^{-1})')
set(gca,'XtickLabel',1961:2020)
xtickangle(90);

set(gca,'fontsize',13)
set(gcf, 'PaperPosition', [0 0 11 6]); %
saveas(gcf,'TotalNdep_Comp_StationsUK_China_Newdata_Dec2022.png')

