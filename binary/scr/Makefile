TARGET      := mylibs.so                               
LDFLAGS     := -shared -fPIC
OBJS        := binary.o 
CC          := g++
CXXFLAGS    := -Wall -fPIC -I../include -std=gnu++11

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $(TARGET) $^ 
$(OBJS): binary.cpp
	$(CC) $(CXXFLAGS) -c binary.cpp -o binary.o
clean:                                                   
	rm -rf $(TARGET) $(OBJS)
