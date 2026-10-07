// Sum version: prover minimises total avoidance sum_j c_j (adversary maximises).
#include <vector>
#include <map>
#include <unordered_map>
#include <functional>
#include <string>
#include <sstream>
#include <cstdio>
#include <cstdlib>
#include <climits>
#include <algorithm>
using namespace std;
int NL = 7; int lineMask[7]; int budget[7]; int M;
typedef vector<pair<int,int>> State;
struct Key { int j; State s; bool operator==(const Key&o) const {return j==o.j && s==o.s;} };
struct KH { size_t operator()(const Key&k) const { size_t h=k.j*1000003u; for(auto&p:k.s){h=h*1315423911u+p.first*131+p.second;} return h; } };
unordered_map<Key,int,KH> memo;
bool deadType(int T, int j){ int fut=0; for(int s=j;s<7;s++) fut|=1<<s; for(int l=0;l<NL;l++) if((T>>l)&1) if((lineMask[l]&fut)==0) return true; return false; }
void addType(map<int,int>& mp, int T, int c, int jn){ if(c<=0) return; if(deadType(T,jn)) return; mp[T]+=c; }
int solve(int j, const State& st){
  if(j==7) return 0; Key key{j,st}; auto it=memo.find(key); if(it!=memo.end()) return it->second;
  int m=budget[j]*M; int n=st.size();
  vector<int> T(n),C(n),forced(n),relevant(n),newT(n);
  for(int i=0;i<n;i++){ T[i]=st[i].first; C[i]=st[i].second; int thr=0,all=1; for(int l=0;l<NL;l++) if((T[i]>>l)&1){ if((lineMask[l]>>j)&1) thr=1; else all=0; }
    relevant[i]=thr; forced[i]=all; int nt=0; for(int l=0;l<NL;l++) if(((T[i]>>l)&1)&&!((lineMask[l]>>j)&1)) nt|=1<<l; newT[i]=nt; }
  int freshT=0; for(int l=0;l<NL;l++) if(!((lineMask[l]>>j)&1)) freshT|=1<<l;
  if(m==0){ map<int,int> mp; for(int i=0;i<n;i++) addType(mp,T[i],C[i],j+1); int v=solve(j+1,State(mp.begin(),mp.end())); memo[key]=v; return v; }
  int best=INT_MAX; vector<int> a(n,0);
  function<void(int,int)> recP=[&](int i,int cost){ if(cost>=best) return;
    if(i==n){ int worst=0; vector<int> r(n,0);
      function<void(int,int)> recA=[&](int k,int used){ if(cost+worst>=best) return; if(k==n){ map<int,int> mp; for(int q=0;q<n;q++){ addType(mp,T[q],C[q]-r[q],j+1); addType(mp,newT[q],r[q],j+1);} addType(mp,freshT,m-used,j+1); int v=solve(j+1,State(mp.begin(),mp.end())); if(v>worst) worst=v; return; }
        int mx=(relevant[k]&&!forced[k])?min(C[k]-a[k],m-used):0; for(int x=mx;x>=0;x--){ r[k]=x; recA(k+1,used+x);} r[k]=0; };
      recA(0,0); if(cost+worst<best) best=cost+worst; return; }
    if(forced[i]){ a[i]=C[i]; recP(i+1,cost+C[i]); a[i]=0; return; }
    if(!relevant[i]){ recP(i+1,cost); return; }
    for(int x=0;x<=C[i];x++){ a[i]=x; recP(i+1,cost+x);} a[i]=0; };
  recP(0,0); memo[key]=best; return best; }
int main(int argc,char**argv){ string ls=argv[1]; stringstream ss(ls); string w; int li=0; while(ss>>w){ int mk=0; for(char c:w) mk|=1<<(c-'0'); lineMask[li++]=mk; }
  string b=argv[2]; for(int i=0;i<7;i++) budget[i]=b[i]-'0'; M=atoi(argv[3]);
  printf("%d\n", solve(0,State())); }
