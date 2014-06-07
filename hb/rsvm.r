library('cvTools')
library('kernlab')
d=read.csv('training_imp.csv',na.string='-999.0')
dx=subset(d,select=-c(Weight))
folds <- cvFolds(NROW(d), K=3)
for(i in c(1,2,3)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  m=ksvm(Label ~ .,data=train,C=5)
  p=predict(m,validation)
  if(i==1) {
	pa=cbind(validation$EventId,p)
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
  }
}
write.csv(pa,'predksvmc5')
dv=read.csv('test_imp.csv',na.string='-999.0')
m=ksvm(Label ~ .,data=dx,C=5)
p=predict(m,dv)
write.csv(cbind(dv$EventId,p),"testsvmc5.csv")
