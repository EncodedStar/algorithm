#ifndef WRAP_H
#define WRAP_H
#include <stdio.h>
#include <iostream>

extern "C"
{
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
}

using namespace std;

class CTest
{
	public:
		CTest()
		{
			this->i = 1;
			this->d = 1.1;
		}
		void print()
		{
			}
		void Set()
		{
			this->i = 2;
			this->d = 2.2;
		}
	private:
		int i;
		double d;
};
#endif

