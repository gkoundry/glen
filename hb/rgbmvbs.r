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

v=read.csv('test_shift.csv',na.string='-999.0')
m=gbm(Y ~ .,data=dx,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR,weights=(d$Weight+4)/4)
p=predict(m,v,n.trees=tr,type="response")
write.csv(cbind(v$EventId,p),paste('testrgbmbsw',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
