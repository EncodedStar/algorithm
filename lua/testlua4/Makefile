TARGET		:= E_luatest
OBJS		:= main.o 
CC			:= g++
DIR			:= .
CXXFLAG		:= -Wall -ggdb -std=gnu++11 -g 
LDFLAGS		:=  
LIBS		:= -lm -ldl /usr/local/lib/liblua.a 
$(TARGET):$(OBJS) 
	$(CC) $(LDFLAGS) $^ $(LIBS) -o $(TARGET)
main.o: main.cpp
	$(CC) $(CXXFLAG) -c main.cpp -o main.o
clean:  
	rm -rf $(TARGET) $(OBJS)
