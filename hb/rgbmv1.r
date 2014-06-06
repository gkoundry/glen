library('cvTools')
library('gbm')
tr=200
LR=0.1
mn=500
mf=18
d=read.csv('training.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=5)
for(i in c(1,2,3,4,5)) {
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
write.csv(pa,'train_rgbmv1.csv')

dt=read.csv('test.csv',na.string='-999.0')
dt$PRI_jet_num = as.factor(dt$PRI_jet_num)
m=gbm(Y ~ .,data=dx,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR, w=(d$Weight+4)/4)
p=predict(m,dt,n.trees=tr)
write.csv(p,'test_rgbmv1.csv')
