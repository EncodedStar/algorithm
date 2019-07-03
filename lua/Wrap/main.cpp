#include "Wrap.h"
#include <unistd.h>
using namespace std;
 
void LuaLayer(int select)
{
	lua_State* l = luaL_newstate();
	int ret = 0;
	luaL_openlibs(l);
	ret = luaL_dofile(l,"dispatcher.lua");
	lua_getglobal(l,"SelectFunc");
	CTest b;
	lua_pushlightuserdata(l,&b);
	ret = lua_pcall(l,1,1,0);
	b.print();
	lua_close(l);
}

int main()
{
	int select = 0;
	while(1)
	{
		LuaLayer(select%2);
		++select;
		sleep(2);
	}
}

