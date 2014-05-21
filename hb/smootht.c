#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define KERNEL 0
#define STEP 10
#define WIDTH 10.0

#define GAUSSIAN 0
#define SQUARED 1
char *kernels[] = { "gaussian", "squared" };
#define ROWS 250000
#define ROWST 550000
#define COLS 31
#define max(a,b) (((a) > (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))

char line[4096];
double x[ROWS][COLS];
double xt[ROWST][COLS];
double y[ROWS],w[ROWS];
double sx[ROWST][COLS];


int main() {

char *p,fname[256];
int r,c;
FILE *fp,*out;

	fp=fopen("training.csv","r");
	p = fgets(line,4096,fp);
	sprintf(fname,"smootht_%s_%f_%d.csv",kernels[KERNEL],WIDTH,STEP);
	out=fopen(fname,"w");
	fprintf(out,"%s",p);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(c=0;c<COLS;c++) {
			x[r][c] = atof(p);
			p=strtok(NULL,","); 
		}
		w[r] = atof(p);
		p=strtok(NULL,","); 
		if(p[0]=='s')
			y[r]=1;
		else
			y[r]=0;
		r+=1;
	}
	fclose(fp);
	if(r!=ROWS) {
		fprintf(stderr,"ERROR: incorrect training rows %d vs %d\n",ROWS,r);
		exit(1);
	}

	fp=fopen("test.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		for(c=0;c<COLS;c++) {
			xt[r][c] = atof(p);
			p=strtok(NULL,","); 
		}
		r+=1;
	}
	fclose(fp);
	if(r!=ROWST) {
		fprintf(stderr,"ERROR: incorrect test rows %d vs %d\n",ROWST,r);
		exit(1);
	}

	#pragma omp parallel for
	for(c=0;c<COLS;c++) {
		double sd,avg,wsum,wtot,dst;
		int rows,r1,r2;
		avg = 0;
		rows = 0;
		for(r1=0;r1<ROWS;r1++) {
			if(x[r1][c]!=-999.0) {
				avg += x[r1][c];
				rows++;
			}
		}
		avg /= rows;
		sd = 0;
		rows = 0;
		for(r1=0;r1<ROWS;r1++) {
			if(x[r1][c]!=-999.0) {
				sd += (avg - x[r1][c]) * (avg - x[r1][c]);
				rows++;
			}
		}
		sd = sqrt(sd/rows);
		if(sd>0.00001) {
			for(r1=0;r1<ROWS;r1++) {
				if(x[r1][c]!=-999.0) {
					x[r1][c] = (x[r1][c] - avg) / sd;
				}
			}
			for(r1=0;r1<ROWST;r1++) {
				if(xt[r1][c]!=-999.0) {
					xt[r1][c] = (xt[r1][c] - avg) / sd;
				}
			}
		}
		for(r1=0;r1<ROWST;r1++) {
			wtot=0;
			wsum=0;
			if(xt[r1][c]==-999.0) {
				for(r2=0;r2<ROWS;r2+=STEP) {
					if(x[r2][c]==-999.0) {
						wsum += y[r2];
						wtot += 1;
					}
				}
			} else {
				if(KERNEL==SQUARED) {
					for(r2=0;r2<ROWS;r2+=STEP) {
						if(x[r2][c]!=-999.0) {
							dst = max(0.01,1-(WIDTH*(xt[r1][c] - x[r2][c])*(xt[r1][c] - x[r2][c])));
							wsum += dst * y[r2];
							wtot += dst;
						}
					}
				} else {
					for(r2=0;r2<ROWS;r2+=STEP) {
						if(x[r2][c]!=-999.0) {
							dst = 1/exp(min(15,WIDTH*(xt[r1][c] - x[r2][c])*(xt[r1][c] - x[r2][c])));
							wsum += dst * y[r2];
							wtot += dst;
						}
					}
				}
			}
			sx[r1][c]=wsum/wtot;
		}
	}

	for(r=0;r<ROWST;r++) {
		for(c=0;c<COLS;c++) {
			fprintf(out,"%f,",sx[r][c]);
		}
		fprintf(out,"\n");
	}
	fclose(out);

	return 0;
}

