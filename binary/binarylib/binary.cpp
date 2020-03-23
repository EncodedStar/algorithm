#include"binary.h"
namespace myLib
{

/************************************************** 
 *  * @file binary.cpp
 *  * @author EncodedStar
 *  * @date 2019.7.3
 *  * @function 计算n二进制的时候存在几个1
 ***************************************************/
	int count_binary(int n) {
		int res = 0;
		while (n != 0) {
			n = n & (n - 1);
			res++;
		}
		return res;
	}

/************************************************** 
 *  * @file binary.cpp
 *  * @author EncodedStar
 *  * @date 2019.7.5
 *  * @function 16进制打印
 ***************************************************/
	std::string toHex(int num) {
		if (num == 0) return "0";
		std::string hex = "0123456789abcdef", ans = "";
		while(num && ans.size() < 8){
			ans = hex[num & 0xf] + ans;
			num >>=  4; 
		}
		return ans;
	}

/************************************************** 
 *  * @file binary.cpp
 *  * @author EncodedStar
 *  * @date 2019.7.5
 *  * @function int转化string and vector<string>
 ***************************************************/
	 std::string int2String(int n) {
		std::stringstream tmpss;
		std::string tmps;
		tmpss.clear();
		tmpss << n;
		tmpss >> tmps;
		tmpss.str("");
		return tmps;
	 }
	 vector<string> int2VString(int n) {
		 vector<string> tmpv;
		 for(int i = 1; i <= n; i++)
		 {
			tmpv.push_back(int2String(i));
		 }
		 return tmpv;
	 }


/************************************************** 
 *  * @file binary.cpp
 *  * @author EncodedStar
 *  * @date 2020.3.23
 *  * @function 开平方
 ***************************************************/
	float Q_rsqrt( float number )
	{
	    long i;
	    float x2, y;
	    const float threehalfs = 1.5F;
	
	    x2 = number * 0.5F;
	    y  = number;
	    i  = * ( long * ) &y; // evil floating point bit level hacking
	    i  = 0x5f3759df - ( i >> 1 );  // what the fuck? 
	    y  = * ( float * ) &i;
	    y  = y * ( threehalfs - ( x2 * y * y ) );  // 1st iteration 
	    // 2nd iteration, this can be removed
	    //     // y  = y * ( threehalfs - ( x2 * y * y ) ); 
	    return y;
	}

}

