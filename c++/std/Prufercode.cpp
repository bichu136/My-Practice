#include<bits/stdc++.h>
using namespace std;
typedef std::vector<int> prufer;
typedef std::vector<vector<int>> Graph;
std::vector<int> pruferCode;
std::vector<vector<int>> G;
void PruferToGraph(std::vector<int> &code,std::vector<vector<int>> &G);
void GraphToPrufer(std::vector<vector<int>> &G,std::vector<int> &code);
int main(){
    int n;
    cin>>n;
    int t;
    G.resize(n+2);
    for (int i = 0; i < n; ++i)
    {
        cin>>t;
        pruferCode.push_back(t);
    }
    for (int i = 0; i < n+2; ++i)
    {
        G[i].assign(n+2,0);
    }
    PruferToGraph(pruferCode,G);
    std::vector<int> p2;
    for (int i = 0; i < G.size(); ++i)
    {
        for (int j = 0; j < G.size(); ++j)
        {
            cout<<G[i][j]<<" ";
        }
        cout<<"\n";
    }
    //GraphToPrufer(G,p2);
}
void PruferToGraph(prufer &code,Graph &G){
    int n=code.size()+2;
    vector<int> a(n,0);
    for (int i = 0; i < code.size(); ++i)
    {
        a[code[i]]+=1;
    }
    for (int i = 0; i < n; ++i)
    {
        cout<<a[i]<<" ";
    }
    cout<<"\n----------------------\n";
    for (int i = 0; i < code.size(); ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            cout<<a[j]<<" ";
            if(a[j]==0){
                G[code[i]][j]=1;
                G[j][code[i]]=1;
                a[code[i]]-=1;
                a[j]-=1;
                break;
            }
        }
        cout<<"\n";
    }
    for (int i = 0; i < n; ++i)
    {
        if(a[i]==0){
            if(code[code.size()-1]!=i){
                G[code[code.size()-1]][i]=1;
                G[i][code[code.size()-1]]=1;
                a[code[code.size()-1]]--;
                a[i]--;
                break;
            }
        }
    }
}
void GraphToPrufer(Graph &G,prufer &code){
}
