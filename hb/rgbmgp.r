library('cvTools')
library('gbm')
tr=400
LR=0.1
mn=50
mf=7
d=read.csv('training.csv',na.string='-999.0')
v=read.csv('test.csv',na.string='-999.0')
d$Y[d$Label=='s']=d$Weight[d$Label=='s']+1
d$Y[d$Label=='b']=-d$Weight[d$Label=='b']
wtrain=d$Weight
d=subset(d,select=-c(Label,Weight))
m=gbm(Y ~ .,data=d,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='gaussian',interaction.depth=mf,shrinkage=LR,n.cores=5) #, w=wtrain[rows]*2.0)
p=predict(m,v,n.trees=tr)
write.csv(cbind(v$EventId,p),'predrgbmgrp.csv')
