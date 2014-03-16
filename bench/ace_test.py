from pyace import ace
#from ace.ace import ace
import sys
sys.path.append('/home/glen/workspace/DataRobot')
from ModelingMachine.engine.eda_multi import _get_report_level_one
from ModelingMachine.engine.metrics import direction_by_name, metric_by_name
import pandas
import numpy as np
import datasets

def get_accuracy_metric(col):
    eda_report = {}
    rp =  _get_report_level_one(eda_report, col, col.dtype)
    return rp['metric_options']['accuracy']['short_name']

#for ds in datasets.get_datasets(name=['fastiron-train-30k','kickcars_train_full','census_1990_small','french_damage_cost','allstate_nonzero_small','amazon_small_no-c','credit_full','bank_marketing_small','bio_grid_small','mets','trainingDataWithoutNegativeWeights','census_2012h_small']):
#for ds in datasets.get_datasets(name='trainingDataWithoutNegativeWeights'):
for ds in datasets.get_datasets(name='fastiron-train-30k'):
#for ds in datasets.get_datasets(name='fastiron_small'):
#for ds in datasets.get_datasets(name='kickcars_train_full'):
#for ds in datasets.get_datasets(name='french_damage_cost'):
#for ds in datasets.get_datasets(name='census_1990_small'):
    X, y = datasets.get_data(ds,standardize=False,convert='numbers')
    cols = datasets.get_columns(ds)
    cats = datasets.get_columns(ds,'category')
    sc1={}
    sc2={}
    klist=(0,)
    #klist = (1,5,10,20,40,80)
    df=pandas.DataFrame(np.hstack((X,np.reshape(y,(-1,1)))),columns=cols+[ds['target']])
    rm = get_accuracy_metric(df[ds['target']])
    mdir = direction_by_name(rm)
    mfunc = metric_by_name(rm)
    rnk1={}
    rnk2={}
    for K in klist:
        sys.stderr.write( ds['name']+' '+str(K)+'\n')
        if ds['rtype']=='Binary':
            cats.append(ds['target'])
        sc1[K] = ace(df, ds['target'], cat_cols=cats, cv=True, K=K)[:-1]
        rnk1[K] = np.empty(len(sc1[K]))
        temp1 = np.argsort(-np.array(sc1[K]))
        rnk1[K][temp1] = np.arange(len(sc1[K]))
        sc2[K] = ace(df, ds['target'], cat_cols=cats, cv=True, K=K, metric=mfunc, metric_dir=mdir)[:-1]
        rnk2[K] = np.empty(len(sc2[K]))
        temp2 = np.argsort(-np.array(sc2[K]))
        rnk2[K][temp2] = np.arange(len(sc2[K]))
        #sc3 = ace(pandas.DataFrame(np.hstack((X,np.reshape(y,(-1,1)))),columns=cols+[ds['target']]),ds['target'],cat_cols=cats,cv=True,logloss=True)
    f=open('ace_'+ds['name']+'.csv','w')
    f.write("Dataset,Column,Type")
    #for K in klist:
    for K in klist:
        f.write(",K%d %s,K%d %s,K%d %s,K%d %s" % (K,'RSQ',K,rm,K,'rank',K,'rank'))
    f.write("\n")
    #f.write(str( zip(cols+['y'],sc2))+'\n')
    for i,c in enumerate(cols):
        if c!='__y__':
            f.write( '%s,%s,%s' % (ds['name'],c,'C' if c in cats else 'N'))
            for K in klist:
                #f.write(",%f" % sc1[K][i])
                f.write(",%f,%f,%d,%d" % (sc1[K][i],sc2[K][i],rnk1[K][i]+1,rnk2[K][i]+1))
            f.write("\n")
            #print '%s,%s,%s,%f,%f,%f' % (ds['name'],c,'C' if c in cats else 'N',sc1[i],sc2[i],sc3[i])
            f.flush()
    f.close()
