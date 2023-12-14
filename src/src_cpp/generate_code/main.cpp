#include <unistd.h>

#include "swap_edges.hpp"


#include <iostream>
#include <vector>
using namespace std;

int main(int argc, char * argv[]) {
    ////////// Parser //////////
    int c;
    int delay_saving = 60;
    int delay_print = 1;
    int code_index = 1;
    char const * file_name = NULL;
    /////////////////////////////////////////
    // -s = the code is saved every -s seconds
    // -p = the score is printed every -p seconds
    // -i = when not used -> new codes are generated with the configuration model
    // -i = when used -> the code is taken in  the -i file
    // -n = with -i: the code -n code is taken in the -i file
    // -n = with or without -i: the random seed depends on it. In particular when launched on slurm, we don't get the same codes with two processors.
    /////////////////////////////////////////
    while((c = getopt(argc, argv, "s:p:i:n:"))!= -1){
	switch(c) {
	case 's':
	    if(optarg) delay_saving = stoi(optarg);
	    break;
	case 'p':
	    if(optarg) delay_print = stoi(optarg);
	    break;
	case 'i':
	    if(optarg) file_name = optarg;
	    break;
	case 'n':
	    if(optarg) code_index = stoi(optarg);
	    break;
	}
    }

    
    if (optind == argc) {
	throw invalid_argument("No output directory given");
    }
    char const * dir_name = argv[optind];
    ////////////////////////////


    
    srand (time(NULL) + 123 * code_index);
    int n = 60;
    int m = 50;
    int dv = 5;
    int dc = 6;
    for (int code = 0; code < 1000; ++code) {
	Ccode* ccode;
	if (file_name != NULL) {
	    ccode = new Ccode(file_name, code_index);
	}
	else {
	    ccode = new Ccode(n,m,dv,dc);
	}
	cout << "------------------------------------------------\nc++ implem \t n = ";
	cout << ccode->n << ", m = " << ccode->m;
	cout << ", dv = " << ccode->dv << ", dc = " << ccode->dc << "\n";
	cout << "\nCode id = " << ccode->id << "\n";
	string file_name0 = dir_name + ccode->id + ".code";
	const char * file_name = file_name0.c_str();
	remove_cycles(ccode, 1000000000, file_name, delay_saving, delay_print);
	ccode->to_file("ccode/" + to_string(n) + "_" + to_string(m) + to_string(dv) + "_" + to_string(dc) + ".code");
	delete ccode;
    }
    
    return 0;
}
