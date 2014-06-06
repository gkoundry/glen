library('cvTools')
library('gam')
d=read.csv('training_imp.csv',na.string='-999.0')
dx=subset(d,select=-c(Weight))
folds <- cvFolds(NROW(d), K=5)
for(i in c(1,2,3,4,5)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  m=gam(Label ~ lo(EventId,degree=2)+lo(DER_mass_MMC,degree=2)+lo(DER_mass_transverse_met_lep,degree=2)+lo(DER_mass_vis,degree=2)+lo(DER_pt_h,degree=2)+lo(DER_deltaeta_jet_jet,degree=2)+lo(DER_mass_jet_jet,degree=2)+lo(DER_prodeta_jet_jet,degree=2)+lo(DER_deltar_tau_lep,degree=2)+lo(DER_pt_tot,degree=2)+lo(DER_sum_pt,degree=2)+lo(DER_pt_ratio_lep_tau,degree=2)+lo(DER_met_phi_centrality,degree=2)+lo(DER_lep_eta_centrality,degree=2)+lo(PRI_tau_pt,degree=2)+lo(PRI_tau_eta,degree=2)+lo(PRI_tau_phi,degree=2)+lo(PRI_lep_pt,degree=2)+lo(PRI_lep_eta,degree=2)+lo(PRI_lep_phi,degree=2)+lo(PRI_met,degree=2)+lo(PRI_met_phi,degree=2)+lo(PRI_met_sumet,degree=2)+PRI_jet_num+lo(PRI_jet_leading_pt,degree=2)+lo(PRI_jet_leading_eta,degree=2)+lo(PRI_jet_leading_phi,degree=2)+lo(PRI_jet_subleading_pt,degree=2)+lo(PRI_jet_subleading_eta,degree=2)+lo(PRI_jet_subleading_phi,degree=2)+lo(PRI_jet_all_pt,degree=2),data=train,family=binomial())
  p=predict(m,validation)
  if(i==1) {
	pa=cbind(validation$EventId,p)
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
  }
}
write.csv(pa,'predgamd2.csv')
