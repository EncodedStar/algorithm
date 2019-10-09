#include<iostream>
#include"test.h"
using namespace std;
int main(void)
{
	/*调用C接口*/
	cout<<"start to call c function"<<endl;
	testCfun();
	cout<<"end to call c function"<<endl;
	return 0;
}
