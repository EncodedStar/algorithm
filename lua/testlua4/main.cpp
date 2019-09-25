#include <iostream>
extern "C"
{
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h" 
}
#include <unistd.h>   
#include <sys/time.h> 
int main()
{
	while(true)
	{
		lua_State *L = luaL_newstate();
		luaL_openlibs(L);
		luaL_dofile(L, "test.lua");
		lua_getglobal(L, "price");
		int price = lua_tointeger(L, -1);
		lua_getglobal(L, "teacher");
		const char *teacher = lua_tostring(L, -1);
		printf("price = %d teacher %s\n", price , teacher);
		sleep(1);
		lua_pop(L, 2);
	}
	return 0;
}
