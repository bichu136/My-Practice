long long bubbleSort(int a[],int n){
  long long count=1; //i=0
  for (size_t i = 0; i < n-1; i++) {
    count+=2;//i < n-1;

    count+=1; //j=0    
    for (size_t j =0; j < n-i-1; j++) {
      count+=3; //j<n-i-1
      count+=2; //a[j]>a[j+1]
      if(a[j]>a[j+1]){
        int t=a[j];
        a[j]=a[j+1];
        a[j+1]=t;
        count+=4; //swap(a[j],a[j+1])
      }
      count+=1; //j++
      
    }
    count+=1;//j<n-i-1
    count+=1;//i++
  }
  count+=2; //i < n-1
  return count;
}
