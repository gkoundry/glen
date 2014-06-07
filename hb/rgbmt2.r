library('cvTools')
library('gbm')
tr=200
LR=0.1
mn=500
mf=18
d=read.csv('training2.csv',na.string='-999.0')
d$Y[d$Label=='b']=0
d$Y[d$Label=='s']=1
dx=subset(d,select=-c(Label,Weight,PRI_jet_num,DER_deltaeta_jet_jet,DER_mass_jet_jet,DER_prodeta_jet_jet,DER_lep_eta_centrality,PRI_jet_subleading_pt,PRI_jet_subleading_eta,PRI_jet_subleading_phi))
folds <- cvFolds(NROW(d), K=3)
#for(i in c(1,2,3,4,5)) {
for(i in c(1,2,3)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='bernoulli',interaction.depth=mf,shrinkage=LR, w=(wtrain+4)/4)
  #m=gbm(Y ~ .,data=train,bag.fraction=1,n.trees=tr,verbose=FALSE,keep.data=FALSE,n.minobsinnode=mn,distribution='adaboost',interaction.depth=mf,shrinkage=LR, w=(wtrain+4)/4)
#  for(j in seq(1,100)) {
#     print(pretty.gbm.tree(m,j))
#  }
  p=predict(m,validation,n.trees=tr)
  if(i==1) {
	pa=cbind(validation$EventId,p)
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
  }
}
write.csv(pa,'predrgbm_t200_mn500_mf18_lr0p1w4cv3ct2.csv')
