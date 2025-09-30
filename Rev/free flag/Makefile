.PHONY: all clean

CC := clang
CXX := clang++
SRC := main.c
DIST_DIR := dist

all: $(SRC)
	mkdir -pv $(DIST_DIR)
	$(CC) $(SRC) -O0 -o dist/chal.o

clean:
	rm -rf dist
