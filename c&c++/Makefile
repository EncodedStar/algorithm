TARGET		:= exe
SRC			:= main.c
OBJS		:= main.o 
#CC			:= g++
CC			:= gcc
DIR			:= .
#CXXFLAG	:= -Wall -ggdb -std=gnu++11  
CXXFLAG		:= 
LDFLAGS		:=  
LIBS		:=  
$(TARGET):$(OBJS) 
	$(CC) $(LDFLAGS) $^ $(LIBS) -o $(TARGET)
$(OBJS):$(SRC)
	$(CC) $(CXXFLAG) -c $(SRC) -o $(OBJS)
clean:  
	rm -rf $(TARGET) $(OBJS)
