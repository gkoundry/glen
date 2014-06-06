library('cvTools')
library('gbm')
tr=200
LR=0.1
mn=500
mf=18
d=read.csv('training.csv',na.string='-999.0')
dl=read.csv('lrgbm.csv')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=3)
#for(i in c(1,2,3,4,5)) {
for(i in c(1,2,3)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  lro <- dl[folds$subsets[folds$which != i], ]$pred
  lrov <- dl[folds$subsets[folds$which == i], ]$pred
  m=gbm(Y ~ . + offset(lro),data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR, w=(wtrain+4)/4)
  #m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='adaboost',interaction.depth=mf,shrinkage=LR, w=(wtrain+4)/4)
#  for(j in seq(1,100)) {
#     print(pretty.gbm.tree(m,j))
#  }
  p=predict(m,validation,n.trees=tr)+lrov
  if(i==1) {
	pa=cbind(validation$EventId,p)
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
  }
}
write.csv(pa,'predrgbm_t200_mn500_mf18_lr0p1w4cv3co.csv')
