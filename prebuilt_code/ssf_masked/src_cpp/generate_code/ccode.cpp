#include "ccode.hpp"
#include "../generate_id.h"

#include <vector>
#include <algorithm>
#include <fstream>

using namespace std;


Ccode::Ccode(int N, int M, int DV, int DC): n(N), m(M), dv(DV), dc(DC), id("swac_" + generate_id()) {
    bit_nbhd = new mat<int>(n,dv,0);
    check_nbhd = new mat<int>(m,dc,0);

    vector<int> half_edges(n*dv);
    for (unsigned i=0; i<half_edges.size(); ++i)
	half_edges[i] = i;
    random_shuffle(half_edges.begin(), half_edges.end() );

    for (unsigned i = 0; i < half_edges.size(); ++i){
	int v = i/dv;
	int v_nbhd_no = i%dv;
	int c = half_edges[i]/dc;
	int c_nbhd_no = half_edges[i]%dc;
	(*bit_nbhd)(v, v_nbhd_no) = c;
	(*check_nbhd)(c, c_nbhd_no) = v;
    }
    
    // for	(int i = 0; i < n; ++i){
    // 	for (int j = 0; j < dv; ++j)
    // 	    cout << (*bit_nbhd)(i,j) << " ";
    // 	cout << "\n";
    // }
    
    // for	(int i = 0; i < m; ++i){
    // 	for (int j = 0; j < dc; ++j)
    // 	    cout << (*check_nbhd)(i,j) << " ";
    // 	cout << "\n";
    // 	    }
}

// Copy/paste from qcode.cpp
string get_param(ifstream& file,const string& param_label){
    string tmp;
    if (!getline(file,tmp,',')) 
	throw invalid_argument("End of file");
    if (tmp.compare(param_label)) {
	throw invalid_argument("Bad file format read codes");
    }
    getline(file,tmp,'\n');
    return tmp;
}


// Copy/paste from qcode.cpp
void get_matrix(mat<int>* matrix_ptr, ifstream& file, const string& matrix_label, int no_rows, int no_cols){
    string tmp;
    getline(file,tmp,'\n');
    if (tmp.compare(matrix_label)) {
	throw invalid_argument("Bad file format read codes2");
    }

    for (int i = 0; i < no_rows; ++i){
	for (int j = 0; j < no_cols; ++j){
	    getline(file,tmp,',');
	    (*matrix_ptr)(i,j) = stoi(tmp);
	}
	getline(file,tmp,'\n');
    }
}



Ccode::Ccode(char const * file_name, int code_index){
    
    ifstream file;
    file.open(file_name);
    if (file.fail()){
	throw invalid_argument("File does not exist");
    }

    bit_nbhd = new mat<int>(0,0,0);
    check_nbhd = new mat<int>(0,0,0);
    
    for (int i = 0; i < code_index; ++i) {
	delete bit_nbhd;
	delete check_nbhd;
	
	n = stoi(get_param(file,"n"));
	m = stoi(get_param(file,"m"));
	dv = stoi(get_param(file,"dv"));
	dc = stoi(get_param(file,"dc"));
	
	id = get_param(file,"id");
	
	bit_nbhd = new mat<int>(n,dv,0);
	check_nbhd = new mat<int>(m,dc,0);
	get_matrix(bit_nbhd, file, "bit_nbhd", n, dv);
	get_matrix(check_nbhd, file, "check_nbhd", m, dc);
    }
}

Ccode::Ccode(const Ccode& ccode): n(ccode.n), m(ccode.m), dv(ccode.dv), dc(ccode.dc), id(ccode.id){
    throw invalid_argument("Not implemented: trying to copy a ccode");
}

Ccode Ccode::operator=(const Ccode&){
    throw invalid_argument("Not implemented: trying to copy a ccode");
}


Ccode::~Ccode(){
    delete bit_nbhd;
    delete check_nbhd;
}

void Ccode::to_file(string file_name) {
    ofstream file(file_name, ios::app);
    file << "n," << n << "\n";
    file << "m,"<< m << "\n";
    file << "dv," << dv << "\n";
    file << "dc," << dc << "\n";
    file << "id," << id << "\n";
    file << "bit_nbhd\n";
    for (int v = 0; v < n; v++) {
        for (int i = 0; i < dv; i++)
            file << (*bit_nbhd)(v,i) << ",";
	file << "\n";
    }
    file << "check_nbhd\n";
    for (int c = 0; c < m; c++) {
        for (int j = 0; j < dc; j++)
            file << (*check_nbhd)(c,j) << ",";
	file << "\n";
    }
    file.close();
}


void replace(int* v, int a, int b) {
    int i = 0;
    while (true) {
	if (v[i] == a) {
	    v[i] = b;
	    return;
	}
	i++;
    }
}



void Ccode::swap_edges(int v1, int c1, int v2, int c2){
    replace((*bit_nbhd)(v1), c1, c2);
    replace((*bit_nbhd)(v2), c2, c1);
    replace((*check_nbhd)(c1), v1, v2);
    replace((*check_nbhd)(c2), v2, v1);
}


int Ccode::get_bit_nbhd(int v, int i) const{
    return (*bit_nbhd)(v,i);
}

int Ccode::get_check_nbhd(int c, int i) const{
    return (*check_nbhd)(c,i);
}

