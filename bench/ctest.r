library('Hmisc')
d=read.csv('/home/glen/datasets/testdata/kickcars-training-sample.csv')
rcorr(d$VehicleAge,d$IsBadBuy,type="spearman")
