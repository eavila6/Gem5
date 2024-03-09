CC = gcc
CFLAGS= -g -W -Wall
SOURCE = mat-mult.CC
OBJ = $(SOURCE: .c=.o)
PROG = mat-mult

all:$(PROG)

mat-mult: $(OBJ)
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $< $(CFLAGS) -c-o $@

.PHONY: clean
clean:
	rm -f core *.o $(PROG)