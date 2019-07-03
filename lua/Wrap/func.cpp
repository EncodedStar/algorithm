#include "Wrap.h"

static int hello(lua_State* L)
{
	CTest* b = (CTest*)lua_touserdata(L,1);
	b->print();
	b->Set();
	return 1;
}

static int world(lua_State* L)
{
	cout<<"World"<<endl;
	return 1;
}

static const struct luaL_Reg l_lib[] = 
{
	{"hello",hello},
	{"world",world},
	{NULL,NULL}
};

extern "C" int luaopen_func(lua_State* L)
{
	luaL_openlib(L,"func",l_lib,0);
	return 1;
}

