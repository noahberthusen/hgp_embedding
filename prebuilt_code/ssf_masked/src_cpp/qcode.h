//ccode.h
#ifndef qcode_H
#define qcode_H

#include <vector>
#include "mat.h"
#include "input_params.h"

class qcode {
 public:
    qcode(int N, int M, int DV, int DC, std::string ID,
	  mat<int>* BIT_NBHD, mat<int>* CHECK_NBHD);
    qcode(const qcode& Q); // Not implemented (rule of three)
    qcode& operator=(const qcode& Q); // Not implemented (rule of three)
    ~qcode();
    
    const int n, m;
    const int dv, dc;
    const std::string id;

    mat<int> const * bit_nbhd_ptr;    // bit nbhd of classical graph
    mat<int> const * check_nbhd_ptr;  // check nbhd of classical graph

    // Test whether the code attributes match one value in each array
    bool test(const vector<int>& n_vector,
	      const vector<int>& m_vector,
	      const vector<int>& dv_vector,
	      const vector<int>& dc_vector,
	      const vector<string>& id_vector) const;

    bool is_stabilizer(const mat<bool>& vv_xerror, const mat<bool>& cc_xerror) const;
		
    void compute_cpci_rref();
    void compute_cpc_rref();
    void compute_i_rref();
    void compute_ctpc_rref();

 private:

    // rref = reduced row echelon form
    // cpci = classical parity check matrix concatenated with identity
    // ctpc = classical transpose parity check
    mat<bool>* cpci_rref_ptr;
    mat<bool>* cpc_rref_ptr;
    mat<bool>* i_rref_ptr;
    mat<bool>* ctpc_rref_ptr;    
};




class qcode_ensemble {
 public:
    qcode_ensemble(char const * const * file_name, int no_files,
		   const vector<int>& n_vector, const vector<int>& m_vector,
		   const vector<int>& dv_vector, const vector<int>& dc_vector,
		   const vector<string>& id_vector);
    qcode_ensemble(const qcode_ensemble& Q); // Not implemented (rule of three)
    qcode_ensemble& operator=(const qcode_ensemble& Q); // Not implemented (rule of three)
    ~qcode_ensemble();
    
    int get_no_qcodes() const;
    qcode* get_qcode_ptr(int qcode_index) const;
    
    
    
 private:
    int no_qcodes;
    vector<qcode*> qcode_vector;
};


#endif

