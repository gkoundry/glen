#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define WLR 0.15
#define PRED 0
#if PRED==0
#define FOLDS 5
#else
#define FOLDS 1
#endif
#define MAX_ITER 1
#define WSHRINK 1500
#define LR 0.0000005
#define RC 0.0000000
#define ROWS 250000
#define ROWST 550000
#define COLS 31
#define COLS2 71
//#define COLS2 42

double coef[FOLDS][COLS2];
char line[4096];
double x[ROWS][COLS2],test[ROWS];
double xt[ROWST][COLS2];
double y[ROWS],w[ROWS];
double srt[ROWS],predt[ROWS];
int id[ROWS],idt[ROWST],levels[ROWS],levels2[ROWS],levelst[ROWST],levelst2[ROWST];
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

double sc,bc,th,a,maxa,maxth;
int r;

	maxa=0;
	maxth=0;
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
			maxth=th;
		}
	}
	fprintf(stderr,"th%f ",maxth);
	return maxa;
}

int get_levelt(int r) {
	if(levelst2[r]>3.2) return 4;
	return levelst[r];
}

int get_level(int r) {
	if(levels2[r]>3.2) return 4;
	return levels[r];
}

double ams_d(double pred,double lpred,int r,int c) {

double ep,dda,squ,dsqu,s0,b0,si,bi,sbi10d,lsbid,sid,xi;
	//p = 1/(1+exp(-(a*x+b+y+c)))
	//sc = (2 *((s+b+10) * log(1+s/(b+10)) -s)) ^ 0.5
	//dsc/da = 2 * ( (s+b+10)' * log(1+s/(b+10)) + (s+b+10) * log(1+s/(b+10))' - s')

	s0 = 230;
	b0 = 4000;
	if(c==-1)
		xi=1;
	else
		xi = x[r][c];
	ep = exp(lpred);
	si = s0 + w[r] * pred * y[r];
	bi = b0 + w[r] * pred * (1-y[r]);
	squ = 2 *((si+bi+10) * log(1+si/(bi+10)) - si);
	sbi10d = xi * w[r] * y[r] * ep / ((ep+1)*(ep+1)); //d/da (g + w * y / (1+exp(-(a * m + b*n +c))) + h +w * (1-y)/ (1+exp(-(a * m + b*n +c))))
	lsbid = xi * w[r] * (s0 * (y[r]-1)+(b0+10)*y[r])*ep / (((s0+b0+w[r]+10)*ep+s0+b0+10)*((b0-w[r]*y[r]+w[r]+10)*ep+b0+10)); // d/da log(1+(g+w*y/(1+exp(-(a * m + b*n +c))))/(h+w*(1-y)/(1+exp(-(a * m + b*n +c)))+10))
	sid = xi * w[r] * y[r] * ep / ((ep+1)*(ep+1));
	dsqu = 2 * (sbi10d * log(1+si/(bi+10)) + (si+bi+10) * lsbid - sid);
	dda = 0.5 * 1/sqrt(squ) * dsqu;
	return dda;
}

int main() {

char *p,fname[256];
int l2,r,c,mc,cv,l,tot,LEVEL;
double lpred,lastsc,sd[COLS2],avg[COLS2],bc,sc,med[COLS2],pred,d,b[FOLDS],ll,llt;
FILE *fp,*out;

	for(r=0;r<ROWS;r++) {
#if PRED==1
		test[r] = 1;
#else
		test[r] = rand() % FOLDS;
#endif
	}

	fp=fopen("training.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		id[r]=atoi(p);
		r++;
	}
	fclose(fp);

	fp=fopen("training.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(c=0;c<COLS;c++) {
			x[r][c] = atof(p);
			if(c==23) levels[r]=atoi(p);
			if(c==8) levels2[r]=atof(p);
			p=strtok(NULL,","); 
		}
		x[r][COLS2-1]=x[r][1]*x[r][8];
		x[r][COLS2-2]=x[r][2]*x[r][8];
		x[r][COLS2-3]=x[r][11]*x[r][12];
		x[r][COLS2-4]=x[r][8]*x[r][14];
		x[r][COLS2-5]=x[r][2]*x[r][4];
		x[r][COLS2-6]=x[r][8]*x[r][12];
		w[r] = atof(p);
		p=strtok(NULL,","); 
		if(p[0]=='s' || p[0]=='1')
			y[r]=1;
		else
			y[r]=0;
		r+=1;
	}
	fclose(fp);
	if(r!=ROWS) {
		fprintf(stderr,"ERROR: incorrect rows %d vs %d\n",ROWS,r);
		exit(1);
	}

	fp=fopen("smooth_gaussian_10.000000_10.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(c=0;c<COLS;c++) {
			x[r][31+c] = atof(p);
			p=strtok(NULL,","); 
		}
		w[r] = atof(p);
		p=strtok(NULL,","); 
		if(p[0]=='s' || p[0]=='1')
			y[r]=1;
		else
			y[r]=0;
		r+=1;
	}
	fclose(fp);
	if(r!=ROWS) {
		fprintf(stderr,"ERROR: incorrect rows %d vs %d\n",ROWS,r);
		exit(1);
	}

	mc = 0;
	for(c=0;c<COLS;c++) {
		if(has_na[c]) {
			for(r=0;r<ROWS;r++) {
				srt[r] = x[r][c];
			}
			qsort(srt,ROWS,sizeof(double),cmpd);
			med[c] = srt[ROWS/2];
			for(r=0;r<ROWS;r++) {
				if(x[r][c] == -999) {
					x[r][c] = med[c];
					if(na_ind[c]) x[r][2*COLS+mc]=1;
				} else {
					if(na_ind[c]) x[r][2*COLS+mc]=0;
				}
			}
			if(na_ind[c]) mc++;
		}
	}

	for(c=0;c<COLS2;c++) {
		avg[c] = 0;
		for(r=0;r<ROWS;r++) {
			avg[c] += x[r][c];
		}
		avg[c] /= ROWS;
		sd[c] = 0;
		for(r=0;r<ROWS;r++) {
			sd[c] += (avg[c] - x[r][c]) * (avg[c] - x[r][c]);
		}
		sd[c] = sqrt(sd[c]/ROWS);
		if(sd[c]>0.00001) {
			for(r=0;r<ROWS;r++) {
				x[r][c] = (x[r][c] - avg[c]) / sd[c];
			}
		}
	}

	fp=fopen("test.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		idt[r]=atoi(p);
		for(c=0;c<COLS;c++) {
			xt[r][c] = atof(p);
			if(c==23) levelst[r]=atoi(p);
			if(c==8) levelst2[r]=atof(p);
			p=strtok(NULL,","); 
		}
		xt[r][COLS2-1]=xt[r][1]*xt[r][8];
		xt[r][COLS2-2]=xt[r][2]*xt[r][8];
		xt[r][COLS2-3]=xt[r][11]*xt[r][12];
		xt[r][COLS2-4]=xt[r][8]*xt[r][14];
		xt[r][COLS2-5]=xt[r][2]*xt[r][4];
		xt[r][COLS2-6]=xt[r][8]*xt[r][12];
		r++;
	}
	fclose(fp);

	fp=fopen("smootht_gaussian_10.000000_10.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(c=0;c<COLS;c++) {
			xt[r][31+c] = atof(p);
			p=strtok(NULL,","); 
		}
		r++;
	}
	fclose(fp);

	mc = 0;
	for(c=0;c<COLS;c++) {
		if(has_na[c]) {
			for(r=0;r<ROWST;r++) {
				if(xt[r][c] == -999) {
					xt[r][c] = med[c];
					if(na_ind[c]) xt[r][2*COLS+mc]=1;
				} else {
					if(na_ind[c]) xt[r][2*COLS+mc]=0;
				}
			}
			if(na_ind[c]) mc++;
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

	for(LEVEL=0;LEVEL<5;LEVEL++) {
	for(cv=0;cv<FOLDS;cv++) {
		b[cv]=0;
		for(c=0;c<COLS2;c++) {
			coef[cv][c]=0;
		}
	}

	lastsc=999;
	for(l=0;l<=MAX_ITER;l++) {
		sc = 0;
		ll = 0;
		llt = 0;
		tot = 0;
		bc = 0;
#if PRED==0
		sprintf(fname,"predlr1l%d.csv",LEVEL);
		out=fopen(fname,"w");
#endif
		for(cv=0;cv<FOLDS;cv++) {
		/*
			for(r=0;r<ROWS;r++) {
				x[r][2] = sx[cv][r][0]-0.25;
				x[r][COLS2-1] = 0;
				//x[r][COLS2-1] = sx[cv][r][0];
				//printf("%d %d %f\n",cv,r,x[r][2]);
			}
			*/
			for(l2=0;l2<30;l2++) {
				for(r=0;r<ROWS;r++) {
					if(get_level(r)==LEVEL && test[r] != cv) {
						lpred=b[cv];
						for(c=0;c<COLS2;c++) {
							//printf("%f %f",coef[cv][c],x[r][c]);
							lpred+=coef[cv][c] * x[r][c];
						}
						pred = 1/(1+exp(-lpred));
						if(pred<0.001) pred=0.001;
						if(pred>0.999) pred=0.999;
						d = ams_d(pred,lpred,r,-1); //y[r]-pred;
						b[cv] += d*LR;
						for(c=0;c<COLS2;c++) {
							//printf("%d %d %f %f %f %f %f\n",cv,r,d,x[r][c],coef[cv][c],y[r],pred);
							d = ams_d(pred,lpred,r,c); //y[r]-pred;
							//printf("%d %d %f %f %f %f\n",r,c,pred,y[r],x[r][c],d);
							coef[cv][c] += d*LR-fabs(RC*coef[cv][c]);
							//coef[cv][c] += ((w[r]-1)/WSHRINK+1)*d*x[r][c]*LR-fabs(RC*coef[cv][c]);
							//coef[cv][c] += (1+WLR*(1-y[r])*(pred>0.5)*w[r])*d*x[r][c]*LR-fabs(RC*coef[cv][c]);
							//coef[cv][c] += -((w[r]-1)/WSHRINK/60000)*x[r][c]+d*x[r][c]*LR-fabs(RC*coef[cv][c]);
						}
					}
				}
			}

			for(r=0;r<ROWS;r++) {
				if(get_level(r)==LEVEL && test[r] != cv) {
					pred=b[cv];
					for(c=0;c<COLS2;c++) {
						pred+=coef[cv][c] * x[r][c];
					}
					pred = 1/(1+exp(-pred));
					if(pred<0.001) pred=0.001;
					if(pred>0.999) pred=0.999;
					llt += y[r] * log(pred) + (1-y[r])*log(1-pred);
					//llt += (y[r]-pred)*(y[r]-pred);
					tot+=1;
				}
			}
#if PRED==0
			for(r=0;r<ROWS;r++) {
				if(get_level(r)==LEVEL && test[r] == cv) {
					pred=b[cv];
					for(c=0;c<COLS2;c++) {
						pred+=coef[cv][c] * x[r][c];
					}
					if(l==MAX_ITER) fprintf(out,"%d,%f\n",id[r],pred);
					predt[r]=pred;
					pred = 1/(1+exp(-pred));
					if(pred<0.001) pred=0.001;
					if(pred>0.999) pred=0.999;
					ll += y[r] * log(pred) + (1-y[r])*log(1-pred);
					//ll += (y[r]-pred)*(y[r]-pred);
				}
			}
#endif
/*
			printf("%f ",b[cv]);
			for(c=0;c<COLS2;c++) printf("%f ",coef[cv][c]);
			printf("\n");
			*/
		} // end cv
#if PRED==0
	fclose(out);
#endif
		fprintf(stderr,"%d %f %f %f %f %f %d\n",LEVEL,sc,bc,max_AMS(),-ll/ROWS,-llt/tot,tot);
		if(fabs(-llt/tot-lastsc)<0.0000005) break;
	}

#if PRED==1
/*
	for(r=0;r<100;r++) {
		if(get_levelt(r)==LEVEL) {
			pred=b[0];
			printf("r %3d c %10.7f",r,b[0]);
			for(c=0;c<COLS2;c++) {
				d = xt[r][c];
				if(sd[c]>0.00001) {
					d = (d-avg[c])/sd[c];
				}
				printf(" %10.7f * %10.7f ",d,coef[0][c]);
				pred+=d*coef[0][c];
			}
			printf("%6d,%f\n",idt[r],pred);
		}
		if(get_level(r)==LEVEL) {
			pred=b[0];
			printf("r %3d c %10.7f",r,b[0]);
			for(c=0;c<COLS2;c++) {
				d = x[r][c];
				printf(" %10.7f * %10.7f ",d,coef[0][c]);
				pred+=d*coef[0][c];
			}
			printf("%6d,%f\n",id[r],pred);
		}
	}
	exit(1);
	*/
	for(r=0;r<ROWST;r++) {
		if(get_levelt(r)==LEVEL) {
			pred=b[0];
			for(c=0;c<COLS2;c++) {
				d = xt[r][c];
				if(sd[c]>0.00001) {
					d = (d-avg[c])/sd[c];
				}
				pred+=d*coef[0][c];
			}
			printf("%d,%f\n",idt[r],pred);
		}
	}
#endif
	}
	return 0;
}

