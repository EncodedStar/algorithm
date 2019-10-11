#include<stdio.h>
#include<map>

#ifdef __cplusplus
extern "C"{
#endif

void print();
void testCfun();

//初始化一些数据
void initData();
//在控制台上打印地图
void drawMap();
//向上移动
void moveUp();
//向左移动
void moveLeft();
//向下移动
void moveDown();
//向右移动
void moveRight();


#ifdef __cplusplus
}
#endif
