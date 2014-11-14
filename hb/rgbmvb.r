library('cvTools')
library('gbm')

tr=1000
LR=0.05
mn=300
mf=12
s_mult=300
s_add=2
b_mult=2
b_add=1

d=read.csv('training.csv',na.string='-999.0')
d$Weight[d$Label=='s'] = d$Weight[d$Label=='s'] * s_mult + s_add
d$Weight[d$Label=='b'] = d$Weight[d$Label=='b'] * b_mult + b_add
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight,EventId))
dx$PRI_jet_num = as.factor(dx$PRI_jet_num)

v=read.csv('test.csv',na.string='-999.0')
m=gbm(Y ~ .,data=dx,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR,w=d$Weight)
p=predict(m,v,n.trees=tr,type="response")
write.csv(cbind(v$EventId,p),paste('testrgbmb300_2_2_1_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
