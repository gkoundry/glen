library('cvTools')
library('gam')
d=read.csv('training_imp.csv',na.string='-999.0')
dx=subset(d,select=-c(Weight))
folds <- cvFolds(NROW(d), K=5)
for(i in c(1,2,3,4,5)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  if(i==1) {
	pa=validation$EventId
  } else {
	pa=rbind(validation$EventId)
  }
}
write.csv(pa,'test1.out')

