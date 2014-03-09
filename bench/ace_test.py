from pyace import ace
#from ace.ace import ace
import sys
import pandas
import numpy as np
import datasets

#for ds in datasets.get_datasets(name=['fastiron_small','kickcars_train_full']):
#for ds in datasets.get_datasets(name=['fastiron-train-30k','kickcars_train_full']):
#for ds in datasets.get_datasets(name='credit_small'):
#for ds in datasets.get_datasets(name='fastiron-train-30k'):
#for ds in datasets.get_datasets(name='fastiron_small'):
#for ds in datasets.get_datasets(name='kickcars_train_full'):
#for ds in datasets.get_datasets(name='french_damage_cost'):
for ds in datasets.get_datasets(name='census_1990_small'):
    X, y = datasets.get_data(ds,standardize=False,convert='numbers')
    cols = datasets.get_columns(ds)
    cats = datasets.get_columns(ds,'category')
    sc2={}
    klist=(1,)
    #klist = (1,5,10,20,40,80)
    df=pandas.DataFrame(np.hstack((X,np.reshape(y,(-1,1)))),columns=cols+[ds['target']])
    for K in klist:
        sys.stderr.write( ds['name']+' '+str(K)+'\n')
        if ds['rtype']=='Binary':
            cats.append(ds['target'])
        #sc1 = ace(pandas.DataFrame(np.hstack((X,np.reshape(y,(-1,1)))),columns=cols+[ds['target']]),ds['target'],cat_cols=cats,cv=False)
        sc2[K] = ace(df,ds['target'],cat_cols=cats,cv=True,K=K,logloss=False)
        #sc3 = ace(pandas.DataFrame(np.hstack((X,np.reshape(y,(-1,1)))),columns=cols+[ds['target']]),ds['target'],cat_cols=cats,cv=True,logloss=True)
    f=open('ace_'+ds['name']+'.csv','w')
    f.write("Dataset,Column,Type")
    #for K in klist:
    for K in klist:
        f.write(",K%d" % K)
    f.write("\n")
    #f.write(str( zip(cols+['y'],sc2))+'\n')
    for i,c in enumerate(cols):
        if c!='__y__':
            f.write( '%s,%s,%s' % (ds['name'],c,'C' if c in cats else 'N'))
            for K in klist:
                f.write(",%f" % sc2[K][i])
            f.write("\n")
            #print '%s,%s,%s,%f,%f,%f' % (ds['name'],c,'C' if c in cats else 'N',sc1[i],sc2[i],sc3[i])
            f.flush()
    f.close()
