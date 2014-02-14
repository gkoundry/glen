import datasets
from tesla.ensemble import RandomForestClassifier
import time

ds = datasets.get_datasets(name='kickcars_small')

st=time.time()
clf = RandomForestClassifier(n_estimators=800)
clf.fit(*datasets.get_data(ds))
print time.time()-st
