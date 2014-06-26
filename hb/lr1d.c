#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PRED 0
#if PRED==0
#define FOLDS 5
#else
#define FOLDS 1
#endif
#define MAX_ITER 5
#define WSHRINK 15
#define LR 0.0000005
#define RC 0.0000000
#define ROWS 250000
#define ROWST 550000
#define COLS 31
#define COLS2 73
#define max(a,b) (((a) > (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))
//#define COLS2 42
/*
p = (1/(1+exp(-(a*m + b*n +c))))
s = q + y * w * p
b = r + (1-y) * w * p
d = s/sqrt(b)
d = (q+y*w*p)/sqrt(r+(1-y)*w*p)
d = d/da ((q+y*w*(1/(1+exp(-(a*m + b*n +c)))))/sqrt(r+(1-y)*w*(1/(1+exp(-(a*m + b*n +c))))))
ep = exp(pred);
d = x * y[r] * sqrt(-w[r]*(y[r]-1)*ep/(ep+1)) / (2 * (y[r]-1) * (ep+1));
d = w[r] * ep * (y[r]*(w[r]*(y[r]-1)*ep-2*b0*(ep+1))-s0*(y[r]-1)*(ep+1)) / (2*(ep+1)*(ep+1)*sqrt(w[r]*(1-y[r])/(epn+1)+b0)*(b0*(ep+1)-w[r]*(y[r]-1)*ep));
*/

double coef[FOLDS][COLS2];
char line[4096];
double x[ROWS][COLS2],test[ROWS];
double y[ROWS],w[ROWS];
double srt[ROWS],predt[ROWS];
int id[ROWS],idt[ROWST];
int has_na[] = {0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0};

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

double minp,maxp,sc,bc,th,a,maxa; //,maxth;
int r;

	minp=9e29;
	maxp=-9e20;
	for(r=0;r<ROWS;r++) {
		if(predt[r]<minp) minp=predt[r];
		if(predt[r]>maxp) maxp=predt[r];
	}
	maxa=0;
	for(th=minp;th<maxp;th+=(maxp-minp)/50) {
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
int l2,r,c,mc,cv,l,tot;
double b0,s0,ep,epn,sd[COLS2],avg[COLS2],bc,sc,med,pred,d,b[FOLDS],ll,llt;
FILE *fp,*out;

	b0=4000;
	s0=230;
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
#if PRED==1
	fp=fopen("test.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		idt[r]=atoi(p);
		r++;
	}
	fclose(fp);
#endif

	fp=fopen("training.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(c=0;c<COLS;c++) {
			x[r][c] = atof(p);
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

#if PRED==0
	out=fopen("predlr1d.csv","w");
#endif
	mc = 0;
	for(c=0;c<COLS;c++) {
		if(has_na[c]) {
			for(r=0;r<ROWS;r++) {
				srt[r] = x[r][c];
			}
			qsort(srt,ROWS,sizeof(double),cmpd);
			med = srt[ROWS/2];
			for(r=0;r<ROWS;r++) {
				if(x[r][c] == -999) {
					x[r][c] = med;
					x[r][2*COLS+mc]=1;
				} else {
					x[r][2*COLS+mc]=0;
				}
			}
			mc++;
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

/*
	for(r=0;r<500;r++) {
		for(c=0;c<COLS2;c++) {
			printf("%.8f ",x[r][c]);
		}
		printf("\n");
	}
	exit(0);
*/

	for(cv=0;cv<FOLDS;cv++) {
		b[cv]=0;
		for(c=0;c<COLS2;c++) {
			coef[cv][c]=0;
		}
	}

	for(l=0;l<=MAX_ITER;l++) {
		sc = 0;
		ll = 0;
		llt = 0;
		tot = 0;
		bc = 0;
		for(cv=0;cv<FOLDS;cv++) {
		/*
			for(r=0;r<ROWS;r++) {
				x[r][2] = sx[cv][r][0]-0.25;
				x[r][COLS2-1] = 0;
				//x[r][COLS2-1] = sx[cv][r][0];
				//printf("%d %d %f\n",cv,r,x[r][2]);
			}
			*/
			for(l2=0;l2<55;l2++) {
				for(r=0;r<ROWS;r++) {
					if(test[r] != cv) {
						pred=b[cv];
						for(c=0;c<COLS2;c++) {
							//printf("%f %f",coef[cv][c],x[r][c]);
							pred+=coef[cv][c] * x[r][c];
						}
						//d = -w[r]*(y[r]*(2*4000-w[r]*(y[r]-1)*pred)+230*(y[r]-1))/(2*pow(4000-w[r]*(y[r]-1)*pred,1.5));
						ep = exp(pred);
						epn = exp(-pred);
						//d = y[r] * sqrt(-w[r]*(y[r]-1)*ep/(ep+1)) / (2 * (y[r]-1) * (ep+1));
						d = -w[r] * ep * (y[r]*(w[r]*(y[r]-1)*ep-2*b0*(ep+1))-s0*(y[r]-1)*(ep+1)) / (2*(ep+1)*(ep+1)*sqrt(w[r]*(1-y[r])/(epn+1)+b0)*(b0*(ep+1)-w[r]*(y[r]-1)*ep));
						b[cv] += d*LR;
						for(c=0;c<COLS2;c++) {
							//printf("%d %d %f %f %f %f %f\n",cv,r,d,x[r][c],coef[cv][c],y[r],pred);
							coef[cv][c] += d*x[r][c]*LR;
							//coef[cv][c] += ((w[r]-1)/WSHRINK+1)*d*x[r][c]*LR-fabs(RC*coef[cv][c]);
							//coef[cv][c] += -((w[r]-1)/WSHRINK/60000)*x[r][c]+d*x[r][c]*LR-fabs(RC*coef[cv][c]);
						}
					}
				}
			}
			printf("%f",b[cv]);
			for(c=0;c<COLS2;c++) {
				printf(" %f",coef[cv][c]);
			}
			printf("\n");
			fflush(stdout);
			for(r=0;r<ROWS;r++) {
				if(test[r] != cv) {
					pred=b[cv];
					for(c=0;c<COLS2;c++) {
						pred+=coef[cv][c] * x[r][c];
					}
					pred=1/(1+exp(-pred));
					pred=min(0.9999,max(0.0001,pred));
					//if(l==5) printf("%d,%f\n",id[r],pred);
					llt += y[r]*log(pred)+(1-y[r])*log(1-pred);
					tot+=1;
				}
			}
			//if(l==5) exit(0);
#if PRED==0
			for(r=0;r<ROWS;r++) {
				if(test[r] == cv) {
					pred=b[cv];
					for(c=0;c<COLS2;c++) {
						pred+=coef[cv][c] * x[r][c];
					}
					if(l==MAX_ITER) fprintf(out,"%d,%f\n",id[r],pred);
					pred=1/(1+exp(-pred));
					pred=min(0.9999,max(0.0001,pred));
					predt[r]=pred;
					ll += y[r]*log(pred)+(1-y[r])*log(1-pred);
				}
			}
#endif
		} // end cv
		fprintf(stderr,"%f %f %f %f %f %f\n",LR,sc,bc,max_AMS(),-ll/ROWS,-llt/tot);
	}
#if PRED==0
	fclose(out);
#endif

#if PRED==1
	fp=fopen("smootht_gaussian_10.000000_10.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		pred=b[0];
		for(c=0;c<COLS;c++) {
			d = atof(p);
			if(sd[c]>0.00001) {
				d = (d-avg[c])/sd[c];
			}
			pred+=d*coef[0][c];
			p=strtok(NULL,","); 
		}
		printf("%d,%f\n",idt[r],pred);
		r++;
	}
	fclose(fp);
#endif
	return 0;
}

