BUILD_DIR = ./build
DEST_DIR = ./bin
DEST_EXE_NAME = main

all: build
	cd $(BUILD_DIR);  make -j4
run:
	cd $(DEST_DIR); ./$(DEST_EXE_NAME)
clean:
	rm $(BUILD_DIR) -rf
build:
	mkdir $(BUILD_DIR);cd $(BUILD_DIR); cmake ..

#功能解释： 
#make clean //清空build文件夹 
#make build //在同级目录下新建build目录，生成makefile 
#make all/make //编译成可执行文件，在bin文件夹 
#make run //进入bin文件夹，运行可执行文件
#注意所有命令都在源文件目录下执行。一般make run用不到，因为可执行文件参数不一，反而直接在bin文件夹运行更方便。
