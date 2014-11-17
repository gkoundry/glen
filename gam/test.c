#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "gam.h"

#define ROWS 1000
#define COLS 10

double X[ROWS][COLS], y[ROWS], pred[ROWS];
char line[4096];

int main() {

FILE *fp;
int r,c;
char *p;
GAM *model;

	fp=fopen("credit-train-1000.csv", "r");
	p = fgets(line,4096,fp);
	r = 0;
	while(fgets(line,4096,fp)) {
		p = strtok(line, ",");
		p = strtok(NULL, ",");
		y[r] = atof(p);
		for(c=0;c<COLS;c++) {
			p = strtok(NULL, ",");
			X[r][c] = atof(p);
		}
		r++;
	}
	fclose(fp);
	model = fit((double *)X, y, ROWS, COLS, 0.000000001);
	predict((double *)X, pred, ROWS, model);
	for(r=0;r<1000;r++) {
		printf("%f %f\n",pred[r],y[r]);
	}
	free_GAM(model);

	return 0;
}
