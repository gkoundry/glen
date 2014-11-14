library('cvTools')
library('gbm')

tr=100
LR=0.05
mn=300
mf=7

d=read.csv('training.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight,EventId))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)
folds <- cvFolds(NROW(d), K=3)

m=list()
for(i in c(1,2,3)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  etest <- d[folds$subsets[folds$which == i], ]$EventId
  m[[i]]=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=TRUE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR)
  p=predict(m[[i]],validation,n.trees=tr,type="response")
  p=pmin(0.9999,pmax(0.0001,p))
  if(i==1) {
	pa=cbind(etest,p)
	y = validation$Y
  } else {
	pa=rbind(pa,cbind(etest,p))
	y = c(y,validation$Y)
  }
}
print(-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2])))
flush.console()
for(j in seq(15)) {
    tr=tr+100
	for(i in c(1,2,3)) {
	  train <- dx[folds$subsets[folds$which != i], ]
	  validation <- dx[folds$subsets[folds$which == i], ]
	  etest <- d[folds$subsets[folds$which == i], ]$EventId
	  mi = gbm.more(m[[i]],n.new.trees=100)
	  p=predict(mi,validation,n.trees=tr,type="response")
	  p=pmin(0.9999,pmax(0.0001,p))
	  m[[i]]=mi
	  if(i==1) {
		pa=cbind(etest,p)
		y = validation$Y
	  } else {
		pa=rbind(pa,cbind(etest,p))
		y = c(y,validation$Y)
	  }
	}
	print(paste(tr," ",-mean(y*log(pa[,2])+(1-y)*log(1-pa[,2]))))
	flush.console()
}
write.csv(pa,paste('trainrgbmb',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
