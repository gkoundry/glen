library('cvTools')
library('gbm')
tr=1000
LR=0.05
mn=300
mf=12
d=read.csv('training.csv',na.string='-999.0')
#d$Y[d$Label=='s']=d$Weight[d$Label=='s']+1
#d$Y[d$Label=='b']=-d$Weight[d$Label=='b']
#d$Y[d$Label=='b']=0
d=subset(d,select=-c(Label))
folds <- cvFolds(NROW(d), K=3)
for(i in c(1,2,3)) {
  train <- d[folds$subsets[folds$which != i], ]
  validation <- d[folds$subsets[folds$which == i], ]
  m=gbm(Weight ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='gaussian',interaction.depth=mf,shrinkage=LR,n.cores=5) #, w=wtrain[rows]*2.0)
  p=predict(m,validation,n.trees=tr)
  if(i==1) {
	pa=cbind(validation$EventId,p)
	y = validation$Weight
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
	y = c(y,validation$Weight)
  }
}
print(paste(tr,LR,mn,mf,mean((pa[,2]-y)**2)))
write.csv(pa,paste('trainrgbmg_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))

