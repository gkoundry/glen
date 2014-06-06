library('cvTools')
library('gbm')
library('doMC')
tr=100
LR=0.1
mn=500
mf=18
registerDoMC(cores=3)

d=read.csv('training.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=3)
for(j in c(1,2,3,4,5,6,7)) {
	foreach(i=1:3) %dopar% {
	  train <- dx[folds$subsets[folds$which != i], ]
	  validation <- dx[folds$subsets[folds$which == i], ]
	  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
	  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR, w=(wtrain+4)/4)
	  p=predict(m,validation,n.trees=tr)
	  if(i==1) {
		pa=cbind(validation$EventId,p)
	  } else {
		pa=rbind(pa,cbind(validation$EventId,p))
	  }
	}
	d$Weight = d$Weight * (1+0.1*(pa>0.0 & d$Y==0))
	write.csv(pa,paste('predrgbm_',j,'.csv',sep=""))
}
