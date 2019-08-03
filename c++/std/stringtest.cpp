#include<string>
#include<iostream>
#include<cstring>
using namespace std;
int main(){
    string s,s1;
    int j=0;
    getline(cin,s);
    getline(cin,s1);
    for(int i=0;i<s.length();i++){
        if(s[i]!=s1[i]){
            cout<<i+1<<"\n";
            j++;
        }
    }
    cout<<"|"<<j<<"|";
    return 0;
}
