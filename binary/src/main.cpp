#include <iostream>
#include <map>
#include <cstring>
#include "binary.h"
using namespace std;
 
int Str2Vector(const string& str, vector<string> &v, const char *p)
{
	v.clear();
	char *pTmp = strtok(const_cast<char *>(str.c_str()),p);
	cout << str << endl;
	while(NULL != pTmp)
	{
		cout << str << endl;
		v.push_back(pTmp);
		pTmp = strtok(NULL, p);
	}

	return v.size();
}
#pragma pack(4)  
struct Test1  
{
	char a;  
	float b;
	int c;
}; 
#pragma pack(1)  
struct Test2  
{
	char a;  
	float b;
	int c;
}; 
int lengthOfLongestSubstring(string s) {
	int n = s.length();
	map<char, int> Map_tmp;
	map<char, int>::iterator iter; 
	int i= 0, ans = 0;
	for(int j = 0; j<n; j++){
		if( (iter = Map_tmp.find(s[j])) != Map_tmp.end() ){
			i = max(i, iter->second);
		} 
		ans = max(ans, j-i+1);
		Map_tmp[(s[j])] = j+1;
	}
	return ans;
}

void Qsort(int arr[], int low, int high){
	if (high <= low) return;
	int i = low;
	int j = high+1;
	int key = arr[low];
	while(true)
	{
		while(arr[++i] < key)
		{
			if(i == high)
				break;
		}
		while(arr[--j] > key)
		{
			if(j == low)
				break;
		}
		if (i >= j) break;
		swap(arr[i],arr[j]);
	}
	swap(arr[low],arr[j]);
	Qsort(arr, low, j - 1);
	Qsort(arr, j + 1, high);
}
int main()
{
//	cout << myLib::count_binary(1) << endl;
//	cout << myLib::count_binary(9) << endl;
//	cout << myLib::toHex(26) << endl;
//	cout << myLib::toHex(-1) << endl;
//	for(auto a:myLib::int2VString(15))
//		cout << a << endl;
//	stringstream ss("012345678901234567890123456789012345678901234567890123456789");  
//	//错误用法  
//	const char* cstr2 = ss.str().c_str();  
//	cout << &cstr2 << endl;
//	//正确用法  
//	const string& str2 = ss.str();  
//	const char* cstr3 = str2.c_str();  
//	cout << &cstr3 << endl;
//	string s = "|ab|cd|efg|h|";
//	string t(s.c_str()) ;
//	vector<string> v;
//	Str2Vector(t, v, "|");
//	for(vector<string>::iterator it = v.begin(); it != v.end(); ++it)
//	{
//		cout << *it << endl;
//	}
//	cout << s << endl;
//	cout << t << endl;
//	cout << lengthOfLongestSubstring("abcabcbbcc") << endl;
	int a[] = {123123,1,3,23,3434,53,57, 68, 59, 52, 72, 28, 96, 33, 24};
	Qsort(a, 0, sizeof(a) / sizeof(a[0]) - 1);/*这里原文第三个参数要减1否则内存越界*/
	for(unsigned int i = 0; i < sizeof(a) / sizeof(a[0]); i++)
	{
		cout << a[i] << " ";
	}
	cout << endl;
}

