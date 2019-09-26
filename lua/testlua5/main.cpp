#include <iostream>
extern "C"
{
	#include "lua.h"
	#include "lualib.h"
	#include "lauxlib.h" 
}
#include <unistd.h>   
#include <sys/time.h> 
using namespace std;
//要想注册进 lua,
//函数的定义为 typedef int (*lua_CFunction)(lua_State* L)

int printHello(lua_State * l)
{
	lua_pushstring(l, "hello lua");
	//返回值代表向栈内压入的元素个数
	return 1;
}

int foo(lua_State * l)
{
	//获得 Lua 传递过来的参数个数
	int n = lua_gettop(l);
	if(n != 0)
	{
		//获得第一个参数
		int i = lua_tonumber(l, 1);
		//将传递过来的参数加一以后最为返回值传递回去
		lua_pushnumber(l, i+1);
		return 1;
	}
	return 0;
}

int add(lua_State * l)
{
	int n = lua_gettop(l);
	int sum = 0;
	for (int i=0;i<n;i++)
	{
		sum += lua_tonumber(l, i+1);
	}
	if(n!=0)
	{
		lua_pushnumber(l, sum);
		return 1;
	}
	return 0;
}

const luaL_Reg lib[]=
{
	{"printHello", printHello},
	{"foo", foo},
	{"add", add},
	{NULL, NULL}
};

int main(int argc, const char * argv[])
{
	//创建一个新的 Lua 环境
	lua_State * l= luaL_newstate();
	//打开需要的库
	luaL_openlibs(l);
	//统一注册 lua 中调用的函数
	const luaL_Reg* libf =lib;
	for (; libf->func; libf++)
	{
		//把 foo 函数注册进 lua,
		//第二个参数代表 Lua 中要调用的函数名称,
		//第三个参数就是 c 层的函数名称
		lua_register(l, libf->name, libf->func);
		//将栈顶清空
		lua_settop(l, 0);
	}
	//加载并且执行 lua 文件
	luaL_dofile(l, "test.lua");
	//关闭
	lua_close(l);
	return 0;
}
