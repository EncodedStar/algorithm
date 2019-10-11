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

//�����ͼ���飬��ά����������ά�ȣ�����ͼҲ�Ƕ�ά�ľ���
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

//�˵�λ�ã��ڶ�ά��ͼ�У����ǿ����������ʾһ���˵�λ�ã��ͺñȾ�γ��
int x, y;

//���ӵĸ����������ӿ϶�Ҫ�������
int boxs;
//�궨��
int main(int argc, char *argv[]) {
	char direction;		//�洢���̰��ķ��� 
	initData();			//��ʼ��һЩ����

	//��ʼ��Ϸ��ѭ���������Ǹ���ѭ����ÿ��һ�ΰ�ťѭ��һ��
	while(1){
		//ÿ��ѭ���Ŀ�ʼ�����Ļ
		//�滭��ͼ
		drawMap();

		//�жϣ���boxs������0ʱ��!0Ϊ�棬Ȼ����break����ѭ����������Ϸ�� 
		if(!boxs){
			break;
		}
		//�������뷽������ʹ��getch����Ϊgetch��ȡ�ַ�������ʾ����Ļ��
		//direction = getch();
		cin >> direction;

		//��switch�ж��û�����ķ���
		switch(direction){
			case 'w':
				//��wʱ�����������ƶ�����
				moveUp();
				break;
			case 'a':
				//��aʱ�����������ƶ�����
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
	//������ѭ��ʱ�����и���䣬��Ϸ����
	printf("game over!\n");
	return 0;
}

#if 0
int main(void)
{
	/*����C�ӿ�*/
	cout<<"start to call c function"<<endl;
	testCfun();
	cout<<"end to call c function"<<endl;
	struct std::tm when;
	std::cout << "Please, enter the time: ";
	std::cin >> get_time(&when,"%R"); 
	return 0;
}
#endif
