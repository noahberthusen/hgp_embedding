#include "generator.h"
#include <math.h>
#include <algorithm>


// Returns Y, indices of X sorted according to increasing order of values of X.
vector<int> ordered_sort(int* X, int length_X){
    vector<int> y(length_X);
    for (int i = 0; i < length_X ; i++) {
        y[i] = i;
    }
    auto comparator = [&X](int a, int b){ return X[a] > X[b]; };
    sort(y.begin(), y.end(), comparator);
    return y;
}


// Returns the cardinality (or weighted cardinality) of the flips
int generator::compute_weight(int wt_rows, int wt_col) {
#if (weight_flag)
    int ans = dv*wt_rows + dc*wt_col;
#else
    int ans = wt_rows + wt_col;
#endif

    return ans;
}

generator::generator(int C1, int V2, int DC, int DV) :
    c1(C1), v2(V2), dc(DC), dv(DV) {
    
    best_rows_flips = new bool[dc];
    best_col_flips = new bool[dv];

    rows_flips = new bool[dc];
    for (int i = 0; i < dc; i++) {
        rows_flips[i] = 0;
    }

    col_flips = new bool[dv];
    for (int i = 0; i < dc; i++) {
        col_flips[i] = 0;
    }

    rows_synd_diff = new int[dc];
    for (int i = 0; i < dc; i++) {
        rows_synd_diff[i] = 0;
    }

    // No need to initialise this matrix. It is used only in score_gen where it is initialized
    synd_gen_ptr = new mat<bool>(dc,dv,false);
}


generator::generator(const generator& gen) :
    c1(gen.c1), v2(gen.v2), dc(gen.dc), dv(gen.dv), 
    best_synd_diff(gen.best_synd_diff), best_weight(gen.best_weight),
    col_synd_diff(gen.col_synd_diff), col_weight(gen.col_weight),
    synd_diff(gen.synd_diff), wt_rows_flips(gen.wt_rows_flips) {
    
    rows_flips = new bool[dc];
    for (int i = 0; i < dc; i++) {
        rows_flips[i] = gen.rows_flips[i];
    }

    col_flips = new bool[dv];
    for (int i = 0; i < dc; i++) {
        col_flips[i] = gen.col_flips[i];
    }

    rows_synd_diff = new int[dc];
    for (int i = 0; i < dc; i++) {
        rows_synd_diff[i] = gen.rows_synd_diff[i];
    }

    best_col_flips = new bool[dv];
    for (int i = 0; i < dv; i++) {
        best_col_flips[i] = gen.best_col_flips[i];
    }

    best_rows_flips = new bool[dc];
    for (int i = 0; i < dc; i++) {
        best_rows_flips[i] = gen.best_rows_flips[i];
    }

    synd_gen_ptr = new mat<bool>(dc,dv,false);
}

generator generator::operator=(const generator& gen){
    return generator(gen);
}

generator::~generator() {
    delete synd_gen_ptr;
    delete [] rows_synd_diff;
    delete [] col_flips;
    delete [] rows_flips;
    delete [] best_col_flips;
    delete [] best_rows_flips;
}


bool generator::get_best_rows_flips(int i) {
    return best_rows_flips[i];
}

bool generator::get_best_col_flips(int j) {
    return best_col_flips[j];
}

int generator::get_best_synd_diff() {
    return best_synd_diff;
}

int generator::get_best_weight() {
    return best_weight;
}


// Call this function when the current flips have a better score than the current best
void generator::update_best() {
    best_synd_diff = synd_diff;
    best_weight = compute_weight(wt_rows_flips, col_weight);
    for (int i = 0; i < dc; ++i) {
        best_rows_flips[i] = rows_flips[i];
    }
    for (int j = 0; j < dv; ++j) {
        best_col_flips[j] = col_flips[j];
    }
}

// Compute the best flip for the generator
void generator::score_gen(const int* gray_code,
			  const mat<int>& bit_nbhd,
			  const mat<int>& check_nbhd,
			  const mat<bool>& synd_matrix) {
    
    for (int i = 0; i < dc; i++) {
        for (int j = 0; j < dv; j++) {
            // cout << "begin here?" << endl;
            bool check = synd_matrix(check_nbhd(c1,i),bit_nbhd(v2,j));
            // cout << "here?" << endl;
            (*synd_gen_ptr)(i,j) = check;
        }
    }
    // cout << "in score gen" << endl;

    col_weight = 0;
    for (int i = 0; i < dv; i++) {
        col_flips[i] = 0;
    }
    
    for (int i = 0; i < dc; i++) {
        rows_synd_diff[i] = 0;
        for (int j = 0; j < dv; j++) { // put mask here
	        rows_synd_diff[i] = rows_synd_diff[i] + 2*(*synd_gen_ptr)(i,j) - 1;
        }
    }

    col_synd_diff = 0;
    
    col_subset_score();
    update_best();

    int size_gray = pow(2,dv) - 1;

#if (!sampling_flag) 
    for (int i = 0; i < size_gray; i++) {
	int j = gray_code[i];
#else
    float PORTION = 0.5;
    int SAMPLE_SIZE = floor(PORTION*size_gray);
    for (int i = 0; i < SAMPLE_SIZE; i++) {
	int ind = (rand() % static_cast<int>(size_gray));
	int j = gray_code[ind];
#endif

	int a = (1-2*col_flips[j]);
	col_weight = col_weight + a;
	col_flips[j] = col_flips[j] + a;
	for (int i = 0; i < dc; i++) { // put mask here
	    rows_synd_diff[i] = rows_synd_diff[i] - a*4*(*synd_gen_ptr)(i,j) + a*2;
	    col_synd_diff = col_synd_diff + a*2*(*synd_gen_ptr)(i,j) - a;
	}

	col_subset_score();
	int weight = compute_weight(wt_rows_flips, col_weight);
	if (synd_diff*best_weight > best_synd_diff*weight) {
	    update_best();	    
#if STOP == true
	    if (best_synd_diff == best_weight * dv) return;
#endif
	}
    }

    // cout << "end score gen" << endl;
}

// Computes the best rows to flip for the current flip of collumns
void generator::col_subset_score() {
    
    synd_diff = col_synd_diff;
    vector<int> sorted_rows_synd_diff = ordered_sort(rows_synd_diff, dc);
    wt_rows_flips = 0;

    int s, weight; //temporary variables only used in-function
    
    for (auto i: sorted_rows_synd_diff) {
	s = rows_synd_diff[i];
	weight = compute_weight(wt_rows_flips, col_weight);
	if (s*weight >= synd_diff) {
	    synd_diff = synd_diff + s;
	    rows_flips[i] = 1;
	    wt_rows_flips += 1;
	}
	else {
	    rows_flips[i] = 0;
	}
    }
}

