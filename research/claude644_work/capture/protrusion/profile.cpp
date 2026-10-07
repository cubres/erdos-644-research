// Decision version with per-step thresholds g[j]: can the prover keep c_j <= g[j] for all j?
// Then search the minimal sum of g over winning profiles (per order), for given m.
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
int NL = 7; int lineMask[7]; int budget[7]; int M; int G[7];
typedef vector<pair<int,int>> State;
struct Key { int j; State s; bool operator==(const Key&o) const {return j==o.j && s==o.s;} };
struct KH { size_t operator()(const Key&k) const { size_t h=k.j*1000003u; for(auto&p:k.s){h=h*1315423911u+p.first*131+p.second;} return h; } };
unordered_map<Key,char,KH> memo;
bool deadType(int T, int j){ int fut=0; for(int s=j;s<7;s++) fut|=1<<s; for(int l=0;l<NL;l++) if((T>>l)&1) if((lineMask[l]&fut)==0) return true; return false; }
void addType(map<int,int>& mp, int T, int c, int jn){ if(c<=0) return; if(deadType(T,jn)) return; mp[T]+=c; }
bool win(int j, const State& st){
  if(j==7) return true; Key key{j,st}; auto it=memo.find(key); if(it!=memo.end()) return it->second;
  int m=budget[j]*M; int n=st.size();
  vector<int> T(n),C(n),forced(n),relevant(n),newT(n);
  for(int i=0;i<n;i++){ T[i]=st[i].first; C[i]=st[i].second; int thr=0,all=1; for(int l=0;l<NL;l++) if((T[i]>>l)&1){ if((lineMask[l]>>j)&1) thr=1; else all=0; }
    relevant[i]=thr; forced[i]=all; int nt=0; for(int l=0;l<NL;l++) if(((T[i]>>l)&1)&&!((lineMask[l]>>j)&1)) nt|=1<<l; newT[i]=nt; }
  int freshT=0; for(int l=0;l<NL;l++) if(!((lineMask[l]>>j)&1)) freshT|=1<<l;
  if(m==0){ map<int,int> mp; for(int i=0;i<n;i++) addType(mp,T[i],C[i],j+1); bool r=win(j+1,State(mp.begin(),mp.end())); memo[key]=r; return r; }
  int fc=0; for(int i=0;i<n;i++) if(forced[i]) fc+=C[i];
  if(fc>G[j]){ memo[key]=0; return false; }
  bool found=false; vector<int> a(n,0);
  function<void(int,int)> recP=[&](int i,int cost){ if(found) return; if(cost>G[j]) return;
    if(i==n){ // check all adversary replies
      bool ok=true; vector<int> r(n,0);
      function<void(int,int)> recA=[&](int k,int used){ if(!ok) return; if(k==n){ map<int,int> mp; for(int q=0;q<n;q++){ addType(mp,T[q],C[q]-r[q],j+1); addType(mp,newT[q],r[q],j+1);} addType(mp,freshT,m-used,j+1); if(!win(j+1,State(mp.begin(),mp.end()))) ok=false; return; }
        int mx=(relevant[k]&&!forced[k])?min(C[k]-a[k],m-used):0; for(int x=mx;x>=0&&ok;x--){ r[k]=x; recA(k+1,used+x);} r[k]=0; };
      recA(0,0); if(ok) found=true; return; }
    if(forced[i]){ a[i]=C[i]; recP(i+1,cost+C[i]); a[i]=0; return; }
    if(!relevant[i]){ recP(i+1,cost); return; }
    for(int x=C[i];x>=0 && !found;x--){ a[i]=x; recP(i+1,cost+x);} a[i]=0; };
  recP(0,0);
  memo[key]=found; return found; }
int main(int argc,char**argv){ string ls=argv[1]; stringstream ss(ls); string w; int li=0; while(ss>>w){ int mk=0; for(char c:w) mk|=1<<(c-'0'); lineMask[li++]=mk; }
  string b=argv[2]; for(int i=0;i<7;i++) budget[i]=b[i]-'0'; M=atoi(argv[3]);
  // enumerate profiles with steps having budget; g_j in [0, 2M]; find min sum. Search by increasing sum.
  vector<int> steps; for(int j=0;j<7;j++) if(budget[j]) steps.push_back(j);
  int maxg=2*M;
  for(int S=0; S<=maxg*(int)steps.size(); S++){
    // enumerate compositions of S into steps.size() parts each <= maxg
    vector<int> g(steps.size(),0); bool any=false; vector<vector<int>> wins;
    function<void(int,int)> rec=[&](int idx,int rem){ if(idx==(int)steps.size()-1){ if(rem>maxg) return; g[idx]=rem; for(int j=0;j<7;j++) G[j]=0; for(size_t q=0;q<steps.size();q++) G[steps[q]]=g[q]; memo.clear(); if(win(0,State())){ any=true; wins.push_back(g);} return; }
      for(int x=0;x<=min(maxg,rem);x++){ g[idx]=x; rec(idx+1,rem-x);} };
    rec(0,S);
    if(any){ printf("m=%d min profile sum=%d; winning profiles:", M, S); for(auto&v:wins){ printf(" ("); for(size_t q=0;q<v.size();q++) printf("%d%s",v[q],q+1<v.size()?",":""); printf(")"); } printf("\n"); return 0; }
  }
}
