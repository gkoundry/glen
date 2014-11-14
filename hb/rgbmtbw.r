library('cvTools')
library('gbm')

tr=1000
LR=0.05
mn=300
mf=12

d=read.csv('training.csv',na.string='-999.0')
d$Weight[d$Label=='s'] = d$Weight[d$Label=='s'] * 1200
d$Weight[d$Label=='b'] = d$Weight[d$Label=='b'] * 2
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight,EventId))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=5)

for(i in c(1,2,3,4,5)) {
  train <- dx[folds$subsets[folds$which != i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  validation <- dx[folds$subsets[folds$which == i], ]
  etest <- d[folds$subsets[folds$which == i], ]$EventId
  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR,w=wtrain)
  p=predict(m,validation,n.trees=tr,type="response")
  if(i==1) {
	pa=cbind(etest,p)
	y = validation$Y
  } else {
	pa=rbind(pa,cbind(etest,p))
	y = c(y,validation$Y)
  }
}
print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
write.csv(pa,paste('train_rgbmbw_',tr,"_",LR,"_",mn,"_",mf,'_1200_2.csv',sep=""))
