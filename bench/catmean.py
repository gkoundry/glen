import pandas
df=pandas.read_csv('/home/glen/datasets/testdata/kickcars-training-sample.csv')
df['AUCGUART']=df['AUCGUART'].fillna('null')
print df.groupby('AUCGUART').mean()['IsBadBuy']
