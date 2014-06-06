#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define ROWS 250000
//#define COLS 32
#define COLS 3

double x[ROWS][COLS],y[ROWS],w[ROWS],predt[ROWS];
double coef[COLS];
char line[4096];

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
	for(th=0.4;th<0.9;th+=0.02) {
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

int c,r,ct,inc;
double tot,oldcoef,sc,bestsc;
char *p;
FILE *fp;

	fp=fopen("vote3.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(c=0;c<COLS;c++) {
			x[r][c] = atof(p);
			p=strtok(NULL,",");
		}
		y[r] = atof(p);
		p=strtok(NULL,",");
		w[r] = atof(p);
		r++;
	}
	fclose(fp);

	for(c=0;c<COLS;c++) {
		coef[c] = 1.0/COLS;
	}

	ct = 0;
	bestsc = 0;
	while(1) {
		for(inc=-1;inc<=1;inc+=2) {
			oldcoef = coef[ct];
			coef[ct] += inc * (rand()%1000)/5000.0;
			for(r=0;r<ROWS;r++) {
				predt[r] = 0;
				tot = 0;
				for(c=0;c<COLS;c++) {
					predt[r] += x[r][c] * coef[c];
					tot+=coef[c];
				}
				predt[r] /= tot;
			}
			sc = max_AMS();
				for(c=0;c<COLS;c++) {
					printf("%f ",coef[c]);
				}
				printf("%f\n",sc);
			if(sc>bestsc) {
				bestsc=sc;
				for(c=0;c<COLS;c++) {
					printf("%f ",coef[c]);
				}
				printf("%f\n",sc);
				fflush(stdout);
			} else {
				coef[ct] = oldcoef;
			}
		}
		ct = (ct + 1) % COLS;
	}

	return 0;
}
