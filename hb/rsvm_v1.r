library('cvTools')
library('kernlab')
d=read.csv('training_imp.csv',na.string='-999.0')
dx=subset(d,select=-c(Weight))
folds <- cvFolds(NROW(d), K=5)
for(i in c(1,2,3,4,5)) {
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
write.csv(pa,'train_rsvm_v1.csv')

dt=read.csv('test_imp.csv',na.string='-999.0')
m=ksvm(Label ~ .,data=dx,C=5)
p=predict(m,dt)
write.csv(p,'test_rsvm_v1.csv')
