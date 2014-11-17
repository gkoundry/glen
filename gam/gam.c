#include <stdlib.h>
#include <stdio.h>
#include <math.h>
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

void smooth_column(double *rsd, double *smoothX, int *sortedX, int rows, int cols, int c) {
	
int r;
double wtot;
	
	wtot = 0;
	for(r=0; r<WINDOW; r++) {
		wtot += rsd[sortedX[c*rows+r]];
	}
	for(r=0; r<WINDOW/2; r++) {
		smoothX[r*cols+c] = (wtot - rsd[sortedX[c*rows+r]]) / (WINDOW - 1);
	}
	for(r=WINDOW/2; r<rows-WINDOW/2; r++) {
		smoothX[r*cols+c] = (wtot - rsd[sortedX[c*rows+r]]) /  WINDOW;
		wtot = wtot - rsd[sortedX[c*rows+(r-WINDOW/2)]] + rsd[sortedX[c*rows+(r+WINDOW/2)]];
	}
	for(r=rows-WINDOW/2; r<rows; r++) {
		smoothX[r*cols+c] = (wtot - rsd[sortedX[c*rows+r]]) / (WINDOW - 1);
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

GAM *fit(double *X, double *y, int rows, int cols, double tol) {

double *rsd, loss, old_loss;
int c;
GAM *model;

	fprintf(stderr,"Start fit.\n");
	model = (GAM *)malloc(sizeof(GAM));
	model->rows = rows;
	model->cols = cols;
	model->X = X;
	rsd = (double *)malloc(rows * sizeof(double));
	model->smoothX = (double *)malloc(rows * cols * sizeof(double));
	model->sortedX = (int *)malloc(rows * cols * sizeof(int));
	old_loss = 1e20;
	loss = 0;
	model->alpha = calculate_alpha(y, rows);
	initialize_smoothX(model->smoothX, rows, cols);
	fprintf(stderr,"Start sort.\n");
	get_sorted_indices(X, model->sortedX, rows, cols);
	fprintf(stderr,"Start backfit.\n");
	while(fabs(old_loss-loss)/old_loss > tol) {
		for(c=0; c<cols; c++) {
			get_partial_residuals(rsd, model->smoothX, y, rows, cols, model->alpha, c);
			smooth_column(rsd, model->smoothX, model->sortedX, rows, cols, c);
		}
		old_loss = loss;
		loss = calculate_loss(y, model->smoothX, rows, cols, model->alpha);
		fprintf(stderr,"Loss %f -> %f\n", old_loss, loss);
	}
	free(rsd);
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
		} else if(model->X[model->sortedX[c*model->rows+middle]*model->cols+c] < x) {
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
