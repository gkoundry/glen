library('cvTools')
library('gbm')
tr=900
LR=0.05
mn=300
mf=12
d=read.csv('training.csv',na.string='-999.0')
d=subset(d,select=-c(Label))
m=gbm(Weight ~ .,data=d,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='gaussian',interaction.depth=mf,shrinkage=LR,n.cores=5) #, w=wtrain[rows]*2.0)
v=read.csv('test.csv',na.string='-999.0')
p=predict(m,v,n.trees=tr)
write.csv(p,paste('predrgbmgp_',tr,"_",LR,"_",mn,"_",mf,'.csv',sep=""))
