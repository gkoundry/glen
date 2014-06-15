library('cvTools')
library('kernlab')
d=read.csv('training_imp.csv',na.string='-999.0')
dx=subset(d,select=-c(Weight,EventId))
folds <- cvFolds(NROW(d), K=3)
for(i in c(1,2,3)) {
  train <- dx[folds$subsets[folds$which != i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  validation <- dx[folds$subsets[folds$which == i], ]
  ev <- d[folds$subsets[folds$which == i], ]$EventId
  m=ksvm(Label ~ .,data=train,C=5)
  p=predict(m,validation)
  if(i==1) {
	pa=cbind(ev,p)
  } else {
	pa=rbind(pa,cbind(ev,p))
  }
}
write.csv(pa,'train_ksvmc5a.csv')
dv=read.csv('test_imp.csv',na.string='-999.0')
m=ksvm(Label ~ .,data=dx,C=5)
p=predict(m,dv)
write.csv(cbind(dv$EventId,p),"test_ksvmc5a.csv")
