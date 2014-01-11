import pandas
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import SGDRegressor,Ridge,LogisticRegression,SGDClassifier
from ModelingMachine.engine.tasks.converters import DesignMatrix2,Numeric_impute,Passthrough,ConvertLevels
from ModelingMachine.engine.tasks.ElasticNet import ElasticNet
from ModelingMachine.engine.tasks.rmars import EarthWrapperR,EarthWrapperC
from sklearn.metrics import log_loss,mean_absolute_error,mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np
import time
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from rpy2.robjects.numpy2ri import numpy2ri
robjects.conversion.py2ri = numpy2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import IntVector
glmnet = importr("glmnet")
acepack = importr("acepack")

class GlmnetWrapper(object):
    def __init__(self,**args):
        self.model = None
        self.args = args
        self.used_vars = []

    def score(self,X,act):
        pred=self.predict(X)
        if self.args['family']=='binomial':
            return logloss(act,pred)
        else:
            return MAD(act,pred)

    def set_params(self,**args):
        self.args.update(args)
        return self

    def get_params(self,deep=True):
        return self.args

    def fit(self,X,Y,**args):
        self.args.update(args)
        self.model = glmnet.glmnet(X,np.reshape(Y,[-1,1]),**self.args)
        return self

    def predict(self,X):
        return glmnet.predict_glmnet(self.model,X,**{'s':self.args['lambda'],'type':"response"})

    def predict_proba(self,X):
        return glmnet.predict_glmnet(self.model,X,**{'s':self.args['lambda'],'type':"class"})

#clf = SGDRegressor(loss='huber',penalty='l2',alpha=0.01,eta0=0.00001)
ni1 = Numeric_impute()
dm2 = DesignMatrix2()
clvl = ConvertLevels()

class ElasticNetC(object):
    def __init__(self,**args):
        self.args=args
        self.clf=ElasticNet()

    def fit(self,X,y,**args):
        self.args.update(args)
        self.clf.fit(np.ascontiguousarray(X).astype(float),y.astype(float),path=False,**self.args)

    def predict(self,X):
        return self.clf.predict(np.ascontiguousarray(X).astype(float))

    def predict_proba(self,X):
        return self.clf.predict(np.ascontiguousarray(X).astype(float))

    def set_params(self,**args):
        self.args.update(args)

    def get_params(self,deep=False):
        return self.args

def MAE(clf,X,y):
    p=clf.predict(X)
    return mean_absolute_error(y,p)

def MSE(clf,X,y):
    p=clf.predict(X)
    return mean_squared_error(y,p)

def LogLoss(clf,X,y):
    p=clf.predict_proba(X)
    if not hasattr(p,'shape'):
        p=1/(1+np.exp(-np.array(p)))
    if len(p.shape)==1 or p.shape[1]==1:
        p=np.column_stack((1-p,p))
    #np.savetxt('test.out',p,fmt="%.5f")
    return log_loss(y,p)

def test1():
    clf1 = Ridge()
    ss = StandardScaler()
    df=pandas.read_csv('/home/glen/datasets/testdata/fastiron_yearna10.csv')

    target = df.pop('SalePrice')
    num = df[['YearMade','MachineHoursCurrentMeter']]
    cat = dm2.fit_transform(df[['MachineID','ModelID','datasource','auctioneerID','UsageBand','saledate','fiModelDesc','fiBaseModel','fiSecondaryDesc','fiModelSeries','fiModelDescriptor','ProductSize','fiProductClassDesc','state','ProductGroup','ProductGroupDesc','Drive_System','Enclosure','Forks','Pad_Type','Ride_Control','Stick','Transmission','Turbocharged','Blade_Extension','Blade_Width','Enclosure_Type','Engine_Horsepower','Hydraulics','Pushblock','Ripper','Scarifier','Tip_Control','Tire_Size','Coupler','Coupler_System','Grouser_Tracks','Hydraulics_Flow','Track_Type','Undercarriage_Pad_Width','Stick_Length','Thumb','Pattern_Changer','Grouser_Type','Backhoe_Mounting','Blade_Type','Travel_Controls','Differential_Type','Steering_Controls']].astype(object))().toarray()

    num1 = ni1.fit_transform(num)()

    X1 = ss.fit_transform(np.hstack((num1,cat)))

    for lm in (1000,1,0.1,0.01,0.001,0.0001):
        for a in (0.1,0.3,0.6):
            clf2 = ElasticNetC(distribution='Gaussian',lambda_=lm,alpha=a,tolerance=0.001)
            clf3 = SGDRegressor(alpha=lm,l1_ratio=a,eta0=0.001,penalty='elasticnet')
            for clf in (clf1,clf2,clf3):
            #for clf in (clf2,):
                st = time.time()
                print 'fastiron %20s a %3.1f lm %8.4f sc %9.2f tm %5.2f' % (clf.__class__.__name__,a,lm,np.mean(cross_val_score(clf, X1, target, cv=5,scoring=MSE)),time.time()-st)
            print ''

def test2a():
    clf1 = LogisticRegression()
    ss = StandardScaler()
    df=pandas.read_csv('/home/glen/datasets/testdata/credit-train-small.csv')

    target = df.pop('SeriousDlqin2yrs')
    num = df

    num1 = ni1.fit_transform(num)()

    X1 = ss.fit_transform(num1)

    for lm in (1,0.1,0.01,0.001):
        for a in (0.1,): #,0.3,0.6):
            clf2 = ElasticNetC(distribution='Bernoulli',lambda_=lm,alpha=a)
            clf3 = SGDClassifier(alpha=lm,l1_ratio=a,loss='log',eta0=0.001,penalty='elasticnet')
            for clf in (clf2,clf3):
                print 'credit '+clf.__class__.__name__+' a='+str(a)+' lm='+str(lm)+' '+str(np.mean(cross_val_score(clf, X1, target, cv=5,scoring=LogLoss)))
            print ''

def test_kc():
    clf1 = LogisticRegression()
    ss = StandardScaler()
    df=pandas.read_csv('/home/glen/datasets/testdata/kickcars_nawc20.csv')

    target = df.pop('IsBadBuy')
    df['rand1']=np.random.rand(df.shape[0])
    df['rand2']=np.random.poisson(5,df.shape[0])
    df['rand3']=np.random.choice(['a','b','c','d','e'],df.shape[0])
    num_cols=['rand1','rand2','RefId','VehYear','VehicleAge','WheelTypeID','VehOdo','MMRAcquisitionAuctionAveragePrice','MMRAcquisitionAuctionCleanPrice','MMRAcquisitionRetailAveragePrice','MMRAcquisitonRetailCleanPrice','MMRCurrentAuctionAveragePrice','MMRCurrentAuctionCleanPrice','MMRCurrentRetailAveragePrice','MMRCurrentRetailCleanPrice','BYRNO','WarrantyCost']
    cat_cols=['rand3','PurchDate','Auction','Make','Model','Trim','SubModel','Color','Transmission','WheelType','Nationality','Size','TopThreeAmericanName','PRIMEUNIT','AUCGUART','VNZIP1','VNST','VehBCost','IsOnlineSale']
    num = df[num_cols].astype(float)
    cat = dm2.fit_transform(df[cat_cols].astype(object))().toarray()

    num1 = ni1.fit_transform(num)()

    X1 = ss.fit_transform(np.hstack((num1,cat)))
    for i in df:
        if i in num_cols:
            x = ni1.fit_transform(pandas.DataFrame(df[i]).astype(float))()
            rsq = acepack.ace(x,target,cat=IntVector([0,]))
        else:
            x = clvl.fit_transform(pandas.DataFrame(df[i]).astype(object))()
            rsq = acepack.ace(x,target,cat=IntVector([0,1]))
        print '%-36s %8.5f' % (i,rsq.rx2('rsq')[0])
    return
    #np.savetxt("kcX.csv",X1,delimiter=",",fmt='%.8f',header=','.join(['f'+str(i) for i in range(X1.shape[1])]))
    #np.savetxt("kcY.csv",target,delimiter=",",fmt='%.8f',header='Y')

    for lm in (1000,1,0.1,0.01,0.001):
        for a in (0.1,0.3,0.6):
            clf2 = ElasticNetC(distribution='Bernoulli',lambda_=lm,alpha=a,tolerance=0.0001)
            clf3 = SGDClassifier(alpha=lm,l1_ratio=a,loss='log',eta0=0.001,penalty='elasticnet')
            clf4 = GlmnetWrapper(**{'family':'binomial','alpha':a,'lambda':lm})
            for clf in (clf2,clf3,clf4):
                st = time.time()
                print 'kickcars %20s a %3.1f lm %8.4f sc %9.4f tm %5.2f' % (clf.__class__.__name__,a,lm,np.mean(cross_val_score(clf, X1, target, cv=5,scoring=LogLoss)),time.time()-st)
            print ''

def test3():
    clf2 = RandomForestClassifier(n_estimators=100,min_samples_leaf=5,n_jobs=-1)
    clf1 = LogisticRegression()
    df=pandas.read_csv('/home/glen/datasets/testdata/rrec_na.csv')

    target = df.pop('Installed')
    num = df[['DependencyCount','SuggestionCount','ImportCount','ViewsIncluding']].astype(float)
    cat = dm2.fit_transform(df[['Package','User','CorePackage','RecommendedPackage','Maintainer','PackagesMaintaining','LogDependencyCount','LogSuggestionCount','LogImportCount','LogViewsIncluding','LogPackagesMaintaining']].astype(object))().toarray()

    num1 = ni1.fit_transform(num)()

    X1 = np.hstack((num1,cat))

    for clf in (clf1,):
        for X in ((X1,'ni'),(X2,'nip')):
            print 'r_recommend '+clf.__class__.__name__+' '+X[1]+' '+str(np.mean(cross_val_score(clf, X[0], target, cv=5,scoring=LogLoss)))

test_kc()
#test2a()
#test1()
#test3()
