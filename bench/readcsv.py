import pandas

d = pandas.read_csv('/home/glen/datasets/testdata/trainingDataWithoutNegativeWeights1k.csv')
print d['noFlash'].astype(float)
for c in d.columns:
    print c+' '+str(d[c].dtype)+' '+str(d[c].count())
