#include <iostream>  
#include <string.h>  
using namespace std;  
   
   extern "C"  
   {  
	#include "lua.h"  
	#include "lauxlib.h"  
	#include "lualib.h"  
   }  
   int main(int argc,char *argv[])  
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

	   //4.读取变量  
	   lua_getglobal(L,"str");  
	   string str = lua_tostring(L,-1);  
	   cout<<"str = "<<str.c_str()<<endl;        //str = I am so cool~  

	   //5.读取table  
	   lua_getglobal(L,"tbl");   
	   lua_getfield(L,-1,"name");  
	   str = lua_tostring(L,-1);  
	   cout<<"tbl:name = "<<str.c_str()<<endl; //tbl:name = shun  

	   //6.读取函数  
	   lua_getglobal(L, "add");        // 获取函数，压入栈中  
	   lua_pushnumber(L, 10);          // 压入第一个参数  
	   lua_pushnumber(L, 20);          // 压入第二个参数  
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

	   //至此，栈中的情况是：  
	   //=================== 栈顶 ===================   
	   //  索引  类型      值  
	   //   4   int：      30   
	   //   3   string：   shun   
	   //   2   table:     tbl  
	   //   1   string:    I am so cool~  
	   //=================== 栈底 ===================   

	   //7.关闭state  
	   lua_close(L);  
	   return 0;  
}
