#include <iostream>

#ifdef __cplusplus
extern "C" {               // 告诉编译器下列代码要以C链接约定的模式进行链接
	#endif
	void hello();
	#ifdef __cplusplus
}
#endif

int main()
{
	hello();
	return 0;
}
