#include <iostream>
extern "C"
{
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h" 
}
using namespace std;
int func(lua_State *L);
static int Foo (lua_State *L);
int main()
{
	{
		lua_State *L = luaL_newstate();
		luaL_openlibs(L);
		luaL_dofile(L, "test.lua");
		lua_getglobal(L, "Func");
		lua_pushinteger(L, 100);
		lua_pushnumber(L, 3.14);
		lua_pushstring(L, "nzhsoft");
		lua_pcall(L, 3, 1, 0);
		int i = lua_tointeger(L, -1);
		printf("i = %d\n", i);
		lua_close(L);
	}
	{
		lua_State *L = luaL_newstate();
		luaL_openlibs(L);
		lua_register(L, "FFF", Foo);
		lua_register(L, "fff", func);
		luaL_dofile(L, "test.lua");
		lua_close(L);
	}
	return 0;
}

int func(lua_State *L)
{
	cout << "----fun----" << endl;
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

static int Foo (lua_State *L)
{
	cout << "---foo---" << endl;
	int n = lua_gettop(L); /* number of arguments */
	lua_Number sum = 0.0;
	int i;
	for (i = 1; i <= n; i++) {
		if (!lua_isnumber(L, i)) {
			lua_pushliteral(L, "incorrect argument");
			lua_error(L);
		}
		sum += lua_tonumber(L, i);
	}
	lua_pushnumber(L, sum/n); /* first result */
	lua_pushnumber(L, sum); /* second result */
	return 2; /* number of results */
}
