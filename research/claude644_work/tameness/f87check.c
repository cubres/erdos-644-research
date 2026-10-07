/* build the capture/notes_tameness [s2.3] candidate: 8-subsets E of [15] with |E cap X| odd and {a,b} not in E,
   X = {0..6}, b = 0 in X, a = 7 notin X.  Check (7,2) exactly and tau. */
#include "lib72.h"
#include <time.h>
int main(){
  lib_init(15); fam H; fam_init(&H);
  mask X = 0x7F; int a = 7, b = 0;
  for (mask m = 0; m < (1u<<15); m++) if (popc(m) == 8 && (popc(m & X) & 1) && !((m>>a&1) && (m>>b&1))) fam_add(&H, m);
  fam_sort(&H);
  printf("edges %d\n", H.m); fflush(stdout);
  clock_t c = clock(); mask out[8]; int r = find_bad(&H, 7, out);
  printf("find_bad -> %d (%.1fs)\n", r, (double)(clock()-c)/CLOCKS_PER_SEC);
  if (r){ for (int i = 0; i < r; i++){ for (int v = 0; v < 15; v++) if (out[i]>>v&1) printf("%d,", v); printf("\n"); } }
  c = clock(); printf("tau %d (%.1fs)\n", tau_of(&H), (double)(clock()-c)/CLOCKS_PER_SEC);
  int cls[MAXN]; printf("twin classes %d\n", twin_classes(&H, cls));
  return 0;
}
