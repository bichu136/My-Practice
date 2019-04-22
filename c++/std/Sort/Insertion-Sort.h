void insertionSort(int a[],int n){
  for (int i = 1; i < n; i++) {
    int x=a[i];
    int j=i-1;
    for (j; j >=0; j--) {
      if(a[j]>x)
        a[j+1]=a[j];
      else
        break;
    }
    a[j+1]=x;
  }
}
