int rootOf(int i){
    return (i%2==0)? (i/2 - 1) : (i/2);
}
int childOf(int i,int index=1){
    return i*2+index;
}
void DeleteAt(int *t,int &Sz,int c){

    while(childOf(c,1)<Sz){
        if(childOf(c,2)>=Sz){
            t[c]=t[childOf(c,1)];
            c=childOf(c,1);
            break;
        }
        if(t[childOf(c,1)]>t[childOf(c,2)]){
            t[c]=t[childOf(c,1)];
            c=childOf(c,1);
            //cout<< "\n" <<t[c];
        }else{
            t[c]=t[childOf(c,2)];
            c=childOf(c,2);
        }
    }

    if(c!=Sz)
        t[c]=t[Sz];
    while((t[c]>t[rootOf(c)])&&(rootOf(c)>=0)){
        int tem=t[c];
        t[c]=t[rootOf(c)];
        t[rootOf(c)]=tem;
        c=rootOf(c);
    }
    Sz--;
}
void buildtree(int*a,int n){
    //int *t = new int[n];
    for (int i = 0; i < n; i++)
    {
        int x=a[i];
        int j=i;
        if(j>0){
            while(a[rootOf(j)]<a[j]&&j>0){
                a[j]=a[rootOf(j)];
                j=rootOf(j);
                a[j]=x;
            }
        }
        a[j]=x;
    }
    //return t;
    //--------------------------//
}
void heapSort(int *a ,int n){

    buildtree(a,n);
    int Sz=n-1;
    for (int i = 0; i < n; ++i)
    {
        int x=a[0];
        DeleteAt(a,Sz,0);
        a[Sz+1]=x;
    }
}
