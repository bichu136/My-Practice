void bubbleSort(int a[],int n){
  for (size_t i = 0; i < n-1; i++) {

    for (size_t j =0; j < n-i-1; j++) {
      if(a[j]>a[j+1]){
        int t=a[j];
        a[j]=a[j+1];
        a[j+1]=t;
      }
    }
  }
}
