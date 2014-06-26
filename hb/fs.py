import pandas
import sys
sys.path.append('/home/glen/workspace/DataRobot')
from ModelingMachine.engine.metrics import direction_by_name, metric_by_name
from pyace import ace
p=pandas.read_csv('train_rgbm.csv')
t=pandas.read_csv('training.csv')
label=t.pop('Label')
wt=t.pop('Weight')
t['rsd'] = p['prob']-(label=='s').astype(int)
mt='MAD'
mdir = direction_by_name(mt)
mfunc = metric_by_name(mt)
for col in t.columns:
    t2=t.copy()
    for col2 in t.columns:
        if col2!='rsd':
            t2[col2] = t[col]*t[col2]
    imp = ace(t2, 'rsd', [], cv=True, K=-1, metric=mfunc, metric_dir=mdir)
    for i,j in enumerate( imp):
        print '%s %s %s' % (col2,t.columns[i],j[0])
    sys.stdout.flush()
