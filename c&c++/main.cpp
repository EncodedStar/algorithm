#include<iostream>
#include"test.h"
#include <iomanip>      // std::get_time
#include <ctime>        // struct std::tm
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;
#define WIDTH 8
#define HEIGHT 8

//定义地图数组，二维数组有两个维度，而地图也是二维的矩形
int map[HEIGHT][WIDTH] = {
	{0, 0, 1, 1, 1, 0, 0, 0},
	{0, 0, 1, 4, 1, 0, 0, 0},
	{0, 0, 1, 0, 1, 1, 1, 1},
	{1, 1, 1, 3, 0, 3, 4, 1},
	{1, 4, 0, 3, 2, 1, 1, 1},
	{1, 1, 1, 1, 3, 1, 0, 0},
	{0, 0, 0, 1, 4, 1, 0, 0},
	{0, 0, 0, 1, 1, 1, 0, 0} 
};

//人的位置，在二维地图中，我们可以用坐标表示一个人的位置，就好比经纬度
int x, y;

//箱子的个数，推箱子肯定要有箱子嘛。
int boxs;
//宏定义
int main(int argc, char *argv[]) {
	char direction;		//存储键盘按的方向 
	initData();			//初始化一些数据

	//开始游戏的循环，这里是个死循环，每按一次按钮循环一次
	while(1){
		//每次循环的开始清除屏幕
		//绘画地图
		drawMap();

		//判断，当boxs的数量0时，!0为真，然后走break跳出循环（结束游戏） 
		if(!boxs){
			break;
		}
		//键盘输入方向，这里使用getch，因为getch读取字符不会显示在屏幕上
		//direction = getch();
		cin >> direction;

		//用switch判断用户输入的方向
		switch(direction){
			case 'w':
				//按w时，调用向上移动函数
				moveUp();
				break;
			case 'a':
				//按a时，调用向左移动函数
				moveLeft(); 
				break;
			case 's':
				moveDown();
				break;
			case 'd':
				moveRight();
				break; 
		}
	}  
	//当跳出循环时，运行该语句，游戏结束
	printf("game over!\n");
	return 0;
}

#if 0
int main(void)
{
	/*调用C接口*/
	cout<<"start to call c function"<<endl;
	testCfun();
	cout<<"end to call c function"<<endl;
	struct std::tm when;
	std::cout << "Please, enter the time: ";
	std::cin >> get_time(&when,"%R"); 
	return 0;
}
#endif
