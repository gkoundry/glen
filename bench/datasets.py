import pandas
import numpy as np
import sys
sys.path.append('/home/glen/workspace/DataRobot')
from ModelingMachine.engine.tasks.converters import DesignMatrix2, ConvertLevels
from sklearn.preprocessing import StandardScaler
from scipy.stats import nanmedian

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
        'name': 'allstate_nonzero_small',
        'file': '/home/glen/datasets/testdata/allstate-nonzero-small.csv',
        'target': 'Claim_Amount',
        'rtype': 'Regression',
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
]

def na_median(X):
    ''' returns a copy of X with NAs
    replaced by the median of the non NAs
    for each column
    '''
    col_median = nanmedian(X,axis=0)
    a=np.copy(X)
    inds = np.where(np.isnan(a))
    a[inds]=np.take(col_median,inds[1])
    return a

def get_datasets(rtype='All', size='small', name=None):
    if name:
        if isinstance(name,str):
            return [i for i in datasets if i['name'] == name][0]
        else:
            return [i for i in datasets if i['name'] in name]
    else:
        ds = []
        for i in datasets:
            if rtype in (i['rtype'],'All') and size in (i['size'],'All'):
                ds.append(i)
        return ds

def get_data(ds, standardize=True, convert='one_hot', drop=[]):
    if standardize and not convert:
        raise ValueError("option standardize requires convert 'one_hot' or 'numbers'")
    df = pandas.read_csv(ds['file'])

    target = df.pop(ds['target'])
    if target.dtype=='object':
        y = target.unique()
        target = target.replace(dict(zip(y,(0,1)))).astype(int)
    keep_num = [c for i,c in enumerate(ds['numeric']) if i+len(ds['category']) not in drop]
    keep_cat = [c for i,c in enumerate(ds['category']) if i not in drop]
    #print "dropping "+str([c for i,c in enumerate(ds['category']+ds['numeric']) if i in drop])
    num = df[keep_num].astype(float)
    cat = df[keep_cat].astype(object)
    if ds['numeric']:
        num2 = na_median(num.values)
    else:
        num2 = np.array([])
    if ds['category']:
        if convert == 'one_hot':
            dm2 = DesignMatrix2()
            cat2 = dm2.fit_transform(cat)().toarray()
        elif convert == 'numbers':
            clvl = ConvertLevels()
            cat2 = clvl.fit_transform(cat)()
        else:
            cat2 = cat.values
    else:
        cat2 = np.array([])

    if standardize:
        ss = StandardScaler()
        if len(cat2):
            if len(num2):
                return (ss.fit_transform(np.column_stack((cat2,num2))), target)
            else:
                return (ss.fit_transform(cat2), target)
        else:
            return (ss.fit_transform(num2), target)
    else:
        if len(cat2):
            if len(num2):
                return (np.column_stack((cat2,num2)), target)
            else:
                return (cat2, target)
        else:
                return (num2, target)

def get_column_index(ds):
    return range(0,len(ds['category']))

def get_columns(ds):
    return ds['category']+ds['numeric']
