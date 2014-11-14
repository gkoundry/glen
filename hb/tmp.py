import pandas as pd
d=pd.read_csv('wt.txt',sep=' ')
d['Weight'].value_counts().to_csv('wtf.txt')
