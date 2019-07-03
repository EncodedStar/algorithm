#include<iostream>
#include"binary.h"

/************************************************** 
 *  * @file binary.cpp
 *  * @author EncodedStar
 *  * @date 2019.7.13
 *  * @function 计算n二进制的时候存在几个1
 ***************************************************/

namespace myLib
{
	int count_binary(int n) {
		int res = 0;
		while (n != 0) {
			n = n & (n - 1);
			res++;
		}
		return res;
	}
}

