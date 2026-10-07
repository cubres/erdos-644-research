// pendant2.c: as pendant.c but with progress output and a wall-time budget (seconds) for the greedy phase.
#include "../lib72.h"
#include <time.h>
int main(int argc,char**argv){
  int k=atoi(argv[1]), M=atoi(argv[2]); uint64_t seed=atoll(argv[3]); double budget=atof(argv[4]);
  int N=M+1; lib_init(N); rng_seed(seed); fam H; fam_init(&H);
  uint32_t s=(1u<<k)-1; while(s<(1u<<M)){fam_add(&H,s); uint32_t c=s&-s,r=s+c; s=(((r^s)>>2)/c)|r;}
  fam_sort(&H); int core=H.m;
  static mask cand[20000]; int nc=0; s=(1u<<(k-1))-1; while(s<(1u<<M)){cand[nc++]=s|(1u<<M); uint32_t c=s&-s,r=s+c; s=(((r^s)>>2)/c)|r;}
  for(int i=nc-1;i>0;i--){int j=rng_next()%(i+1); mask t=cand[i];cand[i]=cand[j];cand[j]=t;}
  int added=0,tried=0; mask cert[8]; int ncert; time_t t0=time(0);
  for(int i=0;i<nc && difftime(time(0),t0)<budget;i++){ tried++;
    if(addable(&H,cand[i],cert,&ncert)){ fam_add(&H,cand[i]); fam_sort(&H); addable_reset(); added++; }
    if(tried%50==0){printf("  tried %d added %d (%.0fs)\n",tried,added,difftime(time(0),t0)); fflush(stdout);} }
  printf("k=%d M=%d seed=%llu core=%d candidates=%d tried=%d added=%d\n",k,M,(unsigned long long)seed,core,nc,tried,added); fflush(stdout);
  printf("tau=%d (3k/4=%.2f)\n", tau_of(&H), 0.75*k); fflush(stdout);
  return 0;
}
