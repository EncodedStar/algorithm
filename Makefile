TARGET		:= out
OBJS		:= main.o binary.o
CC         	:= g++
DIR			:= .
CXXFLAG     := -Wall -I. -I.. -I$(DIR)/binary/include -ggdb -std=gnu++11  
LDFLAGS		:= -Wl,-rpath=../common -L../common 
LIBS		:= 
$(TARGET):$(OBJS) 
	$(CC) $(LDFLAGS) $^ $(LIBS) -o $(TARGET)
main.o: main.cpp
	$(CC) $(CXXFLAG) -c main.cpp -o main.o
binary.o: $(DIR)/binary/scr/binary.cpp
	$(CC) $(CXXFLAG) -c $(DIR)/binary/scr/binary.cpp -o binary.o
clean:  
	rm -rf $(TARGET) $(OBJS)
