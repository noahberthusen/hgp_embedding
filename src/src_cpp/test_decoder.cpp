#include <iostream>

#include "decoder.h"

#include "read_code.h"

#include <random>

mat<bool> generate_errors(double p, int t) {
    int r1;

    mat<bool> errors(t,t,0);

    random_device rd;  //Will be used to obtain a seed for the random number engine
    mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
    bernoulli_distribution dis(p);
    for (int a = 0; a < t; a++) {
      for (int b = 0; b < t; b++) {
      r1 = dis(gen);
      if (r1 == 1) {
    errors(a,b) = (errors(a,b) + 1)%2;
      }
  }
    }

    return errors;
}

int main() {

	double p = 0.01;

	string file_name = "../ccode/70_60_6_7.code";

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

    mat<int> bit_nbhd = get_matrix(file, "bit_nbhd", n, dv);
    mat<int> check_nbhd = get_matrix(file, "check_nbhd", m, dc);

    Decoder dec(n,m,dc, dv, &check_nbhd, &bit_nbhd);

    
    p = 0.01;
    int no_test = 25;
    for (int r = 0; r < no_test; r++) {
      mat<bool> vv_errors = generate_errors(p, n);
      mat<bool> cc_errors = generate_errors(p, m);

      // cout << "Initial error:" << endl;
      // vv_errors.print_true();
    
      // cc_errors.print_true();

    
      

      dec.compute_syndrome_matrix_ptr(vv_errors, cc_errors);
      // dec.synd_matrix_ptr->print_true();

      for (int c1 = 0; c1 < m; c1++) {
      	for (int v2 = 0; v2 < n; v2++) {
      	  dec.update_score_generator(c1,v2);
        }
      }
      dec.find_best_gen();

      int c1_ = dec.best_gen[0];
      int v2_ = dec.best_gen[1];

      // dec.synd_matrix_ptr->print_true();
	
      // for (int j = 0; j < dc; ++j) {
      //   cout << check_nbhd(3,j) << " ";
      // }
      // cout << endl;
      // cout << "c1, v2 best gen  " << c1_ << " " << v2_;
      // cout << " best_synd_diff originally: " << (*dec.dec[n*c1_ + v2_]).best_synd_diff << endl;
      // cout << "Random synd_diff" << (*dec.dec[n*c1_ + v2_+1]).best_synd_diff << endl;


      // cout << endl << "best_ver_flips: ";
      // for (int i = 0; i < dv; i++) {
      // 	cout << (*dec.dec[n*c1_ + v2_]).best_ver_flips[i];
      // }

      // cout << endl << "best_hor_flips: ";
      // for (int j = 0; j < dc; j++) {
      // 	cout << (*dec.dec[n*c1_ + v2_]).best_hor_flips[j];
      // }

      // cout << endl;

 	
      // cout << "syd weight " << dec.synd_weight << endl;

      while((*dec.lookup_table_ptr)(c1_,v2_)->best_synd_diff > 0) {
	dec.update(c1_,v2_);
	// cout << "syd weight " << dec.synd_weight << endl;
	  
	  
	dec.find_best_gen();
	c1_ = dec.best_gen[0];
	v2_ = dec.best_gen[1];
	// cout << c1_ << " " << v2_ << endl;
	// cout << "best_synd_diff later" << (*dec.dec[n*c1_ + v2_]).best_synd_diff << endl;
      }

      //cout << "Final synd weight " << dec.synd_weight << endl;
      //cout << "Final error:" << endl;
      mat<bool> final_vv_errors = *dec.vv_qbits_ptr ^ vv_errors;
      mat<bool> final_cc_errors = *dec.cc_qbits_ptr ^ cc_errors;
      //final_vv_errors.print_true();
      //final_cc_errors.print_true();
      // vv_errors.print_true();
      // cc_errors.print_true();
      // dec.vv_qbits_ptr->print_true();
      // dec.cc_qbits_ptr->print_true();
      
    }
}
