CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2

all: main

main: main.o ccode.o swap_edges.o timer.o mat.o generate_id.o
	$(CXX) -o $@ $^

main.o: swap_edges.hpp

ccode.o: ccode.hpp ../mat.h ../generate_id.h

swap_edges.o: swap_edges.hpp ccode.hpp ../mat.h timer.hpp

timer.o: timer.hpp

mat.o: ../mat.cpp ../mat.h ../input_params.h
	$(CXX) $(CXXFLAGS) -o $@ -c $<

generate_id.o: ../generate_id.cpp ../generate_id.h ../input_params.h
	$(CXX) $(CXXFLAGS) -o $@ -c $<

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -o $@ -c $<

clean:
	rm -rf *.o
