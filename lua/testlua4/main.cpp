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
/* 有参无返回值*/
int c_func1(lua_State *L)
{
	printf("c function\n");
	const char * str = lua_tostring(L, -1);
	int price = lua_tointeger(L, -2);
	printf("price = %d str = %s\n", price , str);
	printf("stack size = %d\n", lua_gettop(L));
	return 0;
}
void test1()
{
	lua_State *L = luaL_newstate();
	luaL_openlibs(L);

	//lua_pushcfunction(L, &func);
	//lua_setglobal(L, "func");
	lua_register(L, "c_func1", c_func1);

	luaL_dofile(L, "test.lua");
	lua_close(L);
}
/* 有参有返回值*/
int c_func2(lua_State *L)
{
	printf("c function\n");
	const char * str = lua_tostring(L, -1);
	int price = lua_tointeger(L, -2);
	printf("price = %d str = %s\n", price , str);
	printf("stack size = %d\n", lua_gettop(L));
	lua_pushinteger(L, price*2);
	char buf[1024];
	sprintf(buf, "good C&C++ study %s", str);
	lua_pushstring(L, buf);
	printf("stack size = %d\n", lua_gettop(L));
	return 2;
}
void test2()
{
	lua_State *L = luaL_newstate();
	luaL_openlibs(L);

	//lua_pushcfunction(L, &func);
	//lua_setglobal(L, "func");
	lua_register(L, "c_func2", c_func2);

	luaL_dofile(L, "test.lua");
	lua_close(L);
}
/*测试lua实现函数 */
void test3()
{
	lua_State *L = luaL_newstate();
	luaL_openlibs(L);
	luaL_dofile(L, "test.lua");
	lua_getglobal(L, "Func");
	lua_pushinteger(L, 100);
	lua_pushnumber(L, 3.14);
	lua_pushstring(L, "soft");
	lua_pcall(L, 3, 1, 0);
	int i = lua_tointeger(L, -1);
	printf("i = %d\n", i);
	lua_close(L);
}
void test4()
{
	lua_State *L = luaL_newstate();
	luaL_openlibs(L); //若无此, print 函数不可用。
	luaL_dofile(L, "test.lua");
	lua_getglobal(L, "Func2");
	lua_pcall(L, 0, 0, 0);
	lua_close(L);
}
void test5()
{

	cout << "start" << endl;
	lua_State *L = luaL_newstate();
	luaL_openlibs(L); //若无此, print 函数不可用。
	luaL_dofile(L, "test.lua");
	lua_getglobal(L, "l_sleep");
	lua_pushinteger(L, 5);
	lua_pcall(L, 1, 0, 0);
	lua_close(L);
	cout << "end" << endl;
}

int main()
{
	test5();
	return 0;
}
