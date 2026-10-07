/* badfind: read "N m e1..em" lines; for each, print up to R bad tuples (edge masks) found by repeatedly
   searching and deleting a random edge of the found tuple; "OK" if (7,2). Then "SAT"/"TAU t"/"TWINS c". */
#include "lib72.h"
int main(int argc, char **argv){
  int R = argc > 1 ? atoi(argv[1]) : 20; int n, m;
  rng_seed(12345);
  while (scanf("%d %d", &n, &m) == 2){
    lib_init(n); fam H; fam_init(&H);
    for (int i = 0; i < m; i++){ unsigned x; scanf("%u", &x); fam_add(&H, x); }
    fam_sort(&H);
    fam G; fam_copy(&G, &H); int cnt = 0; mask out[8];
    while (cnt < R){ int b = find_bad(&G, 7, out); if (!b) break;
      printf("BAD"); for (int i = 0; i < b; i++) printf(" %u", out[i]); printf("\n"); cnt++;
      mask del = out[rng_next() % b]; int w = 0; for (int t = 0; t < G.m; t++) if (G.e[t] != del) G.e[w++] = G.e[t]; G.m = w; }
    if (cnt == 0) printf("OK\n");
    printf("END\n"); fflush(stdout);
    fam_free(&H); fam_free(&G);
  }
  return 0;
}
