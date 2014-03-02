import pandas
import numpy as np
import scipy as sp
import sys
sys.path.append('/home/glen/workspace/DataRobot')
from ModelingMachine.engine.tasks.converters import DesignMatrix2, ConvertLevels, TfIdf2
from sklearn.preprocessing import StandardScaler
from scipy.stats import nanmedian
from common.encoding import detect_encoding

datasets = [
    {
        'name': 'kickcars_small',
        'file': '/home/glen/datasets/testdata/kickcars-training-sample.csv',
        'target': 'IsBadBuy',
        'rtype': 'Binary',
        'size': 'small',
        'numeric': ['VehYear', 'VehicleAge', 'VehOdo',
                    'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice',
                    'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitonRetailCleanPrice',
                    'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice',
                    'MMRCurrentRetailAveragePrice',
                    'MMRCurrentRetailCleanPrice', 'WarrantyCost'],
        'category': ['RefId', 'PurchDate', 'Auction', 'Make', 'Model', 'Trim', 'SubModel', 'Color',
                     'Transmission', 'WheelType', 'WheelTypeID', 'Nationality', 'Size', 'TopThreeAmericanName',
                     'PRIMEUNIT', 'AUCGUART', 'BYRNO', 'VNZIP1', 'VNST', 'VehBCost', 'IsOnlineSale'],
    },
    {
        'name': 'census_1990_small',
        'file': '/home/glen/datasets/testdata/census_1990_small.csv',
        'target': 'iClass',
        'rtype': 'Regression',
        'positive': True,
        'size': 'small',
        'numeric': ['caseid','dAge','dAncstry1','dAncstry2','iAvail','iCitizen','dDepart','iDisabl1','iDisabl2','iEnglish','iFeb55','iFertil','dHispanic','dHour89','dHours','iImmigr','dIncome1','dIncome2','dIncome3','dIncome4','dIncome5','dIncome6','dIncome7','dIncome8','dIndustry','iKorean','iLang1','iLooking','iMarital','iMay75880','iMeans','iMilitary','iMobility','iMobillim','dOccup','iOthrserv','iPerscare','dPOB','dPoverty','dPwgt1','iRagechld','dRearning','iRelat1','iRelat2','iRemplpar','iRiders','iRlabor','iRownchld','dRpincome','iRPOB','iRrelchld','iRspouse','iRvetserv','iSchool','iSept80','iSex','iSubfam1','iSubfam2','iTmpabsnt','dTravtime','iVietnam','dWeek89','iWork89','iWorklwk','iWWII','iYearsch','iYearwrk','dYrsserv'],
        'category': [],
    },
    {
        'name': 'allstate_nonzero_small',
        'file': '/home/glen/datasets/testdata/allstate-nonzero-small.csv',
        'target': 'Claim_Amount',
        'rtype': 'Regression',
        'positive': True,
        'size': 'small',
        'numeric': ['Vehicle', 'Calendar_Year', 'Model_Year','Var1','Var2','Var3','Var4','Var5','Var6','Var7','Var8'],
        'category': ['Row_ID', 'Household_ID', 'OrdCat', 'Blind_Make','Blind_Model','Blind_Submodel','Cat1','Cat2','Cat3','Cat4','Cat5',
                     'Cat6','Cat7','Cat8','Cat9','Cat10','Cat11','Cat12','NVCat','NVVar1','NVVar2','NVVar3','NVVar4'],
    },
    {
        'name': 'fastiron_small',
        'file': '/home/glen/datasets/testdata/fastiron-train-sample.csv',
        'target': 'SalePrice',
        'rtype': 'Regression',
        'positive': True,
        'size': 'small',
        'numeric': ['YearMade', 'MachineHoursCurrentMeter'],
        'category': ['SalesID', 'MachineID', 'ModelID', 'datasource', 'auctioneerID', 'UsageBand', 'saledate', 'fiModelDesc',
                     'fiBaseModel', 'fiSecondaryDesc', 'fiModelSeries', 'fiModelDescriptor', 'ProductSize', 'fiProductClassDesc',
                     'state', 'ProductGroup', 'ProductGroupDesc', 'Drive_System', 'Enclosure', 'Forks', 'Pad_Type', 'Ride_Control',
                     'Stick', 'Transmission', 'Turbocharged', 'Blade_Extension', 'Blade_Width', 'Enclosure_Type',
                     'Engine_Horsepower', 'Hydraulics', 'Pushblock', 'Ripper', 'Scarifier', 'Tip_Control', 'Tire_Size', 'Coupler',
                     'Coupler_System', 'Grouser_Tracks', 'Hydraulics_Flow', 'Track_Type', 'Undercarriage_Pad_Width', 'Stick_Length',
                     'Thumb', 'Pattern_Changer', 'Grouser_Type', 'Backhoe_Mounting', 'Blade_Type', 'Travel_Controls',
                     'Differential_Type', 'Steering_Controls'],
    },
    {
        'name': 'amazon_small_no-c',
        'file': '/home/glen/datasets/testdata/amazon_small_no-c.csv',
        'target': 'ACTION',
        'rtype': 'Binary',
        'size': 'small',
        'numeric': [],
        'category': ['RESOURCE', 'MGR_ID', 'ROLE_ROLLUP_1', 'ROLE_ROLLUP_2', 'ROLE_DEPTNAME', 'ROLE_TITLE',
                     'ROLE_FAMILY_DESC', 'ROLE_FAMILY', 'ROLE_CODE' ],
    },
    {
        'name': 'credit_small',
        'file': '/home/glen/datasets/testdata/credit-train-small.csv',
        'target': 'SeriousDlqin2yrs',
        'rtype': 'Binary',
        'size': 'small',
        'numeric': ['RevolvingUtilizationOfUnsecuredLines', 'age', 'NumberOfTime30-59DaysPastDueNotWorse',
                    'DebtRatio', 'MonthlyIncome', 'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate',
                    'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfDependents'],
        'category': [],
    },
    {
        'name': 'bank_marketing_small',
        'file': '/home/glen/datasets/testdata/bank_marketing_small.csv',
        'target': 'y',
        'rtype': 'Binary',
        'size': 'small',
        'numeric': ['age', 'balance', 'day', 'duration', 'pdays', 'previous'],
        'category': ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'campaign', 'poutcome'],

    },
    {
        'name': 'bio_grid_small',
        'file': '/home/glen/datasets/testdata/bio_grid_small.csv',
        'target': 'Throughput',
        'rtype': 'Binary',
        'size': 'small',
        'numeric': [],
        'category': ['#BioGRID Interaction ID', 'Entrez Gene Interactor A', 'Entrez Gene Interactor B', 'BioGRID ID Interactor A', 'BioGRID ID Interactor B', 'Systematic Name Interactor A', 'Systematic Name Interactor B', 'Official Symbol Interactor A', 'Official Symbol Interactor B', 'Synonyms Interactor A', 'Synonyms Interactor B', 'Experimental System', 'Experimental System Type', 'Author', 'Pubmed ID', 'Organism Interactor A', 'Organism Interactor B', 'Score', 'Modification', 'Phenotypes', 'Qualifications', 'Tags', 'Source Database'],

    },
    {
        'name': 'bio_response',
        'file': '/home/glen/datasets/testdata/bio_response_combined.csv',
        'target': 'Activity',
        'rtype': 'Binary',
        'size': 'small',
        'numeric': ['D'+str(i+1) for i in range(1776)],
        'category': [],
    },
    {
        'name': 'amazon_de_reviews_small',
        'file': '/home/glen/datasets/testdata/amazon_de_reviews_small.csv',
        'target': 'rating',
        'rtype': 'Regression',
        'size': 'small',
        'numeric': [],
        'category': ['category'],
        'text': ['text','summary']
    },
    {
        'name': 'mets',
        'file': '/home/glen/datasets/testdata/New_York_Mets.csv',
        'target': 'Grade',
        'rtype': 'Regression',
        'size': 'small',
        'numeric': ['1B_act','1B_adj','2b_act','2b_adj','3b_act','3b_adj','AVG_act','AVG_adj','AVG_adj_Z','Age','Age_Z','AvgFact','BBPA_act','BBPA_adj','BBPA_adj_Z','Draft Year','ERAFactor','HRPA_act','HRPA_adj','HRPA_adj_Z','Hrfactor','ISO_act','ISO_adj','ISO_adj_Z','KW_act','KW_adj','KW_adj_Z','Kfactor','OBP_act','OBP_adj','OBP_adj_Z','OPS_act','OPS_adj','PF','Pos_1B','Pos_2B','Pos_3B','Pos_C','Pos_CF','Pos_IF','Pos_LF','Pos_OF','Pos_RF','Pos_SS','Rfactor','SLG_act','SLG_adj','SLG_adj_Z','SOPA_act','SOPA_adj','SOPA_adj_Z','Sbfactor','SoS','TPA(ADJ)_act','TPA(ADJ)_adj','TPA_adj_Z','XBH/AB_act','XBH/AB_adj','XBH/AB_adj_Z','XBH_act','XBH_adj','ab_act','ab_adj','bb_act','bb_adj','h_act','h_adj','hr_act','hr_adj','so_act','so_adj','tb_act','tb_adj','JS','YR'],
        'category': ['PlayerID','School','dummy','Type'],
        'text': []
    },
    {
        'name': 'traind1s',
        'file': '/home/glen/datasets/testdata/traind1s.dat',
        'target': 'y',
        'rtype': 'Binary',
        'size': 'large',
        'numeric': ['r','c','h','count','pct','h_fb','count_fb','pct_fb','r0c0','r0c1','r0c2','r0c3','r0c4','r0c5','r0c6','r1c0','r1c1','r1c2','r1c3','r1c4','r1c5','r1c6','r2c0','r2c1','r2c2','r2c3','r2c4','r2c5','r2c6','r3c0','r3c1','r3c2','r3c3','r3c4','r3c5','r3c6','r4c0','r4c1','r4c2','r4c3','r4c4','r4c5','r4c6','r5c0','r5c1','r5c2','r5c3','r5c4','r5c5','r5c6','r6c0','r6c1','r6c2','r6c3','r6c4','r6c5','r6c6'],
        'category': [],
        'text': []
    },
    {
        'name': 'traind4s',
        'file': '/home/glen/datasets/testdata/traind4s.dat',
        'target': 'y',
        'rtype': 'Binary',
        'size': 'large',
        'numeric': ['r','c','h','count','pct','h_fb','count_fb','pct_fb','r0c0','r0c1','r0c2','r0c3','r0c4','r0c5','r0c6','r1c0','r1c1','r1c2','r1c3','r1c4','r1c5','r1c6','r2c0','r2c1','r2c2','r2c3','r2c4','r2c5','r2c6','r3c0','r3c1','r3c2','r3c3','r3c4','r3c5','r3c6','r4c0','r4c1','r4c2','r4c3','r4c4','r4c5','r4c6','r5c0','r5c1','r5c2','r5c3','r5c4','r5c5','r5c6','r6c0','r6c1','r6c2','r6c3','r6c4','r6c5','r6c6'],
        'category': [],
        'text': []
    },
    {
        'name': 'traind5s',
        'file': '/home/glen/datasets/testdata/traind5s.dat',
        'target': 'y',
        'rtype': 'Binary',
        'size': 'large',
        'numeric': ['r','c','h','count','pct','h_fb','count_fb','pct_fb','r0c0','r0c1','r0c2','r0c3','r0c4','r0c5','r0c6','r1c0','r1c1','r1c2','r1c3','r1c4','r1c5','r1c6','r2c0','r2c1','r2c2','r2c3','r2c4','r2c5','r2c6','r3c0','r3c1','r3c2','r3c3','r3c4','r3c5','r3c6','r4c0','r4c1','r4c2','r4c3','r4c4','r4c5','r4c6','r5c0','r5c1','r5c2','r5c3','r5c4','r5c5','r5c6','r6c0','r6c1','r6c2','r6c3','r6c4','r6c5','r6c6'],
        'category': [],
        'text': []
    },
    {
        'name': 'mets_short',
        'file': '/home/glen/datasets/testdata/New_York_Mets.csv',
        'target': 'Grade',
        'rtype': 'Regression',
        'size': 'small',
        'numeric': ['1B_adj','2b_adj','3b_adj'], #,'AVG_adj','Age','AvgFact'], #,'BBPA_adj','Draft Year','ERAFactor'], #,'HRPA_adj','Hrfactor','ISO_adj','KW_adj','Kfactor','OBP_adj','OPS_adj','PF','Pos_1B','Pos_2B','Pos_3B','Pos_C','Pos_CF','Pos_IF','Pos_LF','Pos_OF','Pos_RF','Pos_SS','Rfactor','SLG_adj','SOPA_adj','Sbfactor','SoS','TPA(ADJ)_adj','XBH/AB_adj','XBH_adj','ab_adj','bb_adj','h_adj','hr_adj','so_adj','tb_adj','JS','YR'],
        'category': ['Type','School'],
        'text': []
    },
    {
        'name': 'trainingDataWithoutNegativeWeights',
        'file': '/home/glen/datasets/testdata/trainingDataWithoutNegativeWeights.csv',
        'target': 'classification',
        'rtype': 'Binary',
        'size': 'large',
        'numeric': [ 'age', 'eap', 'ecp', 'reservePrice', 'weight', 'last-clicked-advertiser', 'last-clicked-any', 'last-clicked-campaign', 'last-clicked-creative', 'last-pixeled-advertiser', 'last-pixeled-any', 'last-pixeled-campaign', 'last-seen-advertiser', 'last-seen-any', 'last-seen-campaign', 'last-seen-creative', 'domain-campaign-prop-ratio-log', 'domain-visits', 'log-domain-visits', 'log-unique-domain-visits', 'unique-domain-visits', 'advertiserId', 'campaignId', 'digitCount', 'dma', 'domainLength', 'first-click-campaign', 'first-imp-campaign', 'first-pixel-campaign', 'hyphenCount', 'internalCreativeId', 'inventorySourceId', 'ipA', 'ipB', 'ipC', 'language', 'placement', 'publisher', 'seller', 'siteId', 'tagId', 'templateId', 'timeOfArrival-10MinuteOfDay', 'timeOfArrival-dayOfMonth', 'timeOfArrival-dayOfWeek', 'timeOfArrival-halfHourOfDay', 'timeOfArrival-hourOfDay', 'timeOfArrival-hourOfWeek',
                'timeOfArrival-minuteOfDay', 'timeOfArrival-minuteOfHour', 'timeOfArrival-monthOfYear', 'timeOfArrival-year', 'totalClicks', 'totalEngagements', 'totalImps', 'userId', 'zip'],
        'category': [ 'content-cat-12', 'content-cat-18', 'content-cat-19', 'content-cat-22', 'content-cat-6', 'content-cat-7984', 'content-cat-7994', 'content-cat-8008', 'content-cat-8040', 'content-cat-8142', 'content-cat-8168', 'content-cat-8170', 'content-cat-8320', 'content-cat-8350', 'content-cat-8374', 'content-cat-8388', 'content-cat-8436', 'content-cat-8564', 'content-cat-8604', 'content-cat-8608', 'hit-pixel-anc-click-14264-1845067', 'hit-pixel-anc-click-16220-1806262', 'hit-pixel-anc-click-16695-1806260', 'hit-pixel-anc-click-17514-1982405', 'hit-pixel-anc-click-17522-1845067', 'hit-pixel-anc-click-19407-2257999', 'hit-pixel-anc-click-19408-1806262', 'hit-pixel-anc-click-19410-1845067', 'hit-pixel-anc-click-19412-1982405', 'hit-pixel-anc-click-19418-1806262', 'hit-pixel-anc-click-19420-1845067', 'hit-pixel-anc-click-19431-1806260', 'hit-pixel-anc-click-19453-1845067', 'hit-pixel-anc-click-19455-1982405', 'hit-pixel-anc-click-19595-1845067', 'hit-pixel-anc-click-19597-1845067', 'hit-pixel-anc-click-20685-2403000', 'hit-pixel-anc-click-20696-2402749', 'hit-pixel-anc-click-20755-2402750', 'hit-pixel-anc-click-20762-2403000', 'hit-pixel-anc-click-21141-2445926', 'hit-pixel-anc-click-21170-2445701', 'hit-pixel-anc-click-21209-2445946', 'hit-pixel-anc-click-21210-2445701', 'hit-pixel-aw-click-keyword-13042', 'hit-pixel-consideration-contact', 'hit-pixel-consideration-downloads', 'hit-pixel-conversion-form-visit', 'hit-pixel-form-interaction-download-company',
                'hit-pixel-form-interaction-download-country', 'hit-pixel-form-interaction-download-email', 'hit-pixel-form-interaction-download-lname', 'p39-cat-10038', 'p39-cat-10042', 'p39-cat-10536', 'p39-cat-12943', 'p39-cat-13399', 'p39-cat-16620', 'p39-cat-17266', 'p39-cat-18106', 'p39-cat-18384', 'p39-cat-19283', 'p39-cat-20079', 'p39-cat-3974', 'p39-cat-3976', 'p39-cat-3992', 'p39-cat-3995', 'p39-cat-4001', 'p39-cat-4013', 'p39-cat-4022', 'p39-cat-4383', 'p39-cat-4860', 'p39-cat-5301', 'p39-cat-6006', 'p39-cat-6121', 'hit-pixel-form-interaction-download', 'p39-cat-20413', 'city', 'country', 'domain', 'gender', 'intendedAudience', 'position', 'region', 'tagFormat', 'timeZone', 'url', 'content-cat-31', 'p39-cat-20120', 'p39-cat-4015', 'p39-cat-18120', 'p39-cat-18124', 'p39-cat-20531', 'content-cat-8150', 'p39-cat-3980', 'content-cat-15', 'p39-cat-20439', 'content-cat-7988', 'content-cat-10',
                'p39-cat-14757', 'content-cat-8152', 'hit-pixel-form-interaction', 'p39-cat-19870', 'p39-cat-4032', 'p39-quality-comments', 'hit-pixel-anc-click-19410-2257999', 'p39-cat-10043', 'p39-cat-4012', 'p39-cat-6123', 'p39-cat-18139', 'p39-quality-ffugc', 'p39-quality-ffaat', 'content-cat-8382', 'p39-cat-20412', 'p39-cat-20119', 'content-cat-20593', 'p39-cat-14425', 'content-cat-21128', 'content-cat-21127', 'content-cat-13', 'content-cat-21330', 'content-cat-21332', 'content-cat-25', 'content-cat-26', 'content-cat-8000', 'content-cat-8006', 'content-cat-8010', 'content-cat-8300', 'content-cat-8308', 'content-cat-8314', 'content-cat-8362', 'content-cat-8378', 'hit-pixel-anc-click-15774-1845067', 'hit-pixel-anc-click-15789-2257999', 'hit-pixel-anc-click-16540-1806262', 'hit-pixel-anc-click-16697-1845067', 'hit-pixel-anc-click-19393-2257999', 'hit-pixel-anc-click-19395-2257999', 'hit-pixel-anc-click-19405-1806262', 'hit-pixel-anc-click-21182-2445926', 'hit-pixel-consideration-customers', 'inventory-attr-14', 'inventory-attr-16', 'inventory-attr-4', 'inventory-attr-6', 'inventory-attr-8', 'p39-cat-12358', 'p39-cat-12779', 'p39-cat-16616',
                'p39-cat-17248', 'p39-cat-17510', 'p39-cat-17789', 'p39-cat-18078', 'p39-cat-18474', 'p39-cat-18857', 'p39-cat-19265', 'p39-cat-19291', 'p39-cat-20063', 'p39-cat-20396', 'p39-cat-20437', 'p39-cat-3966', 'p39-cat-3977', 'p39-cat-4034', 'p39-cat-4044', 'p39-cat-4049', 'p39-cat-4207', 'p39-cat-4381', 'p39-cat-5000', 'p39-cat-5026', 'p39-cat-6118', 'p39-cat-8806', 'p39-cat-18244', 'hit-pixel-anc-click-19408-2257999', 'p39-cat-3994', 'content-cat-8154', 'p39-cat-18099', 'hit-pixel-consideration', 'p39-cat-10019', 'p39-cat-12599', 'hit-pixel-page-scroll', 'p39-cat-10627', 'content-cat-5', 'content-cat-7992', 'content-cat-8002', 'content-cat-8090', 'content-cat-8298', 'content-cat-8364', 'content-cat-8414', 'content-cat-8480', 'hit-pixel-anc-click-16294-1806262', 'hit-pixel-anc-click-17514-1806262', 'hit-pixel-anc-click-19392-1845067', 'hit-pixel-consideration-about', 'hit-pixel-consideration-company', 'hit-pixel-consideration-events', 'hit-pixel-consideration-facts', 'hit-pixel-consideration-learn', 'hit-pixel-consideration-support', 'hit-pixel-page-20s-view',
                'p39-cat-10338', 'p39-cat-12357', 'p39-cat-12359', 'p39-cat-18104', 'p39-cat-19301', 'p39-cat-20438', 'p39-cat-3960', 'p39-cat-3997', 'p39-cat-3978', 'hit-pixel-page-40s-view', 'content-cat-23', 'content-cat-8148', 'content-cat-8596', 'hit-pixel-consideration-solutions', 'p39-cat-10339', 'p39-cat-10340', 'p39-cat-18454', 'p39-cat-20645', 'p39-cat-9408', 'p39-cat-18096', 'p39-cat-18241', 'p39-cat-19891', 'p39-cat-10040', 'p39-cat-17263', 'p39-cat-19343', 'p39-cat-18856', 'p39-quality-cre', 'content-cat-21', 'content-cat-8310', 'content-cat-8312', 'content-cat-8434', 'hit-pixel-anc-click-14333-1845067', 'hit-pixel-anc-click-19590-1845067', 'hit-pixel-consideration-products', 'hit-pixel-form-interaction-download-fname', 'hit-pixel-form-interaction-download-phone', 'p39-cat-18242', 'p39-cat-18243', 'p39-cat-18476', 'p39-cat-3962', 'p39-cat-4042', 'p39-cat-4043', 'p39-cat-4046', 'p39-cat-7047', 'p39-cat-15833', 'p39-cat-10044', 'p39-cat-17260', 'p39-cat-18083', 'p39-cat-4014', 'p39-cat-4053',
                'p39-cat-4056', 'p39-adcount', 'p39-cat-10037', 'p39-cat-12776', 'p39-advis', 'p39-cat-4989', 'p39-cat-12777', 'p39-lan', 'p39-cat-4992', 'content-cat-17', 'content-cat-20591', 'content-cat-8012', 'content-cat-8612', 'hit-pixel-anc-click-14257-1845067', 'hit-pixel-anc-click-17528-1845067', 'hit-pixel-anc-click-19428-1845067', 'hit-pixel-consideration-product', 'p39-cat-10041', 'p39-cat-3964', 'p39-quality-hindex', 'p39-cat-18100', 'p39-cat-20112', 'p39-cat-4990', 'p39-cat-5023', 'p39-cat-12657', 'p39-cat-14766', 'p39-cat-5021', 'p39-cat-5302', 'content-cat-20', 'p39-cat-15556', 'p39-cat-17040', 'p39-cat-17042', 'p39-cat-18098', 'p39-cat-4991', 'p39-cat-8803', 'p39-quality-ffparked', 'content-cat-9', 'p39-cat-15837', 'content-cat-8014', 'hit-pixel-anc-click-17515-1845067', 'hit-pixel-anc-click-19398-1845067', 'p39-cat-12925', 'p39-quality-ffbac', 'content-cat-29', 'content-cat-8004', 'content-cat-8202', 'content-cat-8206', 'content-cat-8304', 'hit-pixel-anc-click-16294-2257999', 'p39-cat-12600',
                'p39-cat-3988', 'p39-cat-4031', 'p39-cat-4041', 'hit-pixel-page-view', 'content-cat-8302', 'hit-pixel-consideration-sweepstakes', 'hit-pixel-conversion', 'p39-cat-17512', 'p39-cat-18389', 'p39-cat-19286', 'p39-cat-6117', 'user-hit-pixel', 'hit-pixel-page-multiple-view', 'initial-interaction', 'domain-looks-spammy', 'estimatedPriceVerified', 'isSecure', 'moreThan15Characters', 'moreThan1Hyphen', 'moreThan3Digits', 'noCookies', 'noFlash'],
        'text': []
    },
    {
        'name': 'trainingDataWithoutNegativeWeights1k',
        'file': '/home/glen/datasets/testdata/trainingDataWithoutNegativeWeights1k.csv',
        'target': 'classification',
        'rtype': 'Binary',
        'size': 'small',
        'numeric': [ 'age', 'eap', 'ecp', 'reservePrice', 'weight', 'last-clicked-advertiser', 'last-clicked-any', 'last-clicked-campaign', 'last-clicked-creative', 'last-pixeled-advertiser', 'last-pixeled-any', 'last-pixeled-campaign', 'last-seen-advertiser', 'last-seen-any', 'last-seen-campaign', 'last-seen-creative', 'domain-campaign-prop-ratio-log', 'domain-visits', 'log-domain-visits', 'log-unique-domain-visits', 'unique-domain-visits', 'advertiserId', 'campaignId', 'digitCount', 'dma', 'domainLength', 'first-click-campaign', 'first-imp-campaign', 'first-pixel-campaign', 'hyphenCount', 'internalCreativeId', 'inventorySourceId', 'ipA', 'ipB', 'ipC', 'language', 'placement', 'publisher', 'seller', 'siteId', 'tagId', 'templateId', 'timeOfArrival-10MinuteOfDay', 'timeOfArrival-dayOfMonth', 'timeOfArrival-dayOfWeek', 'timeOfArrival-halfHourOfDay', 'timeOfArrival-hourOfDay', 'timeOfArrival-hourOfWeek',
                'timeOfArrival-minuteOfDay', 'timeOfArrival-minuteOfHour', 'timeOfArrival-monthOfYear', 'timeOfArrival-year', 'totalClicks', 'totalEngagements', 'totalImps', 'userId', 'zip'],
        'category': [ 'content-cat-12', 'content-cat-18', 'content-cat-19', 'content-cat-22', 'content-cat-6', 'content-cat-7984', 'content-cat-7994', 'content-cat-8008', 'content-cat-8040', 'content-cat-8142', 'content-cat-8168', 'content-cat-8170', 'content-cat-8320', 'content-cat-8350', 'content-cat-8374', 'content-cat-8388', 'content-cat-8436', 'content-cat-8564', 'content-cat-8604', 'content-cat-8608', 'hit-pixel-anc-click-14264-1845067', 'hit-pixel-anc-click-16220-1806262', 'hit-pixel-anc-click-16695-1806260', 'hit-pixel-anc-click-17514-1982405', 'hit-pixel-anc-click-17522-1845067', 'hit-pixel-anc-click-19407-2257999', 'hit-pixel-anc-click-19408-1806262', 'hit-pixel-anc-click-19410-1845067', 'hit-pixel-anc-click-19412-1982405', 'hit-pixel-anc-click-19418-1806262', 'hit-pixel-anc-click-19420-1845067', 'hit-pixel-anc-click-19431-1806260', 'hit-pixel-anc-click-19453-1845067', 'hit-pixel-anc-click-19455-1982405', 'hit-pixel-anc-click-19595-1845067', 'hit-pixel-anc-click-19597-1845067', 'hit-pixel-anc-click-20685-2403000', 'hit-pixel-anc-click-20696-2402749', 'hit-pixel-anc-click-20755-2402750', 'hit-pixel-anc-click-20762-2403000', 'hit-pixel-anc-click-21141-2445926', 'hit-pixel-anc-click-21170-2445701', 'hit-pixel-anc-click-21209-2445946', 'hit-pixel-anc-click-21210-2445701', 'hit-pixel-aw-click-keyword-13042', 'hit-pixel-consideration-contact', 'hit-pixel-consideration-downloads', 'hit-pixel-conversion-form-visit', 'hit-pixel-form-interaction-download-company',
                'hit-pixel-form-interaction-download-country', 'hit-pixel-form-interaction-download-email', 'hit-pixel-form-interaction-download-lname', 'p39-cat-10038', 'p39-cat-10042', 'p39-cat-10536', 'p39-cat-12943', 'p39-cat-13399', 'p39-cat-16620', 'p39-cat-17266', 'p39-cat-18106', 'p39-cat-18384', 'p39-cat-19283', 'p39-cat-20079', 'p39-cat-3974', 'p39-cat-3976', 'p39-cat-3992', 'p39-cat-3995', 'p39-cat-4001', 'p39-cat-4013', 'p39-cat-4022', 'p39-cat-4383', 'p39-cat-4860', 'p39-cat-5301', 'p39-cat-6006', 'p39-cat-6121', 'hit-pixel-form-interaction-download', 'p39-cat-20413', 'city', 'country', 'domain', 'gender', 'intendedAudience', 'position', 'region', 'tagFormat', 'timeZone', 'url', 'content-cat-31', 'p39-cat-20120', 'p39-cat-4015', 'p39-cat-18120', 'p39-cat-18124', 'p39-cat-20531', 'content-cat-8150', 'p39-cat-3980', 'content-cat-15', 'p39-cat-20439', 'content-cat-7988', 'content-cat-10',
                'p39-cat-14757', 'content-cat-8152', 'hit-pixel-form-interaction', 'p39-cat-19870', 'p39-cat-4032', 'p39-quality-comments', 'hit-pixel-anc-click-19410-2257999', 'p39-cat-10043', 'p39-cat-4012', 'p39-cat-6123', 'p39-cat-18139', 'p39-quality-ffugc', 'p39-quality-ffaat', 'content-cat-8382', 'p39-cat-20412', 'p39-cat-20119', 'content-cat-20593', 'p39-cat-14425', 'content-cat-21128', 'content-cat-21127', 'content-cat-13', 'content-cat-21330', 'content-cat-21332', 'content-cat-25', 'content-cat-26', 'content-cat-8000', 'content-cat-8006', 'content-cat-8010', 'content-cat-8300', 'content-cat-8308', 'content-cat-8314', 'content-cat-8362', 'content-cat-8378', 'hit-pixel-anc-click-15774-1845067', 'hit-pixel-anc-click-15789-2257999', 'hit-pixel-anc-click-16540-1806262', 'hit-pixel-anc-click-16697-1845067', 'hit-pixel-anc-click-19393-2257999', 'hit-pixel-anc-click-19395-2257999', 'hit-pixel-anc-click-19405-1806262', 'hit-pixel-anc-click-21182-2445926', 'hit-pixel-consideration-customers', 'inventory-attr-14', 'inventory-attr-16', 'inventory-attr-4', 'inventory-attr-6', 'inventory-attr-8', 'p39-cat-12358', 'p39-cat-12779', 'p39-cat-16616',
                'p39-cat-17248', 'p39-cat-17510', 'p39-cat-17789', 'p39-cat-18078', 'p39-cat-18474', 'p39-cat-18857', 'p39-cat-19265', 'p39-cat-19291', 'p39-cat-20063', 'p39-cat-20396', 'p39-cat-20437', 'p39-cat-3966', 'p39-cat-3977', 'p39-cat-4034', 'p39-cat-4044', 'p39-cat-4049', 'p39-cat-4207', 'p39-cat-4381', 'p39-cat-5000', 'p39-cat-5026', 'p39-cat-6118', 'p39-cat-8806', 'p39-cat-18244', 'hit-pixel-anc-click-19408-2257999', 'p39-cat-3994', 'content-cat-8154', 'p39-cat-18099', 'hit-pixel-consideration', 'p39-cat-10019', 'p39-cat-12599', 'hit-pixel-page-scroll', 'p39-cat-10627', 'content-cat-5', 'content-cat-7992', 'content-cat-8002', 'content-cat-8090', 'content-cat-8298', 'content-cat-8364', 'content-cat-8414', 'content-cat-8480', 'hit-pixel-anc-click-16294-1806262', 'hit-pixel-anc-click-17514-1806262', 'hit-pixel-anc-click-19392-1845067', 'hit-pixel-consideration-about', 'hit-pixel-consideration-company', 'hit-pixel-consideration-events', 'hit-pixel-consideration-facts', 'hit-pixel-consideration-learn', 'hit-pixel-consideration-support', 'hit-pixel-page-20s-view',
                'p39-cat-10338', 'p39-cat-12357', 'p39-cat-12359', 'p39-cat-18104', 'p39-cat-19301', 'p39-cat-20438', 'p39-cat-3960', 'p39-cat-3997', 'p39-cat-3978', 'hit-pixel-page-40s-view', 'content-cat-23', 'content-cat-8148', 'content-cat-8596', 'hit-pixel-consideration-solutions', 'p39-cat-10339', 'p39-cat-10340', 'p39-cat-18454', 'p39-cat-20645', 'p39-cat-9408', 'p39-cat-18096', 'p39-cat-18241', 'p39-cat-19891', 'p39-cat-10040', 'p39-cat-17263', 'p39-cat-19343', 'p39-cat-18856', 'p39-quality-cre', 'content-cat-21', 'content-cat-8310', 'content-cat-8312', 'content-cat-8434', 'hit-pixel-anc-click-14333-1845067', 'hit-pixel-anc-click-19590-1845067', 'hit-pixel-consideration-products', 'hit-pixel-form-interaction-download-fname', 'hit-pixel-form-interaction-download-phone', 'p39-cat-18242', 'p39-cat-18243', 'p39-cat-18476', 'p39-cat-3962', 'p39-cat-4042', 'p39-cat-4043', 'p39-cat-4046', 'p39-cat-7047', 'p39-cat-15833', 'p39-cat-10044', 'p39-cat-17260', 'p39-cat-18083', 'p39-cat-4014', 'p39-cat-4053',
                'p39-cat-4056', 'p39-adcount', 'p39-cat-10037', 'p39-cat-12776', 'p39-advis', 'p39-cat-4989', 'p39-cat-12777', 'p39-lan', 'p39-cat-4992', 'content-cat-17', 'content-cat-20591', 'content-cat-8012', 'content-cat-8612', 'hit-pixel-anc-click-14257-1845067', 'hit-pixel-anc-click-17528-1845067', 'hit-pixel-anc-click-19428-1845067', 'hit-pixel-consideration-product', 'p39-cat-10041', 'p39-cat-3964', 'p39-quality-hindex', 'p39-cat-18100', 'p39-cat-20112', 'p39-cat-4990', 'p39-cat-5023', 'p39-cat-12657', 'p39-cat-14766', 'p39-cat-5021', 'p39-cat-5302', 'content-cat-20', 'p39-cat-15556', 'p39-cat-17040', 'p39-cat-17042', 'p39-cat-18098', 'p39-cat-4991', 'p39-cat-8803', 'p39-quality-ffparked', 'content-cat-9', 'p39-cat-15837', 'content-cat-8014', 'hit-pixel-anc-click-17515-1845067', 'hit-pixel-anc-click-19398-1845067', 'p39-cat-12925', 'p39-quality-ffbac', 'content-cat-29', 'content-cat-8004', 'content-cat-8202', 'content-cat-8206', 'content-cat-8304', 'hit-pixel-anc-click-16294-2257999', 'p39-cat-12600',
                'p39-cat-3988', 'p39-cat-4031', 'p39-cat-4041', 'hit-pixel-page-view', 'content-cat-8302', 'hit-pixel-consideration-sweepstakes', 'hit-pixel-conversion', 'p39-cat-17512', 'p39-cat-18389', 'p39-cat-19286', 'p39-cat-6117', 'user-hit-pixel', 'hit-pixel-page-multiple-view', 'initial-interaction', 'domain-looks-spammy', 'estimatedPriceVerified', 'isSecure', 'moreThan15Characters', 'moreThan1Hyphen', 'moreThan3Digits', 'noCookies', 'noFlash'],
        'text': []
    },
    {
        'name': 'census_2012h_small',
        'file': '/home/glen/datasets/testdata/census_2012h_small.csv',
        'target': 'VEHICLES',
        'rtype': 'Regression',
        'size': 'small',
        'numeric': ['SERIALNO','DIVISION','PUMA','REGION','ST','ADJHSG','ADJINC','WGTP','NP','TYPE','ACR','AGS','BATH','BDSP','BLD','BUS','CONP','ELEP','FS','FULP','GASP','HFL','INSP','MHP','MRGI','MRGP','MRGT','MRGX','REFR','RMSP','RNTM','RNTP','RWAT','SINK','SMP','STOV','TEL','TEN','TOIL','VACS','VALP','WATP','YBL','FES','FFINCP','FGRNTP','FHINCP','FINCP','FPARC','FSMOCP','GRNTP','GRPIP','HHL','HHT','HINCP','HUGCL','HUPAC','HUPAOC','HUPARC','KIT','LNGI','MULTG','MV','NOC','NPF','NPP','NR','NRC','OCPIP','PARTNER','PLM','PSF','R18','R60','R65','RESMODE','SMOCP','SMX','SRNT','SVAL','TAXP','WIF','WKEXREL','WORKSTAT','FACRP','FAGSP','FBATHP','FBDSP','FBLDP','FBUSP','FCONP','FELEP','FFSP','FFULP','FGASP','FHFLP','FINSP','FKITP','FMHP','FMRGIP','FMRGP','FMRGTP','FMRGXP','FMVP','FPLMP','FREFRP','FRMSP','FRNTMP','FRNTP','FRWATP','FSINKP','FSMP','FSMXHP','FSMXSP','FSTOVP','FTAXP','FTELP','FTENP','FTOILP','FVACSP','FVALP','FVEHP','FWATP','FYBLP','wgtp1','wgtp2','wgtp3','wgtp4','wgtp5','wgtp6','wgtp7','wgtp8','wgtp9','wgtp10','wgtp11','wgtp12','wgtp13','wgtp14','wgtp15','wgtp16','wgtp17','wgtp18','wgtp19','wgtp20','wgtp21','wgtp22','wgtp23','wgtp24','wgtp25','wgtp26','wgtp27','wgtp28','wgtp29','wgtp30','wgtp31','wgtp32','wgtp33','wgtp34','wgtp35','wgtp36','wgtp37','wgtp38','wgtp39','wgtp40','wgtp41','wgtp42','wgtp43','wgtp44','wgtp45','wgtp46','wgtp47','wgtp48','wgtp49','wgtp50','wgtp51','wgtp52','wgtp53','wgtp54','wgtp55','wgtp56','wgtp57','wgtp58','wgtp59','wgtp60','wgtp61','wgtp62','wgtp63','wgtp64','wgtp65','wgtp66','wgtp67','wgtp68','wgtp69','wgtp70','wgtp71','wgtp72','wgtp73','wgtp74','wgtp75','wgtp76','wgtp77','wgtp78','wgtp79','wgtp80'],
        'category': ['RT',],
        'text': []
    },
#    {
#        'name': 'census_1990_small',
#        'file': '/home/glen/datasets/testdata/census_1990_small.csv',
#        'target': 'iClass',
#        'rtype': 'Regression',
#        'size': 'small',
#        'numeric': [],
#        'category': [],
#    },
]

def na_median(X):
    ''' returns a copy of X with NAs
    replaced by the median of the non NAs
    for each column
    '''
    col_median = np.nan_to_num(nanmedian(X,axis=0))
    a=np.copy(X)
    inds = np.where(np.isnan(a))
    a[inds]=np.take(col_median,inds[1])
    return a

def get_datasets(rtype='All', size='small', name=None):
    if name:
        if isinstance(name,str):
            return [i for i in datasets if i['name'] == name]
        else:
            return [i for i in datasets if i['name'] in name]
    else:
        ds = []
        for i in datasets:
            if rtype == 'Positive' and i.get('positive') and size in (i['size'],'All'):
                ds.append(i)
            elif rtype in (i['rtype'],'All') and size in (i['size'],'All'):
                ds.append(i)
        return ds

def get_data(ds, standardize=True, convert='one_hot', impute='median', drop=[]):
    if standardize and not convert:
        raise ValueError("option standardize requires convert 'one_hot' or 'numbers'")
    df = pandas.read_csv(ds['file'],encoding=detect_encoding(ds['file']))

    df = df[df[ds['target']].notnull()]
    target = df.pop(ds['target'])
    if target.dtype=='object':
        y = target.unique()
        target = target.replace(dict(zip(y,(0,1)))).astype(int)
    keep_cat = [c for i,c in enumerate(ds['category']) if i not in drop]
    keep_num = [c for i,c in enumerate(ds['numeric']) if i+len(ds['category']) not in drop]
    keep_txt = [c for i,c in enumerate(ds['text']) if i+len(ds['numeric'])+len(ds['category']) not in drop]
    #print "dropping "+str([c for i,c in enumerate(ds['category']+ds['numeric']) if i in drop])
    num = df[keep_num].astype(float)
    cat = df[keep_cat].astype(object)
    txt = df[keep_txt].astype(object)
    if ds['numeric']:
        if impute=='median':
            num2 = na_median(num.values)
        else:
            num2 = na_median(num.values)
    else:
        num2 = np.array([])
    if ds['category']:
        if convert == 'one_hot':
            dm2 = DesignMatrix2('dc=1')
            cat2 = dm2.fit_transform(cat)()
        elif convert == 'numbers':
            clvl = ConvertLevels()
            cat2 = clvl.fit_transform(cat)()
        else:
            cat2 = cat.values
    else:
        cat2 = np.array([])
    if ds['text']:
        tfidf = TfIdf2()
        txt2 = tfidf.fit_transform(txt)()
    else:
        txt2 = np.array([])

    if cat2.shape[0]:
        if len(num2):
            if txt2.shape[0]:
                X = np.column_stack((cat2,num2,txt2))
            else:
                #X = np.column_stack((cat2.todense(),num2))
                X = sp.sparse.hstack((cat2,sp.sparse.csc_matrix(num2+0.00001)),format='csc')
                assert np.all(np.logical_not(np.isnan(num2)))
                assert np.all(np.logical_not(np.isnan(cat2.todense())))
        else:
            if txt2.shape[0]:
                X = sp.sparse.hstack([cat2,txt2])
            else:
                X = cat2
    else:
        if len(num2):
            if txt2.shape[0]:
                X = np.column_stack((num2,txt2))
            else:
                X = num2
        else:
            if txt2.shape[0]:
                X = txt2
            else:
                raise RuntimeError("No data types selectes")

    if standardize:
        ss = StandardScaler()
        return (ss.fit_transform(X), target)
    else:
        return (X, target)

def get_column_index(ds):
    return range(0,len(ds['category']))

def get_columns(ds):
    return ds['category']+ds['numeric']
