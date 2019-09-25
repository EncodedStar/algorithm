#include "lua.h"
#include "lualib.h"
#include "lauxlib.h" 
int main()
{
	lua_State *L = luaL_newstate();
	luaL_openlibs(L);
	luaL_dofile(L, "test.lua");
	lua_getglobal(L, "price");
	int price = lua_tointeger(L, -1);
	lua_getglobal(L, "teacher");
	char *teacher = lua_tostring(L, -1);
	printf("price = %d teacher %s\n", price , teacher);
	lua_pop(L, 2);
	return 0;
}
