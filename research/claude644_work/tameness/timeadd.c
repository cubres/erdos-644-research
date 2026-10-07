#include "lib72.h"
#include <time.h>
int main(int argc, char **argv){
  int n = atoi(argv[1]), k = atoi(argv[2]), n0 = atoi(argv[3]); lib_init(n);
  fam H; fam_init(&H); for (mask s = 0; s < (1u<<n0); s++) if (popc(s) == k) fam_add(&H, s); fam_sort(&H);
  int cnt = 0, add = 0; clock_t c = clock();
  for (mask s = 0; s < (1u<<n); s++) if (popc(s) == k && !fam_has(&H, s)){ cnt++; add += addable(&H, s, NULL, NULL);
     if (cnt % 50 == 0){ fprintf(stderr, "%d checks %.1fs\n", cnt, (double)(clock()-c)/CLOCKS_PER_SEC); } if (cnt >= 200) break; }
  printf("n=%d k=%d n0=%d: %d candidates, %d addable, %.2fs\n", n, k, n0, cnt, add, (double)(clock()-c)/CLOCKS_PER_SEC);
}
