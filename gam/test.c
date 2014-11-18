#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "gam.h"

#define ROWS 1000
#define ROWSP 15000
#define COLS 10

double X[ROWS][COLS], y[ROWS], pred[ROWS];
double Xv[ROWSP][COLS], yv[ROWSP], predv[ROWSP];
char line[4096];

int main() {

FILE *fp;
int r,c;
char *p;
double sc,scm,tmean;
GAM *model;

	fp=fopen("credit-train-1000.csv", "r");
	p = fgets(line,4096,fp);
	r = 0;
	tmean = 0;
	while(fgets(line,4096,fp)) {
		p = strtok(line, ",");
		p = strtok(NULL, ",");
		y[r] = atof(p);
		tmean += y[r];
		for(c=0;c<COLS;c++) {
			p = strtok(NULL, ",");
			X[r][c] = atof(p);
		}
		r++;
	}
	tmean /= ROWS;
	fclose(fp);
	fp=fopen("credit-train-small.csv", "r");
	p = fgets(line,4096,fp);
	r = 0;
	while(fgets(line,4096,fp)) {
		p = strtok(line, ",");
		p = strtok(NULL, ",");
		yv[r] = atof(p);
		for(c=0;c<COLS;c++) {
			p = strtok(NULL, ",");
			Xv[r][c] = atof(p);
		}
		r++;
	}
	fclose(fp);
	model = fit((double *)X, y, ROWS, COLS, 0.000000001);
	predict((double *)Xv, predv, ROWSP, model);
	sc = 0;
	scm = 0;
	for(r=0;r<ROWSP;r++) {
		predv[r] = 1/(1+exp(-predv[r]));
		printf("%f %f\n",predv[r],yv[r]);
		sc -= yv[r] * log(predv[r]) + (1-yv[r])*log(1-predv[r]);
		scm -= yv[r] * log(tmean) + (1-yv[r])*log(1-tmean);
	}
	printf("%f %f\n",sc/ROWSP,scm/ROWSP);
	free_GAM(model);

	return 0;
}
