library('cvTools')
library('gbm')

tr=1000
LR=0.05
mn=300
mf=12

d=read.csv('train_shift.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight,EventId))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=3)

for(i in c(1,2,3)) {
  train <- dx[folds$subsets[folds$which != i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  validation <- dx[folds$subsets[folds$which == i], ]
  etest <- d[folds$subsets[folds$which == i], ]$EventId
  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR,weights=(wtrain+4)/4)
  p=predict(m,validation,n.trees=tr,type="response")
  if(i==1) {
	pa=cbind(etest,p)
	y = validation$Y
  } else {
	pa=rbind(pa,cbind(etest,p))
	y = c(y,validation$Y)
  }
}
write.csv(-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2])),paste('rgbmtb',tr,LR,mn,mf,".log",sep="_"))
write.csv(pa,paste('train_rgbmbsw',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
