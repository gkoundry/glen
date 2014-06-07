library('cvTools')
library('gbm')
library('doMC')
tr=2
LR=0.1
mn=5
mf=7

registerDoMC(cores=3)

d=read.csv('short.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=3)
pa = foreach(i=1:3) %dopar% {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR, w=(wtrain+4)/4)
  p=predict(m,validation,n.trees=tr)
  cbind(validation$EventId,p)
}
