library('cvTools')
library('gam')
d=read.csv('training_imp.csv',na.string='-999.0')
dx=subset(d,select=-c(Weight))
folds <- cvFolds(NROW(d), K=5)
for(i in c(1,2,3,4,5)) {
  train <- dx[folds$subsets[folds$which != i], ]
  validation <- dx[folds$subsets[folds$which == i], ]
  wtrain <- d[folds$subsets[folds$which != i], ]$Weight
  m=gam(Label ~ lo(DER_mass_MMC,span=0.2)+lo(DER_mass_transverse_met_lep,span=0.2)+lo(DER_mass_vis,span=0.2)+lo(DER_pt_h,span=0.2)+lo(DER_deltaeta_jet_jet,span=0.2)+lo(DER_mass_jet_jet,span=0.2)+lo(DER_prodeta_jet_jet,span=0.2)+lo(DER_deltar_tau_lep,span=0.2)+lo(DER_pt_tot,span=0.2)+lo(DER_sum_pt,span=0.2)+lo(DER_pt_ratio_lep_tau,span=0.2)+lo(DER_met_phi_centrality,span=0.2)+lo(DER_lep_eta_centrality,span=0.2)+lo(PRI_tau_pt,span=0.2)+lo(PRI_tau_eta,span=0.2)+lo(PRI_tau_phi,span=0.2)+lo(PRI_lep_pt,span=0.2)+lo(PRI_lep_eta,span=0.2)+lo(PRI_lep_phi,span=0.2)+lo(PRI_met,span=0.2)+lo(PRI_met_phi,span=0.2)+lo(PRI_met_sumet,span=0.2)+PRI_jet_num+lo(PRI_jet_leading_pt,span=0.2)+lo(PRI_jet_leading_eta,span=0.2)+lo(PRI_jet_leading_phi,span=0.2)+lo(PRI_jet_subleading_pt,span=0.2)+lo(PRI_jet_subleading_eta,span=0.2)+lo(PRI_jet_subleading_phi,span=0.2)+lo(PRI_jet_all_pt,span=0.2),data=train,family=binomial())
  p=predict(m,validation)
  if(i==1) {
	pa=cbind(validation$EventId,p)
  } else {
	pa=rbind(pa,cbind(validation$EventId,p))
  }
}
write.csv(pa,'train_gam_v1.csv')

#dt=read.csv('test_imp.csv',na.string='-999.0')
#m=gam(Label ~ lo(DER_mass_MMC,span=0.2)+lo(DER_mass_transverse_met_lep,span=0.2)+lo(DER_mass_vis,span=0.2)+lo(DER_pt_h,span=0.2)+lo(DER_deltaeta_jet_jet,span=0.2)+lo(DER_mass_jet_jet,span=0.2)+lo(DER_prodeta_jet_jet,span=0.2)+lo(DER_deltar_tau_lep,span=0.2)+lo(DER_pt_tot,span=0.2)+lo(DER_sum_pt,span=0.2)+lo(DER_pt_ratio_lep_tau,span=0.2)+lo(DER_met_phi_centrality,span=0.2)+lo(DER_lep_eta_centrality,span=0.2)+lo(PRI_tau_pt,span=0.2)+lo(PRI_tau_eta,span=0.2)+lo(PRI_tau_phi,span=0.2)+lo(PRI_lep_pt,span=0.2)+lo(PRI_lep_eta,span=0.2)+lo(PRI_lep_phi,span=0.2)+lo(PRI_met,span=0.2)+lo(PRI_met_phi,span=0.2)+lo(PRI_met_sumet,span=0.2)+PRI_jet_num+lo(PRI_jet_leading_pt,span=0.2)+lo(PRI_jet_leading_eta,span=0.2)+lo(PRI_jet_leading_phi,span=0.2)+lo(PRI_jet_subleading_pt,span=0.2)+lo(PRI_jet_subleading_eta,span=0.2)+lo(PRI_jet_subleading_phi,span=0.2)+lo(PRI_jet_all_pt,span=0.2),data=dx,family=binomial())
#p=predict(m,dt)
#write.csv(cbind(dt$EventId,p),'test_gam_v1.csv')
