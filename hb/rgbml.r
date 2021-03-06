library('cvTools')
library('gbm')

tr=200
LR=0.05
mn=50
mf=12

d=read.csv('training.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=3)
#for(i in c(1,2,3)) {
#  train <- dx[folds$subsets[folds$which != i], ]
#  validation <- dx[folds$subsets[folds$which == i], ]
#  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
#  ytest <- dx[folds$subsets[folds$which != i], ]$Y
#  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
#  p=predict(m,validation,n.trees=tr,type="response")
#  if(i==1) {
#	pa=cbind(validation$EventId,p)
#	y = validation$Y
#  } else {
#	pa=rbind(pa,cbind(validation$EventId,p))
#	y = c(y,validation$Y)
#  }
#}
#print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
#write.csv(pa,paste('predrgbml_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
#
#tr=400
#
#for(i in c(1,2,3)) {
#  train <- dx[folds$subsets[folds$which != i], ]
#  validation <- dx[folds$subsets[folds$which == i], ]
#  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
#  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
#  p=predict(m,validation,n.trees=tr,type="response")
#  if(i==1) {
#	pa=cbind(validation$EventId,p)
#	y = validation$Y
#  } else {
#	pa=rbind(pa,cbind(validation$EventId,p))
#	y = c(y,validation$Y)
#  }
#}
#print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
#write.csv(pa,paste('predrgbml_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
#
#tr=600
#
#for(i in c(1,2,3)) {
#  train <- dx[folds$subsets[folds$which != i], ]
#  validation <- dx[folds$subsets[folds$which == i], ]
#  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
#  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
#  p=predict(m,validation,n.trees=tr,type="response")
#  if(i==1) {
#	pa=cbind(validation$EventId,p)
#	y = validation$Y
#  } else {
#	pa=rbind(pa,cbind(validation$EventId,p))
#	y = c(y,validation$Y)
#  }
#}
#print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
#write.csv(pa,paste('predrgbml_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
#
tr=200
LR=0.05
mn=300
mf=12
#
#d=read.csv('training.csv',na.string='-999.0')
#d$Y[d$Label=='b']=0
#d$Y[d$Label=='s']=1
#dx=subset(d,select=-c(Label,Weight))
#dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
#folds <- cvFolds(NROW(d), K=3)
#for(i in c(1,2,3)) {
#  train <- dx[folds$subsets[folds$which != i], ]
#  validation <- dx[folds$subsets[folds$which == i], ]
#  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
#  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
#  p=predict(m,validation,n.trees=tr,type="response")
#  if(i==1) {
#	pa=cbind(validation$EventId,p)
#	y = validation$Y
#  } else {
#	pa=rbind(pa,cbind(validation$EventId,p))
#	y = c(y,validation$Y)
#  }
#}
#print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
#write.csv(pa,paste('predrgbml_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
#
#tr=400
#
#for(i in c(1,2,3)) {
#  train <- dx[folds$subsets[folds$which != i], ]
#  validation <- dx[folds$subsets[folds$which == i], ]
#  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
#  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
#  p=predict(m,validation,n.trees=tr,type="response")
#  if(i==1) {
#	pa=cbind(validation$EventId,p)
#	y = validation$Y
#  } else {
#	pa=rbind(pa,cbind(validation$EventId,p))
#	y = c(y,validation$Y)
#  }
#}
#print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
#write.csv(pa,paste('predrgbml_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
#
#tr=600
#
#for(i in c(1,2,3)) {
#  train <- dx[folds$subsets[folds$which != i], ]
#  validation <- dx[folds$subsets[folds$which == i], ]
#  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
#  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
#  p=predict(m,validation,n.trees=tr,type="response")
#  if(i==1) {
#	pa=cbind(validation$EventId,p)
#	y = validation$Y
#  } else {
#	pa=rbind(pa,cbind(validation$EventId,p))
#	y = c(y,validation$Y)
#  }
#}
#print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
#write.csv(pa,paste('predrgbml_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))

tr=900

for(i in c(1,2,3)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
  p=predict(m,validation,n.trees=tr,type="response")
  if(i==1) {
	pa=cbind(validation$EventId,p)
	y = validation$Y
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
	y = c(y,validation$Y)
  }
}
print(paste(tr,LR,mn,mf,-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
write.csv(pa,paste('predrgbml_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
