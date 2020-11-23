#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <float.h>
double max_array(double* a, int N);
double X_imp(int i, double K, double P);
void compute_dos_log(double* gl, int N, double P, double K, int live);
void compute_dos_alpha_log(double* gl, double* rn, int N, double K, int live);
void log_weights(double* El, double* gl, double* wl, int N, double T);
double heat_capacity(double* El, double* wl, int N, double T, double ndof, double * U, double * U2);
void heat_capacity_loop(double* El, double* gl, double* wl, double* Cvl, double * Ul, double * U2l, double * Tlist, int N, int nT, double ndof);

double max_array(double* a, int N)
{
  int i;
  double max=-DBL_MAX;
  for (i=0; i<N; ++i)
    {
      if (a[i]>max)
	{
	  max=a[i];
	}
    }
  return max;
}

double X_imp(int i, double K, double P)
{
  double X;
  X = (K - (i%(int)P) )/( K - (i%(int)P) + 1);
  return X;
}

void compute_dos_log(double* gl, int N, double P, double K, int live)
{
  // gl is an array of 0's of size N, K is the number of replicas
  int i,j,lim;
  double Xf;
  double m;
  //step i =0, m here is Xb
  m = log(2. - X_imp(0,K,P)); // reflecting boundary condition, this is X0 
  gl[0] = log(0.5) + m + log(1-X_imp(0,K,P)*X_imp(1,K,P));
  
  //for(i=1;i<(N-K-1);++i) when using live replica
  if (live == 1)
    {
      lim = (N-K-1);
    }
  else
    {
      lim = (N-1);
    }
  for(i=1;i<lim;++i)
    {
      m += log(X_imp(i-1,K,P));
      gl[i] = log(0.5) + m + log(1 - X_imp(i,K,P) * X_imp(i+1,K,P));
      //printf("gl[%d] is %E \n",i, gl[i]);
    }
  //calculate density of states for live replica energies (if flag is on)
  if (live == 1)
    {
      m += log(X_imp(i,K,P));
      j = 0;
      for(i=lim;i<(N-1);++i)
	{
	  gl[i] = log(0.5) + m + log(1 - (K-j)/(K-j+1) * (K-(j+1))/(K-(j+1)+1));
	  m += log((K-j)/(K-j+1));
	  ++j;
	}
      ++i;
      m -= log((K-(j-1))/(K-(j-1)+1));
      Xf = -(K-j)/(K-j+1);
      gl[N-1] = log(0.5) + m + log(1 - (K-j)/(K-j+1) * Xf);
    }
  else
    {
      ++i;
      m += log(X_imp(i-1,K,P));
      Xf = - X_imp(i,K,P);
      gl[N-1] = log(0.5) + m + log(1 - X_imp(i,K,P) * Xf);
    }
}

void compute_dos_alpha_log(double* gl, double* rn, int N, double K, int live)
{
  // gl is an array of 0's of size N, K is the number of replicas
  int i,j,lim;
  double Xf;
  double m;
  //step i =0, m here is Xb
  m = log(2. - rn[0]); // reflecting boundary condition, this is X0 
  gl[0] = log(0.5) + m + log(1-rn[0]*rn[1]);
  
  //for(i=1;i<(N-K-1);++i) when using live replica
  if (live == 1)
    {
      lim = (N-K-1);
    }
  else
    {
      lim = (N-1);
    }
  for(i=1;i<lim;++i)
    {
      m += log(rn[i-1]);
      gl[i] = log(0.5) + m + log(1 - (rn[i] * rn[i+1]));
      //printf("gl[%d] is %E \n",i, gl[i]);
    }
  //calculate density of states for live replica energies (if flag is on)
  if (live == 1)
    {
      j = 0;
      for(i=lim;i<(N-1);++i)
	{
	  m += log(rn[i-1]);
	  gl[i] = log(0.5) + m + log(1 - rn[i] * rn[i+1]);
	  ++j;
	}
      ++i;
      Xf = -rn[i];
      gl[N-1] = log(0.5) + m + log(1 - rn[i] * Xf);
    }
  else
    {
      ++i;
      m += log(rn[i-1]);
      Xf = - rn[i];
      gl[N-1] = log(0.5) + m + log(1 - rn[i] * Xf);
    }
}

void log_weights(double* El, double* gl, double* wl, int N, double T)
{
  int i;
  double beta = 1/T;
  
  for(i=0;i<N;++i)
    {
      wl[i] = gl[i] - beta * El[i];
    }
}



////////////////////////////caclulate heat capacity for a single T////////////////////////
double heat_capacity(double* El, double* wl, int N, double T, double ndof, double * U, double * U2)
{
  //K is the number of replicas, beta the reduced temperature and E is the array of energies 
  int i;
  double Cv;
  double Z = 0;
  double _U = 0;
  double _U2 = 0;
  double beta = 1./T;
  double bolz = 0.;

  for(i=0;i<N;++i)
    {
      bolz = exp(wl[i]);
      Z += bolz;
      //printf("Z %E \n",Z);
      _U += El[i] * bolz;
      _U2 += El[i] * El[i] * bolz;
    }

  _U /= Z;
  _U2 /= Z;
  Cv =  (_U2 - _U*_U)*beta*beta + 0.5 * ndof;
  //printf("Z _U _U2 Cv %E %E %E %E \n",Z,_U,_U2,Cv);
  *U = _U;
  *U2 = _U2;
  return Cv;
}

//////////////////////////////calculate heat capacity over a set of Ts/////////////////////
void heat_capacity_loop(double* El, double* gl, double* wl, double* Cvl, double * Ul, double * U2l, double * Tlist, int N, int nT, double ndof)
{
  //Cvl is a 0's array of size N (same size as El)
  //the mean internal energy for each temperature will be returned in U
  //the mean internal energy squared for each temperature will be returned in U2
  int i,j;
  double T = 0;
  double wl_max;
  double _U = 0.;
  double _U2 = 0.;
  
  for(i=0;i<nT;++i)
    {
      T = Tlist[i];
      log_weights(El, gl, wl, N, T);
      wl_max = max_array(wl,N);
    
      //printf("wl_max %d \n",wl_max);
    
      for(j=0;j<N;++j)
	{
	  wl[j] -= wl_max;
	}
    
      //printf("i %d\n", i);
      Cvl[i] = heat_capacity(El, wl, N, T, ndof, &_U, &_U2);
      //printf("    done with heat_capacity\n");
      Ul[i] = _U;
      U2l[i] = _U2;
      //printf("    done\n");
    }
}
