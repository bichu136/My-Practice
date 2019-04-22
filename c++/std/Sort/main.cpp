#include<iostream>
#include<ctime>
#include<cstring>
#include"Sort.h"
using namespace std;
typedef void (*Sort)(int *a,int n);
void testSort(Sort yourFunction,int *a,int n,string name){
    int *b= new int[n];
    clock_t start,end;
    memcpy(a,b,sizeof(int)*n);
    cout<<"Current Test:"<< name<<"\n";
    start=clock();
    yourFunction(b,n);
    end = clock();
    cout<<"Result: "<<double(end-start)/CLOCKS_PER_SEC<<"s\n";
}
int main(){
    srand(time(NULL));
    int n,*arr;
    clock_t start;
    clock_t end;
    cin>>n;
    arr=new int[n];
    for (int i = 0; i < n; i++)
    {
        //cin >> arr[i];
        int t;
        t=rand()%1000000000;
        arr[i]=t;
        cout<<arr[i]<<" ";
    }
    cout<<"\n";
    testSort(selectionSort,arr,n,"Selection Sort");
    testSort(insertionSort,arr,n,"Insertion Sort");
    testSort(binaryInsertionSort,arr,n,"Binary Insertion Sort");
    testSort(interchangeSort,arr,n,"Interchange Sort");
    testSort(bubbleSort,arr,n,"Bubble Sort");
    testSort(shakeSort,arr,n,"Shake Sort");
    testSort(quickSort,arr,n,"Quick Sort");
    testSort(mergeSort,arr,n,"Merge Sort");
    testSort(shellSort,arr,n,"Shell Sort");
    testSort(heapSort,arr,n,"Heap Sort");
    testSort(radixSort,arr,n,"Radix Sort");
    return 0;
}
