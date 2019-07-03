#include <iostream>

void world();

#ifdef __cplusplus
extern "C" {  // 即使这是一个C++程序，下列这个函数的实现也要以C约定的风格来搞！
#endif

	void m_world()
	{
		world();
	}

#ifdef __cplusplus
}
#endif
