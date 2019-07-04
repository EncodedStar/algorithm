#include <iostream>  
#include <string.h>  
#include <unistd.h>
using namespace std;  
   
extern "C"  
{  
 #include "lua.h"  
 #include "lauxlib.h"  
 #include "lualib.h"  
}  
int test(char* fun,int arg1,int arg2)
{
	//1.创建Lua状态  
	lua_State *L = luaL_newstate();  
	if (L == NULL)  
	{  
	    return 0;  
	}  
	//2.加载Lua文件  
	int bRet = luaL_loadfile(L,"hello.lua");  
	if(bRet)  
	{  
	    cout<<"load file error"<<endl;  
	    return 0;  
	}  
	//3.运行Lua文件  
	bRet = lua_pcall(L,0,0,0);  
	if(bRet)  
	{  
	    cout<<"pcall error"<<endl;  
	    return 0;  
	}  
	lua_getglobal(L,fun);        // 获取函数，压入栈中  
	lua_pushnumber(L,arg1);          // 压入第一个参数  
	lua_pushnumber(L,arg2);          // 压入第二个参数  
	int iRet= lua_pcall(L, 2, 1, 0);// 调用函数，调用完成以后，会将返回值压入栈中，2表示参数个数，1表示返回结果个数。  
	if (iRet)                       // 调用出错  
	{  
	    const char *pErrorMsg = lua_tostring(L, -1);  
	    cout << pErrorMsg << endl;  
	    lua_close(L);  
	    return 0;  
	}  
	if (lua_isnumber(L, -1))        //取值输出  
	{  
	    double fValue = lua_tonumber(L, -1);  
	    cout << "Result is " << fValue << endl;  
	}  
	lua_close(L);
	return 0;
}
int main(int argc,char *argv[])  
{  
	int select = 0;
	while(1)
	{
		test("add",select,select+1);
		++select;
		sleep(2);
	}
	
	return 0;  
}

