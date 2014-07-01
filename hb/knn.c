#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

//0.600000 10 2.294989
// 0.4 10 2.309635
// 0.200000 10 1.557009
// 20.600000 10 2.181502
// 16.600000 10 2.190899
// 12.600000 10 2.151324
#define BW 0.6
#define WLR 0.00000001
#define SKIP 10
#define PRED 0
#if PRED==0
#define FOLDS 5
#else
#define FOLDS 1
#endif
#define ROWS 250000
#define ROWST 550000
#define COLS 30
#define max(a,b) (((a) > (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))

char line[4096];
double x[ROWS][COLS];
double y[ROWS],w[ROWS];
double srt[ROWS],predt[ROWS];
int id[ROWS],idt[ROWST];
//
// MERGE DUPS
// 
int has_na[] = {0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0};
//double vw[] = { 1, 1.0/2, 1.0/12, 1.0/24, 1.0/4, 1.0/18, 1.0/26, 1.0/7, 1.0/21, 1.0/23, 1.0/20, 1.0/8, 1.0/13, 1.0/3, 1.0/14, 1.0/19, 1.0/6, 1.0/30, 1.0/11, 1.0/15, 1.0/9, 1.0/25, 1.0/10, 1.0/17, 1.0/22, 1.0/16, 1.0/5, 1.0/27, 1.0/28, 1.0/29 };
//double vw[] = { 0.005951, 0.084907, 0.020543, 0.044761, 0.054405, 0.057627, 0.054350, 0.008256, 0.020697, 0.048799, 0.042935, 0.063494, 0.054389, 0.090395, 0.013918, 0.016381, 0.014197, 0.012101, 0.012743, 0.026189, 0.021765, 0.042568, 0.042445, 0.031599, 0.057671, 0.025285, 0.054884, 0.054397, 0.054376, 0.052764 };
double vw[] = { 0.750811, 1.166567, 0.777255, 1.198139, 1.187647, 1.263989, 1.186617, 0.669242, 0.869280, 1.123588, 0.988942, 1.158250, 1.187359, 1.393629, 0.673369, 0.738904, 0.876263, 0.665034, 0.735092, 1.078705, 0.738942, 0.966742, 0.924277, 0.865251, 1.168982, 0.943830, 1.186920, 1.187280, 1.187275, 1.143666 };


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
	for(th=0;th<1;th+=0.01) {
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
int r2,r,c,mc;
double sd[COLS],avg[COLS],bc,sc,med,pred,d,ed,td;
FILE *fp,*out;

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
		id[r]=atoi(p);
		for(c=0;c<COLS;c++) {
			p=strtok(NULL,","); 
			x[r][c] = atof(p);
		}
		p=strtok(NULL,","); 
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
	out=fopen("predcknn.csv","w");
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
					//x[r][2*COLS+mc]=1;
				} else {
					//x[r][2*COLS+mc]=0;
				}
			}
			mc++;
		}
	}

	for(c=0;c<COLS;c++) {
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

	for(c=0;c<COLS;c++) {
		vw[c] = (vw[c]-1)*2+1;
	}
	sc=0;
	bc=0;
	for(r=0;r<ROWS;r++) {
		pred=0;
		for(c=0;c<COLS;c++) {
			pred += vw[c];
		}
		/*
		for(c=0;c<COLS;c++) {
			vw[c] /= pred/30;
		}
		*/
		pred = 0;
		td = 0;
		for(r2=0;r2<ROWS;r2+=SKIP) if(r!=r2) {
			ed = 0;
			for(c=0;c<COLS;c++) 
				ed += vw[c]*(x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]);
				//ed += (x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]);
			d = 1/exp(min(18,ed*BW));
			//printf("%d %f\n",r,d);
			if(d>0) {
				pred += d*y[r2];
				td += d;
				/*
				if(y[r]==y[r2]) {
					for(c=0;c<COLS;c++) {
						vw[c] += WLR * 1/(1+(x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]));
					}
				} else {
					for(c=0;c<COLS;c++) {
						vw[c] -= WLR * 1/(1+(x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]));
					}
				}
				*/
			}
		}
		pred /= td;
		predt[r] = pred;
		if(pred>0.5) {
			if(y[r]) {
				sc+=w[r];
			} else {
				bc+=w[r];
			}
		}
		fprintf(out,"%d,%f\n",id[r],pred);
		//if(r>5) break;
	}
	printf("%f %d %f\n",BW,SKIP,max_AMS());
	for(c=0;c<COLS;c++) {
		printf("%d %f\n",c,vw[c]);
	}

	return 0;
}

