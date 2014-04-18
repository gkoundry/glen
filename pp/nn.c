#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define ANS 2150000
#define ROWS 379790
char line[4096];
double scores[ANS];
int hist[ROWS][20];
int quotes[ROWS];
int ans[ROWS];
int ids[ROWS];

double dist(int r,int r2) {
	
int i,j;
double d = 0;

	for(i=0;i<quotes[r];i++) {
		for(j=0;j<quotes[r2];j++) {
			if(hist[r][i]==hist[r2][j]) {
				d += (i+1) * (fabs(i-j)+1);
				break;
			}
			if(j+1==quotes[r2]) {
				d += (i+1)*30;
			}
		}
	}
	return d/quotes[r];
}

void reset_scores() {

int r;

	for(r=0;r<ANS;r++) {
		scores[r]=0;
	}
}

void score(int r,double sc) {
	scores[ans[r]] += sc;
}

int get_best_score() {

double best = -1;
int bestr,r;

	bestr=0;
	for(r=0;r<ANS;r++) {
		if(scores[r]>best) {
			best = scores[r];
			bestr = r;
		}
	}
	return bestr;
}

int check_pred(int r,int p) {
	if(ans[r]==p)
		return 1;
	else
		return 0;
}

int temp[15];

int main() {

FILE *fp;
int i,cnt,h,rt,r,r2,y,id,best;
double sc,d,bnch;
char *p;

	fp=fopen("trains3na.csv","r");
	p = fgets(line,4096,fp);
	h=0;
	r=0;
	while(fgets(line,4096,fp)) {
		p=strtok(line,",");
		id=atoi(p);
		p=strtok(NULL,",");
		p=strtok(NULL,",");
		rt=atoi(p);
		for(i=0;i<14;i++) p=strtok(NULL,",");
		y = atoi(strtok(NULL,","))*1000000+
			atoi(strtok(NULL,","))*100000+
			atoi(strtok(NULL,","))*10000+
			atoi(strtok(NULL,","))*1000+
			atoi(strtok(NULL,","))*100+
			atoi(strtok(NULL,","))*10+
			atoi(strtok(NULL,","))*1;
		if(y>9999999) {
			printf("id %d y %d\n",id,y);
			exit(0);
		}
		if(rt==1) {
			quotes[r] = h;
			ids[r] = id;
			for(i=0;i<h;i++)
				hist[r][i] = temp[h-i-1];
			ans[r] = y;
			h=0;
			r++;
		} else {
			temp[h] = y;
			h++;
		}

	}
	fclose(fp);

	sc=0;
	bnch=0;
	cnt=0;
	for(r=0;r<ROWS;r++) {
		//printf("%d\n",r);
		if(rand()%1000<10) {
			reset_scores();
			for(r2=0;r2<ROWS;r2++) {
				if(r2!=r && ids[r]%100000000!=ids[r2]%100000000) {
					d = dist(r,r2);
					if(ids[r]==10003999)
						printf("%d %d %f\n",ids[r],ids[r2],d);
					score(r2,1/d);
				}
			}
//1 10003999 2011031 1133123
			if(ids[r]==10003999)
				exit(0);
			best = get_best_score();
			if(ans[r]==hist[r][0])
				bnch++;
			if(check_pred(r,best))
				sc++;
			cnt++;
			printf("%d %d %d %d\n",hist[r][0]!=best,ids[r],hist[r][0],best);
		}
	}
	printf("%f %f\n",sc/cnt,bnch/cnt);
		
	return 0;
}
