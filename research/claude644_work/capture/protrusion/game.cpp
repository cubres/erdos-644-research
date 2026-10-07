// Exact discrete protrusion game solver (integer vertices).
// Steps 0..6 = points of the dual Fano plane (time order). A vertex's pattern must contain no line.
// A vertex is represented by its set of LIVE lines (lines disjoint from its pattern).
// Usage: ./game "l0 l1 ... l6" budgets m   where each line is like 013 (three step digits), budgets like 0111111
#include <bits/stdc++.h>
using namespace std;
int NL = 7;
int lineMask[7]; // bitmask of steps in each line
int budget[7];
int M;
// type = bitmask over lines (live lines)
typedef vector<pair<int,int>> State; // sorted (type,count)
struct Key { int j; State s; bool operator==(const Key&o) const {return j==o.j && s==o.s;} };
struct KH { size_t operator()(const Key&k) const { size_t h=k.j*1000003u; for(auto&p:k.s){h=h*1315423911u+p.first*131+p.second;} return h; } };
unordered_map<Key,int,KH> memo;
long long nodes=0;
bool deadType(int T, int j){ // j = next step index (future steps are j..6)
    int fut = 0; for(int s=j;s<7;s++) fut|=1<<s;
    for(int l=0;l<NL;l++) if((T>>l)&1) if((lineMask[l]&fut)==0) return true;
    return false;
}
int solve(int j, const State& st);
void addType(map<int,int>& mp, int T, int c, int jnext){ if(c<=0) return; if(deadType(T,jnext)) return; mp[T]+=c; }
int solve(int j, const State& st){
    if(j==7) return 0;
    Key key{j,st};
    auto it=memo.find(key); if(it!=memo.end()) return it->second;
    nodes++;
    int m = budget[j]*M;
    int n = st.size();
    vector<int> T(n), C(n), forced(n), relevant(n), newT(n);
    for(int i=0;i<n;i++){ T[i]=st[i].first; C[i]=st[i].second;
        int thr=0, all=1; for(int l=0;l<NL;l++) if((T[i]>>l)&1){ if((lineMask[l]>>j)&1) thr=1; else all=0; }
        relevant[i]=thr; forced[i]=all; // all live lines pass through j -> forced (T nonempty always)
        int nt=0; for(int l=0;l<NL;l++) if(((T[i]>>l)&1) && !((lineMask[l]>>j)&1)) nt|=1<<l; newT[i]=nt; }
    int freshT=0; for(int l=0;l<NL;l++) if(!((lineMask[l]>>j)&1)) freshT|=1<<l;
    if(m==0){ // nothing happens except time passes
        map<int,int> mp; for(int i=0;i<n;i++) addType(mp,T[i],C[i],j+1);
        State ns(mp.begin(),mp.end()); int v=solve(j+1,ns); memo[key]=v; return v; }
    int best=INT_MAX;
    // prover avoid vector a[i]: forced -> C[i]; relevant non-forced -> 0..C[i]; non-relevant -> 0
    vector<int> a(n,0);
    function<void(int,int)> recP = [&](int i, int cost){
        if(cost>=best) return;
        if(i==n){
            // adversary: choose r[i] <= C[i]-a[i] for relevant non-forced, sum<=m
            int worst=cost; vector<int> r(n,0);
            function<bool(int,int)> recA=[&](int k,int used)->bool{ // returns true if cutoff
                if(k==n){
                    map<int,int> mp;
                    for(int q=0;q<n;q++){ addType(mp,T[q],C[q]-r[q],j+1); addType(mp,newT[q],r[q],j+1);} 
                    addType(mp,freshT,m-used,j+1);
                    State ns(mp.begin(),mp.end()); int v=solve(j+1,ns);
                    if(v>worst) worst=v;
                    return worst>=best;
                }
                int mx = (relevant[k]&&!forced[k]) ? min(C[k]-a[k], m-used) : 0;
                for(int x=mx;x>=0;x--){ r[k]=x; if(recA(k+1,used+x)) {r[k]=0; return true;} }
                r[k]=0; return false; };
            recA(0,0);
            if(worst<best) best=worst;
            return;
        }
        if(forced[i]){ a[i]=C[i]; recP(i+1,cost+C[i]); a[i]=0; return; }
        if(!relevant[i]){ a[i]=0; recP(i+1,cost); return; }
        for(int x=0;x<=C[i];x++){ a[i]=x; recP(i+1,cost+x); }
        a[i]=0;
    };
    recP(0,0);
    memo[key]=best; return best;
}
int main(int argc,char**argv){
    // argv[1]: lines as "013 026 045 124 156 235 346"; argv[2] budgets "0111111"; argv[3] m
    string ls=argv[1]; stringstream ss(ls); string w; int li=0;
    while(ss>>w){ int mk=0; for(char c:w) mk|=1<<(c-'0'); lineMask[li++]=mk; }
    string b=argv[2]; for(int i=0;i<7;i++) budget[i]=b[i]-'0';
    M=atoi(argv[3]);
    State s0; int v=solve(0,s0);
    printf("m=%d value=%d states=%zu nodes=%lld\n",M,v,memo.size(),nodes);
}
