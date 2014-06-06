library('cvTools')
library('mgcv')
d=read.csv('training_imp.csv',na.string='-999.0')
dx=subset(d,select=-c(Weight))
folds <- cvFolds(NROW(d), K=5)
for(i in c(1,2,3,4,5)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  m=bam(Label ~ s(EventId)+s(DER_mass_MMC)+s(DER_mass_transverse_met_lep)+s(DER_mass_vis)+s(DER_pt_h)+s(DER_deltaeta_jet_jet)+s(DER_mass_jet_jet)+s(DER_prodeta_jet_jet)+s(DER_deltar_tau_lep)+s(DER_pt_tot)+s(DER_sum_pt)+s(DER_pt_ratio_lep_tau)+s(DER_met_phi_centrality)+s(DER_lep_eta_centrality)+s(PRI_tau_pt)+s(PRI_tau_eta)+s(PRI_tau_phi)+s(PRI_lep_pt)+s(PRI_lep_eta)+s(PRI_lep_phi)+s(PRI_met)+s(PRI_met_phi)+s(PRI_met_sumet)+PRI_jet_num+s(PRI_jet_leading_pt)+s(PRI_jet_leading_eta)+s(PRI_jet_leading_phi)+s(PRI_jet_subleading_pt)+s(PRI_jet_subleading_eta)+s(PRI_jet_subleading_phi)+s(PRI_jet_all_pt),data=train,family=binomial())
  p=predict(m,validation)
  if(i==1) {
	pa=cbind(validation$EventId,p)
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
  }
}
write.csv(pa,'predbam.csv')
