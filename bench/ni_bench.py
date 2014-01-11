import pandas
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import SGDRegressor,Ridge,LogisticRegression
from ModelingMachine.engine.tasks.converters import DesignMatrix2,Numeric_impute,Passthrough
from ModelingMachine.engine.tasks.transformers import Numeric_impute_predict
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.metrics import log_loss,mean_absolute_error
import numpy as np

#clf = SGDRegressor(loss='huber',penalty='l2',alpha=0.01,eta0=0.00001)
ni1 = Numeric_impute()
ni2 = Numeric_impute_predict()
dm2 = DesignMatrix2()
ps = Passthrough()

xx=1
def MAE(clf,X,y):
    p=clf.predict(X)
    return mean_absolute_error(y,p)

def LogLoss(clf,X,y):
    global xx
    p=clf.predict_proba(X)
    np.savetxt('testp'+str(xx)+'.out',p)
    xx+=1
    return log_loss(y,[i[1] for i in p])

def test1():
    clf2 = RandomForestRegressor(n_estimators=100,min_samples_leaf=5,n_jobs=-1)
    clf1 = Ridge()
    df=pandas.read_csv('/home/glen/datasets/testdata/fastiron_yearna10.csv')

    target = df.pop('SalePrice')
    num = df[['YearMade','MachineHoursCurrentMeter']]
    cat = dm2.fit_transform(df[['MachineID','ModelID','datasource','auctioneerID','UsageBand','saledate','fiModelDesc','fiBaseModel','fiSecondaryDesc','fiModelSeries','fiModelDescriptor','ProductSize','fiProductClassDesc','state','ProductGroup','ProductGroupDesc','Drive_System','Enclosure','Forks','Pad_Type','Ride_Control','Stick','Transmission','Turbocharged','Blade_Extension','Blade_Width','Enclosure_Type','Engine_Horsepower','Hydraulics','Pushblock','Ripper','Scarifier','Tip_Control','Tire_Size','Coupler','Coupler_System','Grouser_Tracks','Hydraulics_Flow','Track_Type','Undercarriage_Pad_Width','Stick_Length','Thumb','Pattern_Changer','Grouser_Type','Backhoe_Mounting','Blade_Type','Travel_Controls','Differential_Type','Steering_Controls']].astype(object))().toarray()

    num1 = ni1.fit_transform(num)()
    cn = ps.fit_transform(num)
    cn.add(cat)

    X1 = np.hstack((num1,cat))
    X2 = ni2.fit_transform(cn)()

    #np.savetxt('test1.out',X1,fmt='%.1f')
    #np.savetxt('test2.out',X2,fmt='%.1f')
    #for clf in (clf1,clf2):
    for clf in (clf1,):
        for X in ((X1,'ni'),(X2,'nip')):
            print 'fastiron '+clf.__class__.__name__+' '+X[1]+' '+str(np.mean(cross_val_score(clf, X[0], target, cv=5)))

def test2():
    clf2 = RandomForestClassifier(n_estimators=100,min_samples_leaf=5,n_jobs=-1)
    clf1 = LogisticRegression()
    df=pandas.read_csv('/home/glen/datasets/testdata/kickcars_nawc20.csv')

    target = df.pop('IsBadBuy')
    num = df[['VehYear','VehicleAge','WheelTypeID','VehOdo','MMRAcquisitionAuctionAveragePrice','MMRAcquisitionAuctionCleanPrice','MMRAcquisitionRetailAveragePrice','MMRAcquisitonRetailCleanPrice','MMRCurrentAuctionAveragePrice','MMRCurrentAuctionCleanPrice','MMRCurrentRetailAveragePrice','MMRCurrentRetailCleanPrice','BYRNO','WarrantyCost']].astype(float)
    cat = dm2.fit_transform(df[['PurchDate','Auction','Make','Model','Trim','SubModel','Color','Transmission','WheelType','Nationality','Size','TopThreeAmericanName','PRIMEUNIT','AUCGUART','VNZIP1','VNST','VehBCost','IsOnlineSale']].astype(object))().toarray()

    num1 = ni1.fit_transform(num)()
    cn = ps.fit_transform(num)
    cn.add(cat)

    X1 = np.hstack((num1,cat))
    X2 = ni2.fit_transform(cn)()

    #np.savetxt('test1.out',X1,fmt='%.1f')
    #np.savetxt('test2.out',X2,fmt='%.1f')
    #for clf in (clf1,clf2):
    for clf in (clf1,):
        for X in ((X1,'ni'),(X2,'nip')):
            print 'kickcars '+clf.__class__.__name__+' '+X[1]+' '+str(np.mean(cross_val_score(clf, X[0], target, cv=5,scoring=LogLoss)))

def test3():
    clf2 = RandomForestClassifier(n_estimators=100,min_samples_leaf=5,n_jobs=-1)
    clf1 = LogisticRegression()
    df=pandas.read_csv('/home/glen/datasets/testdata/rrec_na.csv')

    target = df.pop('Installed')
    num = df[['DependencyCount','SuggestionCount','ImportCount','ViewsIncluding']].astype(float)
    cat = dm2.fit_transform(df[['Package','User','CorePackage','RecommendedPackage','Maintainer','PackagesMaintaining','LogDependencyCount','LogSuggestionCount','LogImportCount','LogViewsIncluding','LogPackagesMaintaining']].astype(object))().toarray()

    num1 = ni1.fit_transform(num)()
    cn = ps.fit_transform(num)
    cn.add(cat)

    X1 = np.hstack((num1,cat))
    X2 = ni2.fit_transform(cn)()

    #for clf in (clf1,clf2):
    for clf in (clf1,):
        for X in ((X1,'ni'),(X2,'nip')):
            print 'r_recommend '+clf.__class__.__name__+' '+X[1]+' '+str(np.mean(cross_val_score(clf, X[0], target, cv=5,scoring=LogLoss)))

#test2()
#test1()
test3()
