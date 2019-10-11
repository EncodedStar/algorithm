#include<stdio.h>
#include"test.h"


//定义地图数组，二维数组有两个维度，而地图也是二维的矩形

#define WIDTH 8
#define HEIGHT 8

//定义地图数组，二维数组有两个维度，而地图也是二维的矩形
extern int map[HEIGHT][WIDTH];
//人的位置，在二维地图中，我们可以用坐标表示一个人的位置，就好比经纬度
extern int x;
extern int y;

//箱子的个数，推箱子肯定要有箱子嘛。
extern int boxs;


void print()
{
	printf("rainy days\n");
}

void testCfun()
{
	printf("I am c fun\n");
	return;
}

void initData(){
	int i, j;

	//加载数据时让用户等待，一般情况加载数据比较快
	printf("游戏加载中，请稍后........."); 

	//遍历地图中的数据
	for(i = 0; i < HEIGHT; i++){
		for(j = 0; j < WIDTH; j++){
			//遍历到2（人）时，记录人的坐标。x， y是前面定义的全局变量
			if(map[i][j] == 2){
				x = j;
				y = i;
			} 
			//遍历到3时，箱子的数目增加。boxs是前面定义的全局变量 
			if(map[i][j] == 3){
				boxs++;
			}
		}
	} 
}
	
void drawMap(){
	int i, j;
	for(i = 0; i < WIDTH; i++){
		for(j = 0; j < HEIGHT; j++){
			switch(map[i][j]){
				case 0:
					printf(" ");
					break;
				case 1:
					printf("@");
					break;
				case 2:
					printf("$");
					break;
				case 3:
					printf("o");
					break;
				case 4:
					printf("O");
					break;
				case 5:
					printf("*");
					break; 
			}
		}
		printf("\n");
	}
}

void moveUp(){
	//定义变量存放人物上方的坐标
	int ux, uy; 

	//当上方没有元素时，直接return	（其实人不可能在边缘）
	if(y == 0){
		return;
	}

	//记录上方坐标，x为横，y为纵，所有ux = x, uy = y - 1;
	ux = x;
	uy = y - 1; 

	//上方为已完成的箱子
	if(map[uy][ux] == 5){
		return;
	} 
	//假设上方为墙，直接return，这个和上面的判断可以合在一起，这里为了看清楚分开写 
	if(map[uy][ux] == 1){
		return;
	}

	//假设上方为箱子
	if(map[uy][ux] == 3){
		//判断箱子上方是否为墙 
		if(map[uy - 1][ux] == 1){
			return;
		}

		//判断箱子上方是否为终点
		if(map[uy - 1][ux] == 4){
			//将箱子上面内容赋值为5★ 
			map[uy - 1][ux] = 5;
			map[uy][ux] = 0;

			//箱子的数目减1	
			boxs--; 
		}else{
			//移动箱子
			map[uy - 1][ux] = 3;
		}
	}
	//当上面几种return的情况都没遇到，人肯定会移动，移动操作如下
	map[y][x] = 0;
	map[uy][ux] = 2;
	//更新人的坐标
	y = uy; 
} 

void moveLeft(){
	//定义变量存放人物左边的坐标
	int lx, ly; 

	//当左边没有元素时，直接return	
	if(x == 0){
		return;
	}

	//记录左边坐标
	lx = x - 1;
	ly = y; 

	//左边为已完成方块
	if(map[ly][lx] == 5){
		return;
	} 

	//假设左边为墙，直接return 
	if(map[ly][lx] == 1){
		return;
	}

	//假设左边为箱子
	if(map[ly][lx] == 3){
		//判断箱子左边是否为墙 
		if(map[ly][lx - 1] == 1){
			return;
		}

		//判断箱子左边是否为球
		if(map[ly][lx - 1] == 4){
			//将箱子左边内容赋值为5★ 
			map[ly][lx - 1] = 5;
			map[ly][lx] = 0;

			//箱子的数目减1 
			boxs--; 
		}else{
			//移动箱子 
			map[ly][lx - 1] = 3; 
		}
	}
	map[y][x] = 0;
	map[ly][lx] = 2;
	x = lx; 
}
void moveDown(){
	//定义变量存放人物下方的坐标
	int dx, dy; 

	//当下方没有元素时，直接return	
	if(y == HEIGHT - 1){
		return;
	}

	//记录下方坐标
	dx = x;
	dy = y + 1; 

	//下方为已完成方块
	if(map[dy][dx] == 5){
		return;
	} 

	//假设下方为墙，直接return 
	if(map[dy][dx] == 1){
		return;
	}

	//假设下方为箱子
	if(map[dy][dx] == 3){
		//判断箱子下方是否为墙 
		if(map[dy + 1][dx] == 1){
			return;
		}

		//判断箱子下方是否为球
		if(map[dy + 1][dx] == 4){
			//将箱子下面内容赋值为5★ 
			map[dy + 1][dx] = 5;
			map[dy][dx] = 0;

			//箱子的数目减1 
			boxs--; 
		}else{
			//移动箱子
			map[dy + 1][dx] = 3; 
		}
	}
	map[y][x] = 0;
	map[dy][dx] = 2;
	y = dy; 
}
void moveRight(){
	//定义变量存放人物右边的坐标
	int rx, ry; 

	//当右边没有元素时，直接return	
	if(x == WIDTH - 1){
		return;
	}

	//记录右边坐标
	rx = x + 1;
	ry = y; 

	//右边为已完成方块
	if(map[ry][rx] == 5){
		return;
	} 

	//假设右边为墙，直接return 
	if(map[ry][rx] == 1){
		return;
	}

	//假设右边为箱子
	if(map[ry][rx] == 3){
		//判断箱子右边是否为墙 
		if(map[ry][rx + 1] == 1){
			return;
		}

		//判断箱子左边是否为球
		if(map[ry][rx + 1] == 4){
			//将箱子右边内容赋值为5★ 
			map[ry][rx + 1] = 5;
			map[ry][rx] = 0;

			//箱子的数目减1 
			boxs--; 
		}else{
			//移动箱子 
			map[ry][rx + 1] = 3; 
		}
	}
	map[y][x] = 0;
	map[ry][rx] = 2;
	x = rx; 
}

