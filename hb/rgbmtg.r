library('cvTools')
library('gbm')

tr=1000
LR=0.05
mn=30
mf=12

d=read.csv('training.csv',na.string='-999.0')
dx=subset(d,select=-c(Label,EventId))
dx[d$Label=='s',]$Weight = dx[d$Label=='s',]$Weight * -300
folds <- cvFolds(NROW(d), K=5)
for(i in c(1,2,3,4,5)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  etest <- d[folds$subsets[folds$which == i], ]$EventId
  m=gbm(Weight ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='gaussian',interaction.depth=mf,shrinkage=LR)
  p=predict(m,validation,n.trees=tr)
  if(i==1) {
	pa=cbind(etest,p)
	y = validation$Weight
  } else {
	pa=rbind(pa,cbind(etest,p))
	y = c(y,validation$Weight)
  }
}
print(paste(tr,LR,mn,mf,mean((pa[,2]-y)**2)))
write.csv(pa,paste('trainrgbmg_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))

