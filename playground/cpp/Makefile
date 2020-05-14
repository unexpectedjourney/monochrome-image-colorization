build:
	g++ main.cpp -o main

build_opencv:
	g++ -std=c++11 `pkg-config --cflags --libs opencv4` main.cpp -o main

clear:
	rm -rf *.o main

all:
	build
	./main
	clear
