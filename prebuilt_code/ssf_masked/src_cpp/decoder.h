//lookup_table.h
#ifndef decoder_H
#define decoder_H

#include "input_params.h"
#include "generator.h"
#include <math.h>
#include <vector>
#include <tuple>

using namespace std;

//////////////// Decoder class ////////////////
/*

  compute_syndrome_matrix_ptr
    Depedencies: None
    Required by: decode


  synd_weight:
    Used by: init, update


  lookup_table:
    Used by: init, find_best_gen, update, update_score_generator


  best_gen
    Used by: find_best_gen


  synd_matrix
    Used by: compute_synd


  vv_qbits, cc_qbits:
    Used by: compute_qbits


  round
    Used by: update


  find_best_gen
    Updates:
      best_gen
      best_synd_diff
      best_weight
    Dependencies: None
    Required by: None


  update
    Updates:
    Dependences: compute_synd
    Required by:


  update_synd_matrix
    Updates:
      synd_matrix
    Dependencies:
    Required by: update


  update_qbits_flips
    Updates:
      vv_qbits
      cc_qbits
    Dependencies: None
    Required by: update


  update_score_generator
    Required by: update

*/
///////////////////////////////////////////////


class Decoder {

 public:
    
    Decoder(int N, int M, int DV, int DC, mat<int> const * CHECK_NBHD, mat<int> const * BIT_NBHD);
    Decoder(const Decoder& dec); // Not implemented (rule of three)
    Decoder operator=(const Decoder& dec); // Not implemented (rule of three)
    bool operator==(const Decoder& dec);
    ~Decoder();

    void decode(const mat<bool>& vv_errors, const mat<bool>& cc_errors, const mat<bool>& synd_mask);
    void decode_list(const mat<bool>& vv_errors, const mat<bool>& cc_errors, const mat<bool>& synd_mask, int k);
    int get_synd_weight();
    int get_correction_weight();
    const mat<bool>& get_vv_correction();
    const mat<bool>& get_cc_correction();

    bool operator< (const Decoder& dec);
    friend bool operator==(const Decoder& lhs, const Decoder& rhs);
    int compute_syndrome_weight(const mat<bool>& vv_errors, const mat<bool>& cc_errors, const mat<bool>& synd_mask) const;

 private:
    
    int n, m; // no of check nodes and no of var nodes
    int dc, dv; // check degree and variable node degree

    int size_gray; // = 2**dv - 1
    int* gray_code; // Computed once at initialisation and given in parameter to generator::score_gen

    mat<int> const * check_nbhd_ptr; // m x dc matrix, same than class qcode
    mat<int> const * bit_nbhd_ptr; // n x dv matrix, same than class qcode

    int synd_weight;  // Total weight of syndrome
    int correction_weight; // weight of the guessed error
    mat<generator*>* lookup_table_ptr; // mxn matrix representing Z-type generators
    int round;
    mat<int>* last_update_ptr; // (*last_update_ptr)(c1,v2) is the last round we have updated (*lookup_table_ptr)(c1,v2)

    vector<tuple<int,int>> best_gen_indices; // indices best k generators to flip.
    int best_gen[2]; // = (c1,v2) representing the best generator to flip
    mat<bool>* synd_matrix_ptr; // n x m matrix

    mat<bool>* vv_qbits_ptr; // n x n matrix representing vv guessed error
    mat<bool>* cc_qbits_ptr; // m x m matrix representing cc guessed error

    mat<bool>* synd_mask_ptr; // mask over the syndrome
    
    void compute_syndrome_matrix_ptr(const mat<bool>& vv_errors, const mat<bool>& cc_errors);
    void find_best_gen(); // computes the best generator to flip for the current syndrome
    void find_best_gen(int k); // computes the best k generators to flip for the current syndrome
    void update(int c1, int v2); // Calls the three following update functions in the right order when flipping generator (c1,v2)
    void update_synd_matrix(int c1, int v2); // Updates synd_matrix when flipping generator (c1,v2)
    void update_qbits_flips(int c1, int v2); // Updates vv/cc_qbits when flipping generator (c1,v2)
    void update_score_generator(int c1, int v2); // Computes score of generator (c1,v2). Be carefull: (c1,v2) does not represent the same generator than in the previous functions.
};

#endif
