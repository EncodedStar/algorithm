CC=gcc
CFLAGS=-Wall -std=gnu99

TARGET=start
SRCS = main.c \
  ./UserInformation.pb-c.c \
  ./protobuf-c/protobuf-c.c

INC = -I./ -I./protobuf-c

OBJS = $(SRCS:.c=.o)

$(TARGET):$(OBJS)
#	@echo TARGET:$@
#	@echo OBJECTS:$^
	$(CC) -o $@ $^

clean:
	rm -rf $(TARGET) $(OBJS)

%.o:%.c
	$(CC) $(CFLAGS) $(INC) -o $@ -c $<
