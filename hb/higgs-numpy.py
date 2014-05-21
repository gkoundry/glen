#!/usr/bin/python
# this is the example script to use xgboost to train
import inspect
import os
import math
import sys
from sklearn.cross_validation import train_test_split,KFold,cross_val_score
import numpy as np
# add path of xgboost python module
code_path = '/home/glen/workspace/xgboost/python'

sys.path.append(code_path)

import xgboost as xgb

def AMS(s, b):
    """ Approximate Median Significance defined as:
        AMS = sqrt(
                2 { (s + b + b_r) log[1 + (s/(b+b_r))] - s}
              )
    where b_r = 10, b = background, s = signal, log is natural logarithm """

    br = 10.0
    radicand = 2 *( (s+b+br) * math.log (1.0 + s/(b+br)) -s)
    if radicand < 0:
        print 'radicand is negative. Exiting'
        exit()
    else:
        return math.sqrt(radicand)


test_size = 550000

# path to where the data lies
dpath = '.'

# load in training data, directly use numpy
dtrain = np.loadtxt( dpath+'/training.csv', delimiter=',', skiprows=1, converters={32: lambda x:int(x=='s'.encode('utf-8')) } )
print ('finish loading from csv ')

scb=0
scs=0
fo=open('predxgb.csv','w')
kf = KFold(dtrain.shape[0], 2, shuffle=True, random_state=1234)
for train,test in kf:
    label  = dtrain[train,32]
    data   = dtrain[train,1:31]
    # rescale weight to make it same as test set
    weight = dtrain[train,31] * float(test_size) / len(label)

    sum_wpos = sum( weight[i] for i in range(len(label)) if label[i] == 1.0  )
    sum_wneg = sum( weight[i] for i in range(len(label)) if label[i] == 0.0  )

    # print weight statistics
    print ('weight statistics: wpos=%g, wneg=%g, ratio=%g' % ( sum_wpos, sum_wneg, sum_wneg/sum_wpos ))

    # construct xgboost.DMatrix from numpy array, treat -999.0 as missing value
    xgmat = xgb.DMatrix( data, label=label, missing = -999.0, weight=weight )

    # setup parameters for xgboost
    param = {}
    # use logistic regression loss, use raw prediction before logistic transformation
    # since we only need the rank
    param['objective'] = 'binary:logitraw'
    # scale weight of positive examples
    param['scale_pos_weight'] = sum_wneg/sum_wpos
    param['bst:eta'] = 0.1
    param['bst:max_depth'] = 6
    param['eval_metric'] = 'auc'
    param['silent'] = 1
    param['nthread'] = 4

    # you can directly throw param in, though we want to watch multiple metrics here
    plst = list(param.items())+[('eval_metric', 'ams@0.15')]

    watchlist = [ (xgmat,'train') ]
    # boost 120 tres
    num_round = 120
    print ('loading data end, start to boost trees')
    bst = xgb.train( plst, xgmat, num_round, watchlist );

    label  = dtrain[test,32]
    data   = dtrain[test,1:31]
    ids = dtrain[test,0]
    # rescale weight to make it same as test set
    weight = dtrain[test,31] #* float(test_size) / len(label)
    xgmat = xgb.DMatrix( data, missing = -999.0 )
    pred = bst.predict(xgmat)
    for i,a in enumerate(label):
        fo.write('%d,%f\n' % (ids[i],pred[i]))
        if pred[i]>0.5:
            if a==1:
                scs += weight[i]
            else:
                scb += weight[i]

print '%f %f %f' % (scs,scb,AMS(scs,scb))
