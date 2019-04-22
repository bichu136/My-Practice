void shakeSort(int a[],int n){

	int Left = 0;
	int Right = n - 1;
	int k = 0;
	while (Left < Right)
	{
		for (int i = Left; i < Right; i++)
		{
			if (a[i] > a[i + 1])
			{
				int t=a[i];
				a[i]=a[i+1];
				a[i+1]=t;
				k = i;
			}
		}
		Right--;
		for (int i = Right; i > Left; i--)
		{
			if (a[i] < a[i - 1])
			{
				int t=a[i];
				a[i]=a[i-1];
				a[i-1]=t;
				k = i;
			}
		}
		Left++;
	}
}
