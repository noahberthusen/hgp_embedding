//generator.h
#ifndef generator_H
#define generator_H

#include <random>
#include <vector>
#include "mat.h"
#include "input_params.h"

using namespace std;


////////////////////// class Generator //////////////////////
// TODO: explain how score_gen works

/*
  bool* best_rows_flips, bool* best_col_flips
    optimal flips of cols and rows for generator respectively
    best_rows_flips: arr of size dc; best_rows_flips[i] = true ==> (v1,v2) where v1 = check_nbhd(c1,i) ought to be flipped
    best_col_flips: arr of size dv; best_col_flips[j] = true ==> (c1,c2) where c2 = bit_nbhd(v2,j) ought to be flipped
  

    void score_gen(int* gray_code)
      Input:
      'gray_code' is the output of 'Decoder::compute_gray_code'
      Updates:
      best_rows_flips, best_col_flips, best_synd_diff, best_weight
      We go through all the possible flips of columns and use the function 'col_subset_score'
      At the end, best_weight > 0 even it is better to flip nothing
      Dependencies: score_gen calls col_subset_score as sub-routine
      Required by: update_score_generator

  
    void col_subset_score();
      Input:
      'col_synd_diff' is |s| - |s xor synd(F)| for the current F which is a flip of the columns
      'col_weight' is the size of F
      rows_synd_diff[i] is the difference of syndrome size when we flip the line 'i'
      Output:
      'rows_flips' the optimal set of lines to flip for this given flips of columns
      'synd_diff' the syndrome difference for this flips
      col_weight = 0, i.e F = 0 then len(rows_flips) > 0 even if the flipping rows_flips increases the syndrome weight
      Dependencies: None
      Required by: score_gen
*/
/////////////////////////////////////////////////////////////


class generator {
 public:
    generator(int C1, int V2, int deg_c, int deg_v);
    generator(const generator& dec); // Not implemented (rule of three)
    generator operator=(const generator& dec); // Not implemented (rule of three)
    ~generator();

    // Compute the best possible flip for this generator
    void score_gen(const int* gray_code, const mat<int>& bit_nbhd,
		   const mat<int>& check_nbhd, const mat<bool>& synd_matrix);

    // Getters
    bool get_best_rows_flips(int i);
    bool get_best_col_flips(int j);
    int get_best_synd_diff();
    int get_best_weight();

 private:
    int c1, v2; //labels of generator
    int dc, dv; //degree of check and variable nodes

    bool* best_rows_flips; // arr of size dc, best subset of generator to flip
    bool* best_col_flips; // arr of size dv;
    int best_synd_diff; //syndrome difference for this set of flips
    int best_weight; // = dv * len*(rows_flips) + dc * len(col_flips) if weight_flag
                     // = len*(rows_flips) + len(col_flips) otherwise
    
    

    //////////////////////////////////////////////////
    // The following attributes are used in score_gen. We define them here because it would be costly to declare them at each call of score_gen (TODO: find a better way to do that)
    //////////////////////////////////////////////////
    int* rows_synd_diff; // array of size dc. rows_synd_diff[i] represents the decrease in syndrome weight when we flip row i.
    int col_synd_diff;
    bool* rows_flips;
    bool* col_flips;
    int col_weight;

    int synd_diff;
    int wt_rows_flips;

    mat<bool>* synd_gen_ptr;
    //////////////////////////////////////////////////

    void col_subset_score(); // Compute the best rows to flip with current collumn flip
    int compute_weight(int wt_rows, int wt_col); // to deal with the flag weight_flag
    void update_best(); // update best_* attributes when we have found better flips
};

#endif
