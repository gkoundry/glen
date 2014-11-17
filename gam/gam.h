typedef struct {
	double alpha;
	double *X;
	double *smoothX;
	int *sortedX;
	int rows;
	int cols;
} GAM;

GAM *fit(double *X, double *y, int rows, int cols, double tol);
void predict(double *X, double *y, int rows, GAM *model);
void free_GAM(GAM *model);
