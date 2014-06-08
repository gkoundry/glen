import pandas
import numpy as np
from sklearn.preprocessing import Imputer

X=pandas.read_csv("training.csv",na_values='-999.0')
print X.shape
y=X['Label']
y=(y=='s').astype(int)
X['Label']=y
print X.shape
imp = Imputer(strategy='median')
xtrain = imp.fit_transform(X.values)
print xtrain.shape
np.savetxt('training_imp.csv',np.hstack((np.reshape(X['EventId'].values,(-1,1)),xtrain)),fmt='%f',delimiter=',')
X=pandas.read_csv("test.csv",na_values='-999.0')
xtrain = imp.fit_transform(X.values)
np.savetxt('test_imp.csv',np.hstack((np.reshape(X['EventId'].values,(-1,1)),xtrain)),fmt='%f',delimiter=',')