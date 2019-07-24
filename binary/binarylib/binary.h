#ifndef BINARY_H
#define BINARY_H
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
using namespace std;

namespace myLib
{
	int count_binary(int n);
	std::string toHex(int num);
	std::string int2String(int n);
	vector<string> int2VString(int n);
}
#endif
