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
        'numeric': ['RefId', 'VehYear', 'VehicleAge', 'VehOdo',
                    'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice',
                    'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitonRetailCleanPrice',
                    'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice',
                    'MMRCurrentRetailAveragePrice',
                    'MMRCurrentRetailCleanPrice', 'BYRNO', 'WarrantyCost'],
        'category': ['PurchDate', 'Auction', 'Make', 'Model', 'Trim', 'SubModel', 'Color',
                     'Transmission', 'WheelType', 'WheelTypeID', 'Nationality', 'Size', 'TopThreeAmericanName',
                     'PRIMEUNIT', 'AUCGUART', 'VNZIP1', 'VNST', 'VehBCost', 'IsOnlineSale'],
    }
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
    keep_num = [c for i,c in enumerate(ds['numeric']) if i+len(ds['category']) not in drop]
    keep_cat = [c for i,c in enumerate(ds['category']) if i not in drop]
    #print "dropping "+str([c for i,c in enumerate(ds['category']+ds['numeric']) if i in drop])
    num = df[keep_num].astype(float)
    cat = df[keep_cat].astype(object)
    num2 = na_median(num.values)
    if convert == 'one_hot':
        dm2 = DesignMatrix2()
        cat2 = dm2.fit_transform(cat)().toarray()
    elif convert == 'numbers':
        clvl = ConvertLevels()
        cat2 = clvl.fit_transform(cat)()
    else:
        cat2 = cat.values

    if standardize:
        ss = StandardScaler()
        return (ss.fit_transform(np.column_stack((cat2,num2))), target)
    else:
        return (np.column_stack((cat2,num2)), target)

def get_column_index(ds):
    return range(0,len(ds['category']))

def get_columns(ds):
    return ds['category']+ds['numeric']
