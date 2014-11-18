#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <float.h>
#include "gam.h"

#define WINDOW 100

struct sort_pair {
	int i;
	double x;
};

int cmpp(const void *a, const void *b) {
	if((*(struct sort_pair *)a).x < (*(struct sort_pair *)b).x) {
		return -1;
	} else if((*(struct sort_pair *)a).x > (*(struct sort_pair *)b).x) {
		return 1;
	}
	return 0;
}

double calculate_alpha(double *y, int rows) {

double alpha;
int r;

	alpha = 0;
	for(r=0; r<rows; r++) {
		alpha += y[r];
	}
	alpha /= rows;

	return alpha;
}

void initialize_smoothX(double *smoothX, int rows, int cols) {

int r,c;

	for(r=0; r<rows; r++) {
		for(c=0; c<cols; c++) {
			smoothX[r*cols+c] = 0;
		}
	}
}

void get_partial_residuals(double *rsd, double *smoothX, double *y, int rows, int cols, double alpha, int k) {

int r,c;

	for(r=0; r<rows; r++) {
		rsd[r] = y[r] - alpha;
		for(c=0; c<cols; c++) {
			if(c != k) {
				rsd[r] -= smoothX[r*cols+c];
			}
		}
	}
}

double calculate_loss(double *y, double *smoothX, int rows, int cols, double alpha) {

int r,c;
double loss, pred;

	loss = 0;
	for(r=0; r<rows; r++) {
		pred = alpha;
		for(c=0; c<cols; c++) {
			pred += smoothX[r*cols+c];
		}
		loss += (y[r] - pred) * (y[r] - pred);
	}
	return sqrt(loss/rows);
}

void smooth_column(double *rsd, double *smoothX, int *sortedX, double *w, int rows, int cols, int c) {
	
int r;
double wtot,wsum,mean;
	
	mean = 0;
	wtot = 0;
	wsum = 0;
	for(r=0; r<WINDOW; r++) {
		wtot += rsd[sortedX[c*rows+r]] * w[sortedX[c*rows+r]];
		wsum += w[sortedX[c*rows+r]];
	}
	for(r=0; r<WINDOW/2; r++) {
		smoothX[sortedX[c*rows+r]*cols+c] = (wtot - rsd[sortedX[c*rows+r]]) / (wsum - w[sortedX[c*rows+r]]);
		mean += smoothX[sortedX[c*rows+r]*cols+c];
	}
	for(r=WINDOW/2; r<rows-WINDOW/2; r++) {
		smoothX[sortedX[c*rows+r]*cols+c] = (wtot - rsd[sortedX[c*rows+r]]) /  (wsum - w[sortedX[c*rows+r]]);
		mean += smoothX[sortedX[c*rows+r]*cols+c];
		wtot = wtot - rsd[sortedX[c*rows+(r-WINDOW/2)]] + rsd[sortedX[c*rows+(r+WINDOW/2)]];
		wsum = wsum - w[sortedX[c*rows+(r-WINDOW/2)]] + w[sortedX[c*rows+(r+WINDOW/2)]];
	}
	for(r=rows-WINDOW/2; r<rows; r++) {
		smoothX[sortedX[c*rows+r]*cols+c] = (wtot - rsd[sortedX[c*rows+r]]) / (wsum - w[sortedX[c*rows+r]]);
		mean += smoothX[sortedX[c*rows+r]*cols+c];
	}
	mean /= rows;
	for(r=0; r<rows; r++) {
		smoothX[sortedX[c*rows+r]*cols+c] -= mean;
	}
}

void get_sorted_indices(double *X, int *sortedX, int rows, int cols) {

int r,c;
struct sort_pair *sort_pairs;

	sort_pairs = (struct sort_pair *)malloc(rows * sizeof(struct sort_pair));
	for(c=0; c<cols; c++) {
		for(r=0; r<rows; r++) {
			sort_pairs[r].x = X[r*cols+c];
			sort_pairs[r].i = r;
		}
		qsort(sort_pairs, rows, sizeof(struct sort_pair), cmpp);
		for(r=0; r<rows; r++) {
			sortedX[c*rows+r] = sort_pairs[r].i;
		}
	}
	free(sort_pairs);
}

double inverse_link(double eta) {

double e;

	e = 1/(1+exp(-eta));
	if(e<0.000001) e=0.000001;
	if(e>0.999999) e=0.999999;
	return e;
}

#define MAX_LOG_PRED 15
double inv_link_function_d(double eta) {

double e;

	if(eta>MAX_LOG_PRED) eta = MAX_LOG_PRED;
	e=exp(eta);
	e = e/((1+e)*(1+e));
	if(e<DBL_EPSILON)
		return DBL_EPSILON;
	else
		return e;
}

void get_z(double *z, double *y, double *smoothX, int rows, int cols, double alpha) {

int r,c;
double lde,eta;

	for(r=0; r<rows; r++) {
		eta = alpha;
		for(c=0; c<cols; c++) {
			eta += smoothX[r*cols+c];
		}
		lde = inv_link_function_d(eta);
		z[r] = eta + (y[r] - inverse_link(eta)) / lde;
	}
}

double variance(double mu) {
	if(mu<0.000001) mu=0.000001;
	else if(mu>0.999999) mu=0.999999;
	return mu*(1-mu);
}

void get_weights(double *w, double *smoothX, int rows, int cols, double alpha) {

double eta,lde,mu;
int r,c;

	for(r=0; r<rows; r++) {
		eta = alpha;
		for(c=0; c<cols; c++) {
			eta += smoothX[r*cols+c];
		}
		lde = inv_link_function_d(eta);
		mu = inverse_link(eta);
		w[r] = 1/sqrt(lde*lde/variance(mu)); 
		//w[r] = 1/(lde*lde/variance(mu)); 
	}
}

void weight_smoothx(double *wsx, double *w, double *smoothX, int rows, int cols, int c) {

int r;

	for(r=0;r<rows;r++) {
		wsx[r] = w[r] * smoothX[r*cols+c];
	}
}

GAM *fit(double *X, double *y, int rows, int cols, double tol) {

double *rsd, loss, old_loss, *z, *w, *wsx;
int c;
GAM *model;
int t;

	fprintf(stderr,"Start fit.\n");
	model = (GAM *)malloc(sizeof(GAM));
	model->rows = rows;
	model->cols = cols;
	model->X = X;
	rsd = (double *)malloc(rows * sizeof(double));
	model->smoothX = (double *)malloc(rows * cols * sizeof(double));
	model->sortedX = (int *)malloc(rows * cols * sizeof(int));
	z = (double *)malloc(rows * sizeof(double));
	w = (double *)malloc(rows * sizeof(double));
	wsx = (double *)malloc(rows * sizeof(double));
	old_loss = 1e20;
	loss = 0;
	model->alpha = calculate_alpha(y, rows);


	model->alpha = log(model->alpha) - log(1-model->alpha);


	initialize_smoothX(model->smoothX, rows, cols);
	fprintf(stderr,"Start sort.\n");
	get_sorted_indices(X, model->sortedX, rows, cols);
	fprintf(stderr,"Start backfit.\n");
	while(fabs(old_loss-loss)/old_loss > tol) {
		get_z(z, y, model->smoothX, rows, cols, model->alpha);
		get_weights(w, model->smoothX, rows, cols, model->alpha);
		for(c=0; c<cols; c++) {
			get_partial_residuals(rsd, model->smoothX, z, rows, cols, model->alpha, c);
			smooth_column(rsd, model->smoothX, model->sortedX, w, rows, cols, c);
			//for(t=0;t<1000;t++) printf("%f %f\n",model->smoothX[t*cols+c],X[t*cols+c]);
			//exit(0);
		}
		old_loss = loss;
		loss = calculate_loss(y, model->smoothX, rows, cols, model->alpha);
		fprintf(stderr,"Loss %f -> %f\n", old_loss, loss);
	}
	fprintf(stderr,"Coverged\n");
	//for(t=0;t<1000;t++) printf("%f %f %f\n",y[t],z[t],w[t]);
	//exit(0);
	free(rsd);
	free(z);
	free(w);
	free(wsx);
	fprintf(stderr,"End fit.\n");
	return model;
}

void free_GAM(GAM *model) {
	free(model->sortedX);
	free(model->smoothX);
	free(model);
}

double smooth_predict(double x, GAM *model, int c) {

int first,last,middle;

	if(x <= model->X[model->sortedX[c*model->rows]*model->cols+c]) {
		return model->smoothX[model->sortedX[c*model->rows]*model->cols+c];
	}
	if(x >= model->X[model->sortedX[c*model->rows+model->rows-1]*model->cols+c]) {
		return model->smoothX[model->sortedX[c*model->rows+model->rows-1]*model->cols+c];
	}
	first = 0;
	last = model->rows - 1;
	middle = (first+last)/2;
 
	while(first <= last) {
		if(model->X[model->sortedX[c*model->rows+middle]*model->cols+c] < x) {
			first = middle + 1;    
		} else if(model->X[model->sortedX[c*model->rows+middle]*model->cols+c] == x) {
			return model->smoothX[model->sortedX[c*model->rows+middle]*model->cols+c];
		} else {
			last = middle - 1;
		}
		middle = (first + last)/2;
	}
	return model->smoothX[model->sortedX[c*model->rows+middle]*model->cols+c];
}

void predict(double *X, double *y, int rows, GAM *model) {	

int r,c;

	for(r=0; r<rows; r++) {
		y[r] = model->alpha;
		for(c=0; c<model->cols; c++) {
			y[r] += smooth_predict(X[r*model->cols+c], model, c);
		}
	}
}
