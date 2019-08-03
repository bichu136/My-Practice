#include<iostream>

#include<cstring>
#include<map>
using namespace std;
bool checkAnagram(string &s,map<char,int> &a){
    for (int i=0;i<s.length();i++)
    {
        if(a.find(s[i])==a.end()){
            return false;
        }
        else
        {
            if(a[s[i]]<=0) return false;
            a[s[i]]--;
        }
    }
    return true;
}
int main(){
    string s,t;
    getline(cin,s);
    getline(cin,t);
    std::map<char,int>sm;
    if(s.length()!=t.length()){
        cout<<"NOT ANAGRAM!!!";
        return 0;
    }
    for (int i=0;i<s.length();i++)
    {
        if(sm.find(s[i])==sm.end()){
            sm[s[i]]=1;
        }else{
            sm[s[i]]++;
        }
    }
    if(checkAnagram(t,sm)) cout<<"IS ANAGRAM";
    else cout<<"NOT ANAGRAM!!!";
    return 0;
}
