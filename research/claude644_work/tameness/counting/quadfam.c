// quadfam.c: quadratic (matching) families and variants; exact tau (bitset) and (7,2) via lib72 find_bad.
// usage: quadfam N k variant [linP]
// variant 0: #matching pairs inside E odd; 1: (#pairs + |E cap P|) odd, |P|=linP (P = first linP points)
// variant 2: #pairs inside E odd, matching only on first 2*linP points (partial matching)
#include "../lib72.h"
#include <time.h>
int main(int argc,char**argv){
  int N=atoi(argv[1]),k=atoi(argv[2]),var=atoi(argv[3]); int lp=argc>4?atoi(argv[4]):0;
  lib_init(N); fam H; fam_init(&H);
  uint32_t P=0; for(int i=0;i<lp;i++)P|=1u<<i;
  int npairs = (var==2)? lp : N/2;
  uint32_t s=(1u<<k)-1; long ne=0;
  while(s < (1u<<N)){
    int np=0; for(int i=0;i<npairs;i++){uint32_t pm=3u<<(2*i); if((s&pm)==pm)np++;}
    int keep = (var==1)? ((np+__builtin_popcount(s&P))&1) : (np&1);
    if(keep){fam_add(&H,s);ne++;}
    uint32_t c=s&-s, rr=s+c; s=(((rr^s)>>2)/c)|rr;
  }
  fam_sort(&H);
  size_t M=(size_t)1<<N; uint8_t*G=calloc(M,1); for(int i=0;i<H.m;i++)G[H.e[i]]=1;
  for(int i=0;i<N;i++){uint32_t b=1u<<i; for(size_t m=0;m<M;m++) if((m&b)&&G[m^b]) G[m]=1;}
  int alpha=0; for(size_t m=0;m<M;m++) if(!G[m]){int c=__builtin_popcount((uint32_t)m); if(c>alpha)alpha=c;}
  printf("N=%d k=%d var=%d lp=%d edges=%ld tau=%d 3k/4=%.2f\n",N,k,var,lp,ne,N-alpha,0.75*k); fflush(stdout);
  clock_t t0=clock(); mask out[8]; int b=find_bad(&H,7,out);
  printf("  is72=%d (%.1fs)",b==0,(double)(clock()-t0)/CLOCKS_PER_SEC);
  if(b){printf(" bad:"); for(int i=0;i<b;i++)printf(" %x",out[i]);} printf("\n");
  return 0;
}
