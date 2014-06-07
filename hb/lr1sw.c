#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define FOLDS 2
#define LR 0.00005
#define ROWS 250000
#define ROWST 550000
#define COLS 31
#define COLS2 531

char line[4096];
double x[ROWS][COLS2],test[ROWS];
double y[ROWS],w[ROWS];
double srt[ROWS],predt[ROWS];
int use[COLS2];
int id[ROWS],idt[ROWST];
//
// MERGE DUPS
// 
int has_na[] = {0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0};
int na_ind[] = {0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0};

int cmpd(const void *a,const void *b) {
	return (int)(*((double *)a)-*((double *)b));
}
double AMS(double s, double b) {
	double br,radicand;

    br = 10.0;
    radicand = 2 *( (s+b+br) * log (1.0 + s/(b+br)) -s);
    return sqrt(radicand);
}


double max_AMS() {

double sc,bc,th,a,maxa; //,maxth;
int r;

	maxa=0;
	for(th=0;th<4;th+=0.05) {
		sc=0;
		bc=0;
		for(r=0;r<ROWS;r++) {
			if(predt[r]>th) {
				if(y[r]==1) {
					sc += w[r];
				} else {
					bc += w[r];
				}
			}
		}
		a=AMS(sc,bc);
		if(a>maxa) {
			maxa=a;
//			maxth=th;
		}
	}
	return maxa;
}

int main() {

char *p;
int ci2,ci,ri,tc,bestc,mc;
double besta,sd[COLS2],avg[COLS2],med;
FILE *fp;

	for(ri=0;ri<ROWS;ri++) {
		test[ri] = rand() % FOLDS;
	}

	fp=fopen("training.csv","r");
	p = fgets(line,4096,fp);
	ri=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		id[ri]=atoi(p);
		ri++;
	}
	fclose(fp);

	fp=fopen("training.csv","r");
	p = fgets(line,4096,fp);
	ri=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(ci=0;ci<COLS;ci++) {
			x[ri][ci] = atof(p);
			p=strtok(NULL,","); 
		}
		w[ri] = atof(p);
		p=strtok(NULL,","); 
		if(p[0]=='s' || p[0]=='1')
			y[ri]=1;
		else
			y[ri]=0;
		ri+=1;
	}
	fclose(fp);
	if(ri!=ROWS) {
		fprintf(stderr,"ERROR: incorrect rows %d vs %d\n",ROWS,ri);
		exit(1);
	}

	fp=fopen("smooth_gaussian_10.000000_10.csv","r");
	p = fgets(line,4096,fp);
	ri=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(ci=0;ci<COLS;ci++) {
			x[ri][31+ci] = atof(p);
			p=strtok(NULL,","); 
		}
		w[ri] = atof(p);
		p=strtok(NULL,","); 
		if(p[0]=='s' || p[0]=='1')
			y[ri]=1;
		else
			y[ri]=0;
		ri+=1;
	}
	fclose(fp);
	if(ri!=ROWS) {
		fprintf(stderr,"ERROR: incorrect rows %d vs %d\n",ROWS,ri);
		exit(1);
	}

	mc = 0;
	for(ci=0;ci<COLS;ci++) {
		if(has_na[ci]) {
			for(ri=0;ri<ROWS;ri++) {
				srt[ri] = x[ri][ci];
			}
			qsort(srt,ROWS,sizeof(double),cmpd);
			med = srt[ROWS/2];
			for(ri=0;ri<ROWS;ri++) {
				if(x[ri][ci] == -999) {
					x[ri][ci] = med;
					if(na_ind[ci]) x[ri][2*COLS+mc]=1;
				} else {
					if(na_ind[ci]) x[ri][2*COLS+mc]=0;
				}
			}
			if(na_ind[ci]) mc++;
		}
	}

	mc=65;
	for(ci=0;ci<COLS2;ci++) {
		for(ci2=ci+1;ci2<COLS2;ci2++) {
			if(ci<31 && ci2<31) {
				for(ri=0;ri<ROWS;ri++) {
					x[ri][mc]=x[ri][ci]*x[ri][ci2];
				}
				mc++;
			}
		}
	}

	for(ci=0;ci<COLS2;ci++) {
		avg[ci] = 0;
		for(ri=0;ri<ROWS;ri++) {
			avg[ci] += x[ri][ci];
		}
		avg[ci] /= ROWS;
		sd[ci] = 0;
		for(ri=0;ri<ROWS;ri++) {
			sd[ci] += (avg[ci] - x[ri][ci]) * (avg[ci] - x[ri][ci]);
		}
		sd[ci] = sqrt(sd[ci]/ROWS);
		if(sd[ci]>0.00001) {
			for(ri=0;ri<ROWS;ri++) {
				x[ri][ci] = (x[ri][ci] - avg[ci]) / sd[ci];
			}
		}
	}

/*
	for(r=0;r<500;r++) {
		for(c=0;c<COLS2;c++) {
			printf("%.8f ",x[r][c]);
		}
		printf("\n");
	}
	exit(0);
*/

	for(ci=0;ci<COLS2;ci++)
		if(ci<65)
			use[ci]=1;
		else
			use[ci]=0;
	besta=11110;
	bestc=0;
	while(1) {
		#pragma omp parallel for
		for(tc=0;tc<COLS2;tc++) {
			int r,l2,cv,c;
			double maxa,d,pred,ll,lastsc,b[FOLDS],coef[FOLDS][COLS2];
			if(use[tc]==0) {
				for(cv=0;cv<FOLDS;cv++) {
					b[cv]=0;
					for(c=0;c<COLS2;c++) {
						coef[cv][c]=0;
					}
				}

				lastsc=99999;
				while(1) {
					ll = 0;
					for(cv=0;cv<FOLDS;cv++) {
						for(l2=0;l2<10;l2++) {
							for(r=0;r<ROWS;r++) {
								if(test[r] != cv) {
									pred=b[cv];
									for(c=0;c<COLS2;c++) {
										if(use[c] || c==tc) pred+=coef[cv][c] * x[r][c];
									}
									pred = 1/(1+exp(-pred));
									if(pred<0.001) pred=0.001;
									if(pred>0.999) pred=0.999;
									d = y[r]-pred;
									b[cv] += d*LR;
									for(c=0;c<COLS2;c++) {
										if(use[c] || c==tc) coef[cv][c] += d*x[r][c]*LR;
									}
								}
							}
						}
						for(r=0;r<ROWS;r++) {
							if(test[r] == cv) {
								pred=b[cv];
								for(c=0;c<COLS2;c++) {
									if(use[c] || c==tc) pred+=coef[cv][c] * x[r][c];
								}
								predt[r]=pred;
								pred = 1/(1+exp(-pred));
								if(pred<0.001) pred=0.001;
								if(pred>0.999) pred=0.999;
								ll += y[r] * log(pred) + (1-y[r])*log(1-pred);
							}
						}
					} // end cv
					maxa=-ll/ROWS;
					if(fabs(lastsc-maxa)<0.00001) break;
					lastsc=maxa;
				} //end while 1
				#pragma omp critical
				if(maxa<besta) {
					besta=maxa;
					bestc=tc;
				}
			} // if !use
		} //end for tc
		use[bestc]=1;
		printf("%d %f\n",bestc,besta);
		fflush(stdout);
	}

	return 0;
}

