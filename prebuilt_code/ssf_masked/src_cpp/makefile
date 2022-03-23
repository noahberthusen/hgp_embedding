CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O3

main: main.o decoder.o generator.o mat.o qcode.o write_result.o generate_id.o input_params.h flip.o
	$(CXX) $(CXXFLAGS) -o main main.o decoder.o generator.o mat.o qcode.o write_result.o generate_id.o flip.o

main.o: main.cpp qcode.h decoder.h write_result.h mat.h generator.h decoder.h generate_id.h input_params.h flip.h
	$(CXX) $(CXXFLAGS) -c main.cpp

mat.o: mat.h input_params.h
	$(CXX) $(CXXFLAGS) -c mat.cpp

qcode.o: qcode.cpp qcode.h mat.h input_params.h
	$(CXX) $(CXXFLAGS) -c qcode.cpp

flip.o: flip.cpp flip.h mat.h input_params.h
	$(CXX) $(CXXFLAGS) -c flip.cpp

decoder.o: decoder.cpp decoder.h generator.h input_params.h
	$(CXX) $(CXXFLAGS) -c decoder.cpp

generator.o: generator.cpp generator.h mat.h input_params.h
	$(CXX) $(CXXFLAGS) -c generator.cpp

write_result.o: write_result.cpp write_result.h qcode.h input_params.h
	$(CXX) $(CXXFLAGS) -c write_result.cpp

generate_id.o: generate_id.cpp generate_id.h input_params.h
	$(CXX) $(CXXFLAGS) -c generate_id.cpp

clean:
	rm -rf *.o
