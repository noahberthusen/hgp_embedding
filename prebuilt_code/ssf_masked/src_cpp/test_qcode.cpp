#include <iostream>
#include "qcode.h"
#include "read_code.h"
#include "mat.h"



using namespace std;


qcode test() {
    string file_name = "ccode/70_60_6_7.code";

    ifstream file;

    file.open(file_name);
    if (file.fail()){
        throw invalid_argument("File does not exist");
    }

    int n = stoi(get_param(file,"n"));
    int m = stoi(get_param(file,"m"));
    int dv = stoi(get_param(file,"dv"));
    int dc = stoi(get_param(file,"dc"));

    string id = get_param(file,"id");

    cout << id << endl;

    mat<int> bit_nbhd = get_matrix(file, "bit_nbhd", n, dv);
    mat<int> check_nbhd = get_matrix(file, "check_nbhd", m, dc);

    return qcode(n,m,dv,dc, id, &bit_nbhd, &check_nbhd);

}

int main() {

    qcode & Q(test());
    cout << Q.n << endl;
    
    // // 3 x 3 Toric code
    // int n = 3;
    // int m = 3;
    // int dc = 2;
    // int dv = 2;

    // mat<int> bit_nbhd(3,2,0);
    // bit_nbhd(0,0) = 2;
    // bit_nbhd(0,1) = 0;
    // bit_nbhd(1,0) = 0;
    // bit_nbhd(1,1) = 1;
    // bit_nbhd(2,0) = 1;
    // bit_nbhd(2,1) = 2;

    // mat<int> check_nbhd(3,2,0);
    // check_nbhd(0,0) = 0;
    // check_nbhd(0,1) = 1;
    // check_nbhd(1,0) = 1;
    // check_nbhd(1,1) = 2;
    // check_nbhd(2,0) = 2;
    // check_nbhd(2,1) = 0;

    // qcode Q(n,m,dv,dc, &bit_nbhd, &check_nbhd);

    // Q.compute_cpci_rref();

    // Q.compute_cpc_rref();

    // Q.compute_i_rref();

    // Q.compute_ctpc_rref();

    // mat<bool> vv_error(3,3,0);
    // mat<bool> cc_error(3,3,0);

    // // vv_error(0,0) = 1;
    // // vv_error(0,1) = 1;
    // // vv_error(0,2) = 1;

    // // vv_error(1,0) = 1;
    // // vv_error(1,1) = 1;
    // // cc_error(0,0) = 1;
    // // cc_error(1,0) = 1;

    // // vv_error(0,1) = 1;
    // // vv_error(1,1) = 1;
    // // cc_error(0,0) = 1;
    // // cc_error(0,1) = 1;

    // vv_error(0,0) = 1;
    // vv_error(0,1) = 1;
    // vv_error(1,0) = 1;
    // vv_error(1,1) = 1;
    // vv_error(2,2) = 1;
    // cc_error(0,2) = 1;
    // cc_error(0,1) = 1;

    // cout << Q.is_stabilizer(vv_error, cc_error) << endl;



    return 0;
}
