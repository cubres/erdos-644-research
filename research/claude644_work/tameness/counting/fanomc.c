// fanomc.c : Step-1 numerics.  Families on N<=24 points, k-uniform; G = up-closure bitset (W contains an edge).
// Random Fano placements alpha: V -> F_2^3 (iid from lambda, or exact cell sizes); rows R_p = {v: <alpha_v,p>=1}.
// Outputs failure-pattern statistics: g_j, g_jl, collinear-triple joint, P[Z=0], D=E(Z-1)^+.
// usage: fanomc fam N k param seed samples mode [empty_prob]
//  fam: 0 complete, 1 thinning(rho=param), 2 FKW parity (|P|=param), 3 code r=param (random v, a=1), 4 thinned parity (rho=param, |P|=k)
//  mode: 0 iid alpha uniform on nonzero (w/ empty prob), 1 exact balanced cell sizes (random permutation)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
static uint64_t rs=88172645463325252ULL;
static inline uint64_t xr(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static inline double ur(void){return (xr()>>11)*(1.0/9007199254740992.0);}
int N,k; uint8_t *G;
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  int fam=atoi(argv[1]); N=atoi(argv[2]); k=atoi(argv[3]); double par=atof(argv[4]);
  rs ^= (uint64_t)atoll(argv[5])*0x9E3779B97F4A7C15ULL; for(int i=0;i<10;i++)xr();
  long S=atol(argv[6]); int mode=atoi(argv[7]); double pe = argc>8? atof(argv[8]):0.0;
  size_t M=(size_t)1<<N; G=calloc(M,1);
  uint32_t P = 0; int Psz=(fam==2)?(int)par:k; for(int i=0;i<Psz;i++)P|=1u<<i;
  uint32_t vx[32]; int r=(int)par; if(fam==3){for(int i=0;i<N;i++)vx[i]=xr()&((1u<<r)-1);} 
  long ne=0;
  // enumerate k-subsets (Gosper)
  uint32_t s=(1u<<k)-1;
  while(s < (1u<<N)){
    int keep=0;
    if(fam==0) keep=1;
    else if(fam==1) keep = ur()<par;
    else if(fam==2) keep = __builtin_popcount(s&P)&1;
    else if(fam==3){uint32_t acc=0; for(int i=0;i<N;i++) if(s>>i&1) acc^=vx[i]; keep = acc==1;}
    else if(fam==4) keep = (__builtin_popcount(s&P)&1) && ur()<par;
    if(keep){G[s]=1;ne++;}
    uint32_t c=s&-s, rr=s+c; s=(((rr^s)>>2)/c)|rr;
  }
  for(int i=0;i<N;i++){uint32_t b=1u<<i; for(size_t m=0;m<M;m++) if((m&b)&&G[m^b]) G[m]=1;}
  int alpha=0; for(size_t m=0;m<M;m++) if(!G[m]){int c=__builtin_popcount((uint32_t)m); if(c>alpha)alpha=c;}
  printf("fam=%d N=%d k=%d par=%g edges=%ld alpha=%d tau=%d (3k/4=%.2f)\n",fam,N,k,par,ne,alpha,N-alpha,0.75*k);
  // placements
  long hist[128]; memset(hist,0,sizeof hist);
  int perm[32]; int cellsz[8];
  // exact balanced: cells 1..7 (nonzero alpha) sizes floor/ceil of N*(1-pe)/7, empty gets rest
  if(mode==1){int ne0=(int)floor(N*pe+0.5); int rest=N-ne0; cellsz[0]=ne0; for(int c=1;c<8;c++)cellsz[c]=rest/7+((c-1)<rest%7);}  
  double rowsz[7]={0};
  for(long t=0;t<S;t++){
    uint8_t al[32];
    if(mode==0){for(int v=0;v<N;v++){ if(ur()<pe) al[v]=0; else al[v]=1+(xr()%7);} }
    else { for(int v=0;v<N;v++)perm[v]=v; for(int v=N-1;v>0;v--){int j=xr()%(v+1);int tt=perm[v];perm[v]=perm[j];perm[j]=tt;}
      int pos=0; for(int c=0;c<8;c++) for(int q=0;q<cellsz[c];q++) al[perm[pos++]]=c; }
    uint32_t R[7]={0};
    for(int v=0;v<N;v++) for(int p=1;p<8;p++) if(__builtin_popcount(al[v]&p)&1) R[p-1]|=1u<<v;
    int pat=0; for(int p=0;p<7;p++){ if(!G[R[p]]) pat|=1<<p; rowsz[p]+=__builtin_popcount(R[p]); }
    hist[pat]++;
  }
  double g[7],gg[7][7]; double pz0=(double)hist[0]/S, D=0, EZ=0;
  for(int p=0;p<7;p++){g[p]=0; for(int q=0;q<7;q++)gg[p][q]=0;}
  for(int pat=0;pat<128;pat++){ double w=(double)hist[pat]/S; int z=__builtin_popcount(pat); EZ+=z*w; if(z>1)D+=(z-1)*w;
    for(int p=0;p<7;p++) if(pat>>p&1){ g[p]+=w; for(int q=0;q<7;q++) if(pat>>q&1) gg[p][q]+=w; } }
  printf("mode=%d pe=%.3f samples=%ld  mean row size %.3f\n",mode,pe,S,rowsz[0]/S);
  printf("g_p:"); for(int p=0;p<7;p++)printf(" %.4f",g[p]); printf("\n");
  printf("P[Z=0]=%.6f  sum g=%.4f  D=E(Z-1)^+=%.4f  check 1-sum g+D=%.6f\n",pz0,EZ,D,1-EZ+D);
  // pairwise dependence ratios g_pq/(g_p g_q) ; lines of Fano in F2^3: {p,q,p^q}
  double mx=0,mn=1e9; for(int p=0;p<7;p++)for(int q=p+1;q<7;q++){double rr=gg[p][q]/(g[p]*g[q]+1e-300); if(rr>mx)mx=rr; if(rr<mn)mn=rr;}
  printf("pair ratio g_pq/(g_p g_q): min %.4f max %.4f\n",mn,mx);
  // collinear triple {1,2,3} (p=1,2,3 -> indices 0,1,2): P[all three succeed] vs product of f
  long col=0,tri=0; // triangle {1,2,4}: indices 0,1,3
  for(int pat=0;pat<128;pat++){ if(!(pat&7)) col+=hist[pat]; if(!(pat&0xB)) tri+=hist[pat]; }
  double f0=1-g[0],f1=1-g[1],f2=1-g[2],f3=1-g[3];
  printf("collinear{1,2,3} P[all succeed]=%.5f  prod f=%.5f  ratio=%.4f | triangle{1,2,4} P=%.5f prod=%.5f ratio=%.4f\n",
    (double)col/S,f0*f1*f2,(double)col/S/(f0*f1*f2+1e-300),(double)tri/S,f0*f1*f3,(double)tri/S/(f0*f1*f3+1e-300));
  double f7=1; for(int p=0;p<7;p++) f7*=1-g[p];
  printf("7-wise ratio P[Z=0]/prod f = %.4f (prod f=%.3e)\n",pz0/(f7+1e-300),f7);
  return 0;
}
