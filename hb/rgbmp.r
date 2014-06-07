library('cvTools')
library('gbm')
tr=300
LR=0.1
mn=500
mf=7
d=read.csv('training.csv',na.string='-999.0')
v=read.csv('test.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight))
wtrain=d$Weight
m=gbm(Y ~ .,data=dx,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR, w=(wtrain+4)/4)
p=predict(m,v,n.trees=tr)
write.csv(cbind(v$EventId,p),'predrgbm_t300_mn500_mf7_lr0p1w4p.csv')
