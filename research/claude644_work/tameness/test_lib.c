#include "lib72.h"
/* reads families from stdin: line "N m" then m masks; prints is72(0/1) tau twins */
int main(){
  int n, m;
  while (scanf("%d %d", &n, &m) == 2){
    lib_init(n); fam H; fam_init(&H);
    for (int i = 0; i < m; i++){ unsigned x; scanf("%u", &x); fam_add(&H, x); }
    fam_sort(&H);
    mask out[8]; int b = find_bad(&H, 7, out);
    int cls[MAXN]; int nc = twin_classes(&H, cls);
    printf("%d %d %d\n", b == 0, tau_of(&H), nc);
    fam_free(&H); addable_reset();
  }
  return 0;
}
