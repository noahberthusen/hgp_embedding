#include "qcode.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <math.h>
#include "write_result.h"

using namespace std;

#define COLUMN_NAMES_FOR_SIMULATION_DESCRITPION "algo,dv,dc,nv,nc,code_id,p_phys,p_mask"
#define COLUMN_NAMES_FOR_SIMULATION_RESULTS "no_test,no_success,no_stop"
#define COLUMN_NAMES_FOR_EXTRAS "p_log"
// DO NOT modify SEPARATOR
#define SEPARATOR "\t\t"
#define FIRST_LINE COLUMN_NAMES_FOR_SIMULATION_DESCRITPION SEPARATOR COLUMN_NAMES_FOR_SIMULATION_RESULTS SEPARATOR COLUMN_NAMES_FOR_EXTRAS


Result::Result(int algo,int dv,int dc,int n,int m,string code_id,double p_phys,double p_mask,int no_test,int no_success,int no_stop) : 
algo(algo),dv(dv),dc(dc),n(n),m(m),code_id(code_id),p_phys(p_phys),p_mask(p_mask),no_test(no_test),no_success(no_success),no_stop(no_stop)
{
}


Result::Result(string line)
{
  stringstream stream(line);
  string tmp;
  
  getline(stream,tmp,',');
  algo = stoi(tmp);
  getline(stream,tmp,',');
  dv = stoi(tmp);
  getline(stream,tmp,',');
  dc = stoi(tmp);
  getline(stream,tmp,',');
  n = stoi(tmp);
  getline(stream,tmp,',');
  m = stoi(tmp);
  getline(stream,tmp,',');
  code_id = tmp;
  getline(stream,tmp,',');
  p_phys = stod(tmp);
  getline(stream,tmp,'\t');
  p_mask = stod(tmp);
  getline(stream,tmp,'\t');
  getline(stream,tmp,',');
  no_test = stoi(tmp);
  getline(stream,tmp,',');
  no_success = stoi(tmp);
  getline(stream,tmp,',');
  no_stop = stoi(tmp);
}


// # r1 and r2 are objects of the class Result
// # This function tries to combine the results r1 and r2.
// # It is possible to combine r1 and r2 when r1.algo == r2. algo and r1.dv == r2.dv and r1.dc == r2.dv and r1.n == r2.n and r1.m == r2.m and r1.code_id == r2.code_id and r1.p_phys == r2.p_phys
// # It returns None when it
bool compare_proba(double p1, double p2) {
  return (fabs(p1-p2) < EPSILON);
}

bool Result::test_combine_res(Result r) {
    return (algo == r.algo && dv == r.dv &&
	  dc == r.dc && n == r.n &&
	  m == r.m && code_id.compare(r.code_id) == 0 && 
	    compare_proba(p_phys,r.p_phys) && compare_proba(p_mask,r.p_mask));
}

// Be carefull: use this function only if test_combine_res(r1, r2) is true
Result Result::combine_res(Result r) {
  int new_no_test = no_test + r.no_test;
  int new_no_success = no_success + r.no_success;
  int new_no_stop = no_stop + r.no_stop;
  return Result(algo,dv,dc,n,m,code_id,p_phys,p_mask,new_no_test,new_no_success,new_no_stop);
}


string Result::to_line() {
  double p_log = double(no_success) / no_test;
  stringstream sstream;
  sstream << algo << ',' << dv << ',' << dc << ',' << n << ',' << m << ',' << code_id << ',' << p_phys << ',' << p_mask
    << SEPARATOR << no_test << ',' << no_success << ',' << no_stop
    << SEPARATOR << p_log << "\n";
  return sstream.str();
}

void Result_ensemble::add_result(Result r){
    for (vector<Result>::iterator it=result_vector.begin(); it!=result_vector.end(); ++it) {
	if (it->test_combine_res(r)) {
	    *it = it->combine_res(r);
	    return;
	}
    }
    result_vector.push_back(r);
}


void Result_ensemble::add_result(int algo,int dv,int dc,int n,int m,std::string code_id,double p_phys,double p_mask,int no_test,int no_success,int no_stop){
    Result r(algo, dv, dc, n, m, code_id, p_phys, p_mask, no_test, no_success, no_stop);
    add_result(r);
}

// Hypothesis: the file exists
void Result_ensemble::add_file(const string file_name){
    ifstream file(file_name);
    string line;
    getline(file,line,'\n');
    if (line != FIRST_LINE)
	throw std::invalid_argument("Bad file format write result");
    while(getline(file,line,'\n')){
	add_result(Result(line));
    }
    file.close();
}

// Deletes file_name
void Result_ensemble::to_file(const string file_name){
    vector<string> line_vector(result_vector.size());
    for (unsigned i = 0; i < result_vector.size(); ++i)
	line_vector[i] = result_vector[i].to_line();

    sort(line_vector.begin(), line_vector.end());
    const string tmp_file_name = file_name + ".tmp";
    ofstream file(tmp_file_name, ios::out | ios::trunc);
    file << FIRST_LINE << "\n";
    for (vector<string>::iterator it=line_vector.begin(); it!=line_vector.end(); ++it)
	file << *it;
    file.close();
    rename(tmp_file_name.c_str(),file_name.c_str());   
}



// int main() {
//   Result_ensemble res_ens;
  
//   res_ens.add_file("1.res");
//   res_ens.add_result(-1,1,2,3,4,"id",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id2",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id3",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id4",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id5",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id2",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id3",0.03422,100,26,74);
//   res_ens.add_result(-1,1,2,3,4,"id4",0.03422,100,26,90);
//   res_ens.add_result(-1,1,2,3,4,"id5",0.03422,100,26,74);
//   res_ens.add_file("2.res");
//   res_ens.to_file("1.res");
  
//   return 0;
// }



// // Creates a file whose lines are stored in lines_vector
// // Be carefull 
// void create_file(const string file_name, vector<string> line_vector) {
//   sort(line_vector.begin(), line_vector.end());
//   const string tmp_file_name = file_name + ".tmp";
//   ofstream file(tmp_file_name, ios::out | ios::trunc);
//   file << FIRST_LINE << "\n";
//   for (vector<string>::iterator it=line_vector.begin(); it!=line_vector.end(); ++it)
//     file << *it;
//   file.close();
//   rename(tmp_file_name.c_str(),file_name.c_str());
// }


// // ############# To store the results during simulations #############
// void save_new_res(string file_name, int algo, int dv,int dc,int n,int m,string code_id,double p_phys,int no_test,int no_success,int no_stop) {
//     Result r(algo, dv, dc, n, m, code_id, p_phys, no_test, no_success, no_stop);
    
//     ifstream file(file_name);
//     string line;
//     vector<string> line_vector;
//     bool done = false;

//     if (file.fail()){
// 	vector<string> empty_vector;
// 	create_file(file_name, empty_vector);
// 	file = ifstream(file_name);
//     }
  
//     getline(file,line,'\n');
//     if (line != FIRST_LINE)
// 	throw std::invalid_argument("Bad file format write result");
//     while(getline(file,line,'\n')){
// 	Result r1 = Result(line);
// 	if (!done && r.test_combine_res(r1)){
// 	    r1 = r.combine_res(r1);
// 	    done = true;
// 	}
      
// 	line_vector.push_back(r1.to_line());
//     }
//     if (! done) 
// 	line_vector.push_back(r.to_line());
//     file.close();
  
//     create_file(file_name,line_vector);
// }


  
// int main() {
//     string file_name = "ccode/70_60_6_7.code";
//     string result_file_name = "result.res";

//     ifstream file;
//     cout << "A" << endl;
//     file.open(file_name);
//     if (file.fail()){
//         throw invalid_argument("File does not exist");
//     }

//     int n = stoi(get_param(file,"n"));
//     int m = stoi(get_param(file,"m"));
//     int dv = stoi(get_param(file,"dv"));
//     int dc = stoi(get_param(file,"dc"));

//     string id = get_param(file,"id");

//     cout << id << endl;

//     mat<int> bit_nbhd = get_matrix(file, "bit_nbhd", n, dv);
//     mat<int> check_nbhd = get_matrix(file, "check_nbhd", m, dc);

    
//     save_new_res(result_file_name, -1,1,2,3,4,"id",0.03422,100,26,74);
//     file.close();
//     cout << "fin" << endl;
//     return 0;
// }



