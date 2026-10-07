// pendant.c: H = K_M^(k) on C=[M] plus pendant edges F+{d}, F a (k-1)-subset of C, added by random greedy with (7,2) test.
#include "../lib72.h"
#include <time.h>
int main(int argc,char**argv){
  int k=atoi(argv[1]), M=atoi(argv[2]); uint64_t seed=atoll(argv[3]);
  int N=M+1; lib_init(N); rng_seed(seed); fam H; fam_init(&H);
  uint32_t s=(1u<<k)-1; while(s<(1u<<M)){fam_add(&H,s); uint32_t c=s&-s,r=s+c; s=(((r^s)>>2)/c)|r;}
  fam_sort(&H); int core=H.m;
  mask cand[20000]; int nc=0; s=(1u<<(k-1))-1; while(s<(1u<<M)){cand[nc++]=s|(1u<<M); uint32_t c=s&-s,r=s+c; s=(((r^s)>>2)/c)|r;}
  for(int i=nc-1;i>0;i--){int j=rng_next()%(i+1); mask t=cand[i];cand[i]=cand[j];cand[j]=t;}
  int added=0; mask cert[8]; int ncert;
  for(int i=0;i<nc;i++){ if(addable(&H,cand[i],cert,&ncert)){ fam_add(&H,cand[i]); fam_sort(&H); addable_reset(); added++; } }
  printf("k=%d M=%d core=%d pendant candidates=%d added=%d (density %.3f)\n",k,M,core,nc,added,(double)added/nc);
  mask out[8]; printf("final is72=%d tau=%d (3k/4=%.2f)\n", find_bad(&H,7,out)==0, tau_of(&H), 0.75*k);
  return 0;
}
