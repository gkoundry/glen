#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define ROWS 250000

#define max(a,b) (((a) > (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))

char line[4096];
double x[ROWS][64],y[ROWS],wt[ROWS],pred[ROWS];
int rows[ROWS];
double coef[64],test_coef[64];

int cmpr(const void *a,const void *b) {
	//return (int)(pred[*((int *)a)]-pred[*((int *)b)]);
	if(pred[*((int *)a)]>pred[*((int *)b)])
		return 1;
	else if(pred[*((int *)a)]>pred[*((int *)b)])
		return -1;
	else
		return 0;
}

double AMS(double s, double b) {
	double br,radicand;

    br = 10.0;
    //radicand = 2 *( (s+b+br) * log (1.0 + s/(b+br)) -s);
    //return sqrt(radicand);
    radicand = ( (s+b+br) * log (1.0 + s/(b+br)) -s);
    return radicand;
}

int main() {

FILE *fp;
int r,c,cols,ri,bestr,l;
double ams,bestams,bestams2,sc,bc;
char *p;

	fp=fopen("merge1.csv","r");
	p = fgets(line,4096,fp);
	r=0;
	cols=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,","); 
		y[r] = atof(p);
		p=strtok(NULL,","); 
		wt[r] = atof(p);
		cols=0;
		while((p=strtok(NULL,","))) {
			x[r][cols] = atof(p);
			cols+=1;
		}
		r++;
	}
	fclose(fp);

	for(c=0;c<cols;c++) {
		coef[c]=0;
	}
	bestams2=0;
	l=0;
	while(1) {
		for(c=0;c<cols;c++) {
			if(l%2==1)
				test_coef[c] = coef[c] + (rand()%20000 - 10000)*max(0.00007,(fabs(coef[c])/5000));
			else
				test_coef[c] = coef[c] + (rand()%20000 - 10000)*max(0.00001,(fabs(coef[c])/50000));
		}
		l++;
		for(r=0;r<ROWS;r++) {
			pred[r] = 0;
			for(c=0;c<cols;c++) {
				pred[r] += x[r][c] * test_coef[c];
			}
			rows[r]=r;
		}
		qsort(rows,ROWS,sizeof(int),cmpr);
		for(r=0;r<ROWS;r++) {
			ri = rows[r];
		}
		sc=0;
		bc=0;
		bestams=0;
		bestr=0;
		//for(r=ROWS-1;r>=0;r--) {
		for(r=ROWS-1;r>=200000;r--) {
			ri = rows[r];
			if(y[ri])
				sc+=wt[ri];
			else
				bc+=wt[ri];
			ams = AMS(sc,bc);
			if(ams>bestams) {
				bestr=r;
				bestams=ams;
			}
		}
		/*
		printf("%f",sqrt(2*bestams));
		for(c=0;c<cols;c++) {
			printf(" %f",test_coef[c]);
		}
		*/
		if(bestams > bestams2) {
			printf("%d %f",bestr,sqrt(2*bestams));
			bestams2 = bestams;
			for(c=0;c<cols;c++) {
				printf(" %f",test_coef[c]);
				coef[c] = test_coef[c];
			}
			printf("\n");
			//printf(" ===");
			fflush(stdout);
		}
		//printf("\n");
		r=0;
		for(c=0;c<cols;c++) 
			if(fabs(coef[c])>7) r=1;
		if(r) 
			for(c=0;c<cols;c++) 
				coef[c] /= 7;
	}
		
	return 0;
}
