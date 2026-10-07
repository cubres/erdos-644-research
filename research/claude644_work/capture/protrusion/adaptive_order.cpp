// Discrete protrusion game where the prover chooses the NEXT line adaptively (after seeing the history).
// Dual Fano plane: points 0..6 = original lines (steps), lines = concurrent triples. Standard plane {i,i+1,i+3} mod 7.
// anchored: point 0 is the anchor (processed first, no outside mass).
#include <vector>
#include <map>
#include <unordered_map>
#include <functional>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <climits>
#include <algorithm>
using namespace std;
int lineMask[7]; int M; bool anchored;
typedef vector<pair<int,int>> State;
struct Key { int used; State s; bool operator==(const Key&o) const {return used==o.used && s==o.s;} };
struct KH { size_t operator()(const Key&k) const { size_t h=k.used*1000003u; for(auto&p:k.s){h=h*1315423911u+p.first*131+p.second;} return h; } };
unordered_map<Key,int,KH> memo;
bool deadType(int T, int used){ for(int l=0;l<7;l++) if((T>>l)&1) if((lineMask[l]&~used)==0) return true; return false; }
void addType(map<int,int>& mp, int T, int c, int used){ if(c<=0) return; if(deadType(T,used)) return; mp[T]+=c; }
int solve(int used, const State& st){
  if(used==127) return 0; Key key{used,st}; auto it=memo.find(key); if(it!=memo.end()) return it->second;
  int best=INT_MAX;
  for(int j=0;j<7;j++){ if((used>>j)&1) continue;
    int n=st.size(); vector<int> T(n),C(n),forced(n),relevant(n),newT(n);
    for(int i=0;i<n;i++){ T[i]=st[i].first; C[i]=st[i].second; int thr=0,all=1; for(int l=0;l<7;l++) if((T[i]>>l)&1){ if((lineMask[l]>>j)&1) thr=1; else all=0; }
      relevant[i]=thr; forced[i]=all; int nt=0; for(int l=0;l<7;l++) if(((T[i]>>l)&1)&&!((lineMask[l]>>j)&1)) nt|=1<<l; newT[i]=nt; }
    int freshT=0; for(int l=0;l<7;l++) if(!((lineMask[l]>>j)&1)) freshT|=1<<l;
    int nused=used|(1<<j);
    vector<int> a(n,0);
    function<void(int,int)> recP=[&](int i,int cost){ if(cost>=best) return;
      if(i==n){ int worst=cost; vector<int> r(n,0);
        function<void(int,int)> recA=[&](int k,int usedb){ if(worst>=best) return; if(k==n){ map<int,int> mp; for(int q=0;q<n;q++){ addType(mp,T[q],C[q]-r[q],nused); addType(mp,newT[q],r[q],nused);} addType(mp,freshT,M-usedb,nused); int v=solve(nused,State(mp.begin(),mp.end())); if(v>worst) worst=v; return; }
          int mx=(relevant[k]&&!forced[k])?min(C[k]-a[k],M-usedb):0; for(int x=mx;x>=0;x--){ r[k]=x; recA(k+1,usedb+x);} r[k]=0; };
        recA(0,0); if(worst<best) best=worst; return; }
      if(forced[i]){ a[i]=C[i]; recP(i+1,cost+C[i]); a[i]=0; return; }
      if(!relevant[i]){ recP(i+1,cost); return; }
      for(int x=0;x<=C[i];x++){ a[i]=x; recP(i+1,cost+x);} a[i]=0; };
    recP(0,0);
  }
  memo[key]=best; return best; }
int main(int argc,char**argv){ for(int i=0;i<7;i++) lineMask[i]=(1<<i)|(1<<((i+1)%7))|(1<<((i+3)%7));
  M=atoi(argv[1]); anchored=atoi(argv[2]);
  int v; if(anchored){ v=solve(1,State()); } else { v=solve(0,State()); }
  printf("adaptive order, %s, m=%d: value %d (states %zu)\n", anchored?"anchored":"unanchored", M, v, memo.size()); }
