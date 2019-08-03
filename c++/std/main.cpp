#include<iostream>
using namespace std;

int HashFunc(int a){
    return a%100000;
}
int HashCount(int a,int i){
    return (HashFunc(a)+i*i)%100000;
}
int main(){
int* HashTable[100000];
    for (int i = 0; i < 100000; ++i)
    {
        HashTable[i]=NULL;
    }
    int c,t;

    cin>>c;
    while(c){
        switch(c)
        {
        case 1:
            {
            cin>>t;
                int i=0;
                while(HashTable[HashCount(t,i)]){
                    i++;
                }
                HashTable[HashCount(t,i)]= new int; *HashTable[HashCount(t,i)]=t;
            }
            break;
        case 2:
            {
            cin>>t;
            int j=0;
            int f=0;
            while(HashTable[HashCount(t,j)]){
                if(*HashTable[HashCount(t,j)]==t){ cout<<1; f=1; break;}
                j++;
            }
            if(f==0){cout<<0;}
            cout<<"\n";
        }
        break;
        }
        cin>>c;
    }
    return 0;
}
