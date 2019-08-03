#include <iostream>
#include<vector>
#include<map>
#include<sstream>
#include<string>
#include<stack>
#include<queue>
#include<fstream>
#include<utility>
using namespace std;
vector<pair<int,int>> *a;
typedef vector<vector<pair<int,int>>> Graph;

map<string,int> Points;
//vector<string> name;
/*void assignName(string &x,int &i,Graph &G){
//    name.push_back(x);
    Points[x]=i;
    a=new vector<pair<bool,int>>;
    G.push_back(*a);
    i++;
}
bool checkName(string &x){
    return Points.find(x)==Points.end();
}
bool isContacted(string &x,string&y){
    if(G[Points[x]].empty()) return false;
    for(int &xx:G[Points[x]]){
        if(xx==Points[y]) return true;
    }
    return false;
}
bool Find(vector<int> &arr,int x){
    if(arr.empty()) return false;
    for(int i=0;i<arr.size();i++){
        if(arr[i]==x)
        return true;
    }
    return false;
}
int dfs(vector<vector<int>> &G,string &begin,string &end){
    stack<int> open;
    vector<int> close;
    open.push(Points[begin]);
    int i=open.top();open.pop();
    while(i!=Points[end]){
        for(int &x:G[i]){
            if(!Find(close,x))
            {
                //cout<<x<<" ";
                open.push(x);
            }
        }
        close.push_back(i);
        if(open.empty()) break;
        i=open.top();open.pop();

    }
    if(i==Points[end]) return 1;
    return 0;

}
int bfs(vector<vector<int>> &G,string &begin,string &end){
    queue<int> open;
    vector<int> close;
    open.push(Points[begin]);
    int i=open.front();open.pop();
    while(i!=Points[end]){
        for(int &x:G[i]){
            if(!Find(close,x))
            {
                //cout<<x<<" ";
                open.push(x);
            }
        }
        close.push_back(i);
        if(open.empty()) break;
        i=open.front();open.pop();

    }
    if(i==Points[end]) return 1;
    return 0;

}*/
void printGraph(Graph G){
    for(int i=0;i<G.size();i++){
        cout<<char(i+65)<<"|";
        for(int j=0;j<G[i].size();j++){
            if(G[i][j].first)
            cout<<char(j+65)<<" ";
        }
        cout<<"\n";
    }
    cout<<"---------------------\n";
}
string randomPoint(){
    int i=rand()%10;
    switch(i){
    case 0:
        return "A";
    case 1:
        return "B";
    case 2:
        return "C";
    case 3:
        return "D";
    case 4:
        return "E";
    case 5:
        return "F";
    case 6:
        return "G";
    case 7:
        return "H";
    case 8:
        return "I";
    case 9:
        return "J";
    }
}
int Deg(Graph &G,int a){
	int res=0;
	for(int i=0;i<G.size();i++){
		res+=G[a][i].first;
	}
	return res;
}

void EulerCirculationUtil(Graph &G,int i=0){
    //int i=2;
    int j=0;
    int f=-1;
    int d=0;
    cout<<char(i+65);
    while(j<G.size()){
        if(G[i][j].first && Deg(G,j)>1){
           
           //cout<<char(i+65)<<char(j+65)<<Deg(G,j)<<"\n";
	   G[i][j].first--;
	   G[j][i].first--;
	   
	      i=j;
	      j=0;
	      cout<<char(i+65);
	      continue;
	}
        j++;
    }
    j=0;
    while(G[i][j].first==0&& j<G.size())
        j++;
    cout<<char(j+65);
    cout<<"\n";
}
void EulerCirculation(Graph G){
    int d=0;
    for(int i=0; i<G.size();i++){
	if(Deg(G,i)%2)
	d++;		
    }
    if(d==0){
	return EulerCirculationUtil(G);
    }else{
	if(d==2){
           int j=0;
           while(Deg(G,j)%2==0)
		j++;
	   return EulerCirculationUtil(G,j);
	}
    }
    cout<<"Not found!!!!";
    return;
}
int main(){
    ifstream ifs("Input");
    int e,n,x,y;
    string t;
    //stringstream ss;
    int i=0;
    ifs>>n>>e;
    Graph G;
    for (int i = 0; i < n; ++i)
    {
        vector<pair<int,int>> *a= new vector<pair<int,int>>;
        for (int j = 0; j < n; ++j)
        {
            pair<bool,int> *b= new pair<bool,int>(0,0);
            a->push_back(*b);
        }
        G.push_back(*a);
    }
    //string x,y;
    for(int iter=0;iter<e;iter++){
        //getline(ifs,t);
        //ss<<t;
        //getline(ss,x,' ');
        //getline(ss,y,' ');
        //ss.clear();

        ifs>>x>>y;
        //if(Points.empty()){
        //    assignName(x,i);
        //    assignName(y,i);
        //}
        //else{
        //    if(checkName(x)) assignName(x,i);
        //    if(checkName(y)) assignName(y,i);
        //}
        G[x][y].first++;
        G[y][x].first++;
        //G[Points[y]].push_back(Points[x]);
    }
    //cout<<"\n------\n";
    //for(auto& temp:G){
    //    cout<<(G.begin()-k);
    //    for(auto&xx:temp){
    //        cout<<xx<<" ";
    //    }
    //    cout<<"\n";
    //}
    //cout<<Points.end();

    int choice,flag;
    /*while(n>0){
    //    getline(cin,t);
    //    ss<<t;
    //    getline(ss,t,' ');
    //    choice=stoi(t);
    //    switch (choice)
    //    {
    //    case 1:
    //        getline(ss,x,' ');
    //        getline(ss,y,' ');
    //        if(checkName(x)) assignName(x,i);
    //        if(checkName(y)) assignName(y,i);
    //        if(isContacted(x,y)) cout<<"TRUE";
    //        else cout<<"FALSE";
    //        ss.clear();
    //        break;
    //    case 2:
    //        flag=0;
    //        getline(ss,x,' ');
    //        if(checkName(x)) assignName(x,i);
    //        cout<<G[Points[x]].size();
//
//            ss.clear();
//            break;
//        case 3:
//            getline(ss,x,' ');
//            getline(ss,y,' ');
//            ss.clear();
//            if(checkName(x)) assignName(x,i);
//            if(checkName(y)) assignName(y,i);
//            cout<<dfs(G,x,y);
//            break;
//        case 4:
//            getline(ss,x,' ');
//            getline(ss,y,' ');
//            ss.clear();
//            if(checkName(x)) assignName(x,i);
//            if(checkName(y)) assignName(y,i);
//            cout<<bfs(G,x,y);
//            break;
//        case 0:
//            printGraph();
//            ss.clear();
//        }
//        cout<<"\n";
//        n--;
//    }*/
    printGraph(G);
    EulerCirculation(G);
    printGraph(G);
    return 0;
}
