///////////////////////////
// Matrix Multiplication //
///////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct matrix {
  int		r;	// rows
  int		c;	// columns
  float		*d;	// data
} matrix;

float randfloat(float min, float max)
{
  int	irandom; 
  float	frandom;

  irandom = rand();
  frandom = min + ((float) irandom / RAND_MAX) * (max - min);
  return frandom;

} // randfloat

void matin(matrix *m)
{
  int	i, j, r, c;

  //  r = m->r;
  //  c = m->c;
  //  for (int i = 0; i<r; i++) {
  //    for (int j = 0; j<c; j++) {
  //      printf("%d, %d : ", i, j);
  //      scanf("%d", m->d[i*c + j]);
  //    }
  //  }

  r = m->r;
  c = m->c;
  for (int i = 0; i<r; i++) {
    for (int j = 0; j<c; j++) {
      m->d[i*c + j] = randfloat(1.0, 100.0);
    }
  }

} // matin

void matout(matrix *a)
{
  int	i, j, r, c;

  r = a->r;
  c = a->c;
  for (int i = 0; i<r; i++) {
    for (int j = 0; j<c; j++) {
      printf("%3f ", a->d[i*c + j]);
    }
    printf("\n");
  }

} // matout

void matmul(matrix *a, matrix *b, matrix *c)
{
  int	i, j, k, ar, ac, cc;
  float	*am, *bm, *cm;

  ar = a->r;
  ac = a->c;
  cc = c->c;
  am = a->d;
  bm = b->d;
  cm = c->d;
  // Version 1: loop order (i j k)
  for (i=0; i<ar; i++) {
    for (j=0; j<cc; j++) {
      cm[i*cc + j] = 0;
      for (k=0; k<ac; k++) {
	cm[i*cc + j] += am[i*ac + k] * bm[k*cc + j];
      }
    }
  }
  // // Version 2: loop order (j i k)
  //  for (j=0; j<cc; j++) {
  //    for (i=0; i<ar; i++) {
  //      cm[i*cc + j] = 0;
  //      for (k=0; k<ac; k++) {
  //	cm[i*cc + j] += am[i*ac + k] * bm[k*cc + j];
  //      }
  //    }
  //  }

} // matmul

int main()
{
  int		r1, c1, r2, c2;
  matrix	a, b, c;

  printf("Matrix #1 rows and columns:\n");
  scanf("%d %d", &r1, &c1);
  printf("Matrix #2 rows and columns:\n");
  scanf("%d %d", &r2, &c2);

  if (r2 != c1) {
    printf("ERROR: matrices are incompatible!\n");
    exit(EXIT_FAILURE);
  }

  a.r = r1; a.c = c1;
  b.r = r2; b.c = c2;
  c.r = a.r; c.c = b.c;

  a.d = (float *) malloc(a.r*a.c * sizeof(float));  
  b.d = (float *) malloc(a.r*a.c * sizeof(float));  
  c.d = (float *) malloc(a.r*a.c * sizeof(float));  

  // printf("Enter elements of the first matrix:\n");
  matin(&a);
  // matout(&a);
  // printf("Enter elements of the second matrix:\n");
  matin(&b);
  // matout(&b);

  matmul(&a, &b, &c);

  // printf("The product is :\n");
  // matout(&c);

  return EXIT_SUCCESS;

} // main
