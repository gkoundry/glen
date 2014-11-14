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
#define BW 4.8
#define CREDK 0.1
#define VSCALE 0.77 
#define WLR 0.0000000001 // 0.00001
#define SKIP 1
#define PRED 0
#define MAXROWS 100000
#define MAXROWST 221000
#define max(a,b) (((a) > (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))
#define MAXCOLS 31

char line[4096];
double x[MAXROWS][MAXCOLS];
double xt[MAXROWST][MAXCOLS];
double y[MAXROWS],w[MAXROWS];
#if PRED==0
double srt[MAXROWS],predt[MAXROWS];
#else
double srt[MAXROWST],predt[MAXROWST];
#endif
int id[MAXROWS],idt[MAXROWST];
int COLS[3] = { 19,23,31 };
int ROWS[3] = { 99913,77544,72543 };
int ROWST[3] = { 220156, 169716, 160128 };

//
// MERGE DUPS
// 
int has_na[] = {0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0};
//double vw[] = { 1, 1.0/2, 1.0/12, 1.0/24, 1.0/4, 1.0/18, 1.0/26, 1.0/7, 1.0/21, 1.0/23, 1.0/20, 1.0/8, 1.0/13, 1.0/3, 1.0/14, 1.0/19, 1.0/6, 1.0/30, 1.0/11, 1.0/15, 1.0/9, 1.0/25, 1.0/10, 1.0/17, 1.0/22, 1.0/16, 1.0/5, 1.0/27, 1.0/28, 1.0/29 };
//double vw[] = { 0.005951, 0.084907, 0.020543, 0.044761, 0.054405, 0.057627, 0.054350, 0.008256, 0.020697, 0.048799, 0.042935, 0.063494, 0.054389, 0.090395, 0.013918, 0.016381, 0.014197, 0.012101, 0.012743, 0.026189, 0.021765, 0.042568, 0.042445, 0.031599, 0.057671, 0.025285, 0.054884, 0.054397, 0.054376, 0.052764 };
double vw[] = { 0.750811, 1.166567, 0.777255, 1.198139, 1.187647, 1.263989, 1.186617, 0.669242, 0.869280, 1.123588, 0.988942, 1.158250, 1.187359, 1.393629, 0.673369, 0.738904, 0.876263, 0.665034, 0.735092, 1.078705, 0.738942, 0.966742, 0.924277, 0.865251, 1.168982, 0.943830, 1.186920, 1.187280, 1.187275, 1.143666 };
double vwt[3][MAXCOLS] = {
 { 0.452123, 0.431454, 0.436998, 0.443771, 0.402818, 0.443771, 0.449823, 0.411521, 0.515281, 0.477002, 0.379220, 0.381187, 0.425300, 0.377659, 0.381087, 0.436981, 0.381294, 0.401916, 0.459904 },
 { 0.263547, 0.231607, 0.258287, 0.260499, 0.219829, 0.238407, 0.262660, 0.241301, 0.228382, 0.264583, 0.215489, 0.216070, 0.249459, 0.215050, 0.216108, 0.247134, 0.216071, 0.238454, 0.270734, 0.221553, 0.216112, 0.270734, 0.310927 },
 { 0.227428, 0.193795, 0.217561, 0.192049, 0.186118, 0.215360, 0.193500, 0.176061, 0.197798, 0.196622, 0.201372, 0.194048, 0.186564, 0.211415, 0.174100, 0.173467, 0.204444, 0.173977, 0.173465, 0.197473, 0.173461, 0.190891, 0.206940, 0.200023, 0.176600, 0.173521, 0.208472, 0.176656, 0.173492, 0.197978, 0.268396 }
};

int cmpd(const void *a,const void *b) {
	return (int)(*((double *)a)-*((double *)b));
}
double AMS(double s, double b) {
	double br,radicand;

    br = 10.0;
    radicand = 2 *( (s+b+br) * log (1.0 + s/(b+br)) -s);
    return sqrt(radicand);
}


double max_AMS(int ft) {

double sc,bc,th,a,maxa; //,maxth;
int r;

	maxa=0;
	for(th=0;th<1;th+=0.01) {
		sc=0;
		bc=0;
		for(r=0;r<ROWS[ft];r++) {
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

char *p,fname[256];
int r2,r,c,ft;
double cred,minv,sd[MAXCOLS],avg[MAXCOLS],pred,d,ed,td,vt,va,vs,ym;
FILE *fp,*out;

	for(ft=0;ft<3;ft++) {
	#if PRED==1
		sprintf(fname,"test%d.csv",ft);
		fp=fopen(fname,"r");
		p = fgets(line,4096,fp);
		r=0;
		while(fgets(line,4096,fp)) {
			p=strtok(line,","); 
			idt[r]=atoi(p);
			for(c=0;c<COLS[ft]-1;c++) {
				p=strtok(NULL,","); 
				xt[r][c] = atof(p);
			}
			p=strtok(NULL,","); 
			xt[r][COLS[ft]-1] = atof(p);
			r++;
		}
		fclose(fp);
	#endif

		sprintf(fname,"training%d.csv",ft);
		fp=fopen(fname,"r");
		p = fgets(line,4096,fp);
		r=0;
		ym=0;
		while(fgets(line,4096,fp)) {
			p=strtok(line,","); 
			id[r]=atoi(p);
			for(c=0;c<COLS[ft]-1;c++) {
				p=strtok(NULL,","); 
				x[r][c] = atof(p);
			}
			p=strtok(NULL,","); 
			w[r] = (atof(p)+8)/8;
			p=strtok(NULL,","); 
			if(p[0]=='s')
				y[r]=1;
			else if(p[0]=='b')
				y[r]=0;
			else
				fprintf(stderr,"Invalid target\n");
			ym+=y[r];
			p=strtok(NULL,","); 
			x[r][COLS[ft]-1] = atof(p);
			r+=1;
		}
		fclose(fp);
		if(r!=ROWS[ft]) {
			fprintf(stderr,"ERROR: incorrect rows %d vs %d\n",ROWS[ft],r);
			exit(1);
		}
		ym/=r;

	#if PRED==0
		sprintf(fname,"train_cknn_t%d_bw%f_vs%f.csv",ft,BW,VSCALE);
	#else
		sprintf(fname,"test_cknn_t%d_bw%f_vs%f.csv",ft,BW,VSCALE);
	#endif
		out=fopen(fname,"w");
	/*
		mc = 0;
		for(c=0;c<COLS[ft];c++) {
			if(has_na[c]) {
				for(r=0;r<ROWS[ft];r++) {
					srt[r] = x[r][c];
				}
				qsort(srt,ROWS[ft],sizeof(double),cmpd);
				med = srt[ROWS[ft]/2];
				for(r=0;r<ROWS[ft];r++) {
					if(x[r][c] == -999) {
						x[r][c] = med;
						//x[r][2*COLS[ft]+mc]=1;
					} else {
						//x[r][2*COLS[ft]+mc]=0;
					}
				}
				mc++;
			}
		}
		*/

		for(c=0;c<COLS[ft];c++) {
			avg[c] = 0;
			for(r=0;r<ROWS[ft];r++) {
				avg[c] += x[r][c];
			}
			avg[c] /= ROWS[ft];
			sd[c] = 0;
			for(r=0;r<ROWS[ft];r++) {
				sd[c] += (avg[c] - x[r][c]) * (avg[c] - x[r][c]);
			}
			sd[c] = sqrt(sd[c]/ROWS[ft]);
			if(sd[c]>0.00001) {
				for(r=0;r<ROWS[ft];r++) {
					x[r][c] = (x[r][c] - avg[c]) / sd[c];
				}
				for(r=0;r<ROWST[ft];r++) {
					xt[r][c] = (xt[r][c] - avg[c]) / sd[c];
				}
			}
		}

#if PRED==0
/*
		for(c=0;c<COLS[ft];c++) {
			vw[c] = 1.0/COLS[ft];
		}
		*/
		va=0;
		for(c=0;c<COLS[ft];c++) {
			vw[c] = vwt[ft][c];
			va += vw[c];
		}
		va /= COLS[ft];
		vs=0;
		for(c=0;c<COLS[ft];c++) {
			vs+=(vw[c]-va)*(vw[c]-va);
		}
		vs = sqrt(vs/COLS[ft]);
		minv=99999;
		for(c=0;c<COLS[ft];c++) {
			vw[c] = (vw[c]-va)/vs;
			if(vw[c]<minv) minv=vw[c];
		}
		for(c=0;c<COLS[ft];c++) {
			vw[c] = 1 + vw[c] * VSCALE;
			//vw[c] = vw[c]*2 - 2*minv;
		}

		for(r=0;r<ROWS[ft];r++) {
#else
		for(c=0;c<COLS[ft];c++) {
			vw[c] = vwt[ft][c];
		}
		for(r=0;r<ROWST[ft];r++) {
#endif
			pred = 0;
			td = 0;
			for(r2=0;r2<ROWS[ft];r2+=SKIP) if(r!=r2 || PRED) {
				ed = 0;
				for(c=0;c<COLS[ft];c++) 
#if PRED==0
					ed += vw[c]*(x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]);
#else
					ed += vw[c]*(xt[r][c]-x[r2][c])*(xt[r][c]-x[r2][c]);
#endif
					//ed += (x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]);
				d = 1/exp(min(18,sqrt(ed)*BW));
				if(d>0) {
					pred += d*y[r2];
					td += d;
#if PRED==3
					if(y[r]==y[r2]) {
						//vt=0;
						for(c=0;c<COLS[ft];c++) {
							vw[c] += WLR * 1/(1+(x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]));
							//vt+=vw[c];
						}
						/*
						for(c=0;c<COLS[ft];c++) {
							vw[c] /= vt;
			//				printf("%f ",vw[c]);
						}
			//			printf("\n");
			*/
			/*
					} else {
						for(c=0;c<COLS[ft];c++) {
							vw[c] -= WLR * 1/(1+(x[r][c]-x[r2][c])*(x[r][c]-x[r2][c]));
						}
					*/
					}
#endif
				}
			}
			pred /= td;
			/*
			cred = td/(CREDK+td);
			predt[r] = cred * pred + (1-cred) * ym;
			*/
			predt[r] = pred;
#if PRED==0
			fprintf(out,"%d,%f\n",id[r],predt[r]);
#else
			fprintf(out,"%d,%f\n",idt[r],predt[r]);
#endif
			//if(r>5) break;
		}
		fclose(fp);
#if PRED==0
		printf("%f %d %f\n",BW,SKIP,max_AMS(ft));
		for(c=0;c<COLS[ft];c++) {
			printf("%d %f\n",c,vw[c]);
		}
#endif
	}

	return 0;
}

