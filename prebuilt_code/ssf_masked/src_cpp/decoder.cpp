#include "decoder.h"
#include <algorithm>
#include <deque>

void compute_gray_code(int* gray_code, int begin, int end, int dv) {
    /*
      Starting from 0^dv, if you flip the bits res[0], res[1], ..., res[dv-2] then you go through {0,1}^dv
    */
    if (dv > 0) {
    	int mid = (begin + end)/2;
    	gray_code[mid] = dv - 1;
    	compute_gray_code(gray_code,begin,mid-1,dv-1);
    	compute_gray_code(gray_code,mid+1,end,dv-1);
    }
}

Decoder::Decoder(int N, int M, int DV, int DC, mat<int> const * CHECK_NBHD_PTR, mat<int> const * BIT_NBHD_PTR): n(N), m(M), dc(DC), dv(DV), check_nbhd_ptr(CHECK_NBHD_PTR), bit_nbhd_ptr(BIT_NBHD_PTR)
{

    size_gray = pow(2,dv)-1;

    gray_code = new int[size_gray];
    for (int i = 0; i < size_gray; i++) {
        gray_code[i] = 0;
    }

    compute_gray_code(gray_code, 0, size_gray-1, dv);

    round = 0;

    last_update_ptr = new mat<int>(m,n,-1);

    synd_matrix_ptr = new mat<bool>(n,m,false);

    lookup_table_ptr = new mat<generator*>(m,n,NULL);
    for (int c1 = 0; c1 < m; c1++) {
        for (int v2 = 0; v2 < n; v2++) {
            (*lookup_table_ptr)(c1,v2) = new generator(c1,v2,dc,dv);
        }
    }

    synd_weight = 0;

    vv_qbits_ptr = new mat<bool>(n,n,false);

    cc_qbits_ptr = new mat<bool>(m,m,false);
}


Decoder::Decoder(const Decoder& dec) :
    n(dec.n), m(dec.m), dc(dec.dc), dv(dec.dv), size_gray(dec.size_gray), synd_weight(dec.synd_weight), round(dec.round) { // deep copy
    vv_qbits_ptr = new mat<bool>(*dec.vv_qbits_ptr);
    cc_qbits_ptr = new mat<bool>(*dec.cc_qbits_ptr);

    gray_code = new int[size_gray];
    for (int i = 0; i < size_gray; i++) {
        gray_code[i] = dec.gray_code[i];
    }

    lookup_table_ptr = new mat<generator*>(dec.m,dec.n,NULL);
    for (int c1 = 0; c1 < dec.m; c1++) {
        for (int v2 = 0; v2 < dec.n; v2++) {
            (*lookup_table_ptr)(c1, v2) = new generator(*((*dec.lookup_table_ptr)(c1, v2)));
        }
    }

    check_nbhd_ptr = new mat<int>(*dec.check_nbhd_ptr);
    bit_nbhd_ptr = new mat<int>(*dec.bit_nbhd_ptr);
    synd_matrix_ptr = new mat<bool>(*dec.synd_matrix_ptr);
    last_update_ptr = new mat<int>(*dec.last_update_ptr);

    // best_gen_indices = dec.best_gen_indices;
    // vector<int> best_gen_indices(dec.best_gen_indices);
    best_gen_indices = vector<tuple<int, int>>(0);
    for (size_t i = 0; i < dec.best_gen_indices.size(); i++) {
        tuple<int, int> tmp(get<0>(dec.best_gen_indices[i]), get<1>(dec.best_gen_indices[i]));
        best_gen_indices.push_back(make_tuple(get<0>(dec.best_gen_indices[i]), get<1>(dec.best_gen_indices[i])));
    }
}


Decoder Decoder::operator=(const Decoder& dec){
    return Decoder(dec);
}

bool Decoder::operator==(const Decoder& dec) {
    // will behave the same if they have the same syndrome matrices (or maybe guessed errors)
    // return synd_matrix_ptr == dec.synd_matrix_ptr;
    return (*vv_qbits_ptr == *dec.vv_qbits_ptr && *cc_qbits_ptr == *dec.cc_qbits_ptr);
}


Decoder::~Decoder() {
    delete vv_qbits_ptr;
    delete cc_qbits_ptr;

    for (int c1 = 0; c1 < m; c1++) {
        for (int v2 = 0; v2 < n; v2++) {
            delete (*lookup_table_ptr)(c1,v2);
        }
    }

    delete lookup_table_ptr;
    delete synd_matrix_ptr;
    delete last_update_ptr;
    delete[] gray_code;
}



const mat<bool>& Decoder::get_vv_correction(){
    return *vv_qbits_ptr;
}

const mat<bool>& Decoder::get_cc_correction(){
    return *cc_qbits_ptr;
}

int Decoder::get_synd_weight(){
    return synd_weight;
}




void Decoder::compute_syndrome_matrix_ptr(const mat<bool>& vv_errors, const mat<bool>& cc_errors) {
    for (int v1 = 0; v1 < n; v1++) {
        for (int c2 = 0; c2 < m; c2++) {
            (*synd_matrix_ptr)(v1,c2) = false;
            for (int i = 0; i < dv; i++) {
		        (*synd_matrix_ptr)(v1,c2) ^= cc_errors((*bit_nbhd_ptr)(v1,i),c2);
            }
            for (int j = 0; j < dc; j++) {
                (*synd_matrix_ptr)(v1,c2) ^= vv_errors(v1,(*check_nbhd_ptr)(c2,j));
            }
        }
    }

    for (int c1 = 0; c1 < m; c1++ ) {
	    for (int v2 = 0; v2 < n; v2++) {
	        synd_weight += (*synd_matrix_ptr)(v2,c1);
	    }
    }

}

void Decoder::find_best_gen() {
    int synd_diff, weight; //temporary variables created in-function
    int best_synd_diff = -1;
    int best_weight = 0;
    for (int c1 = 0; c1 < m; c1++) {
        for (int v2 = 0; v2 < n; v2++) {
            synd_diff = (*lookup_table_ptr)(c1,v2)->get_best_synd_diff();
            weight = (*lookup_table_ptr)(c1,v2)->get_best_weight();
            if (synd_diff > 0 && best_synd_diff*weight < synd_diff*best_weight) {
                best_gen[0] = c1;
                best_gen[1] = v2;
                best_synd_diff = synd_diff;
                best_weight = weight;
#if STOP == true
		if (best_synd_diff == best_weight * dv) return;
#endif
            }
        }
    }
}

// finds best k nonzero generators
void Decoder::find_best_gen(int k) {
    best_gen_indices.clear();
    int synd_diff, weight;
    vector<generator*> best_gens;

    for (int c1 = 0; c1 < m; c1++) {
        for (int v2 = 0; v2 < n; v2++) {
            bool placed = false;
            synd_diff = (*lookup_table_ptr)(c1,v2)->get_best_synd_diff();
            weight = (*lookup_table_ptr)(c1,v2)->get_best_weight();

            for(size_t i = 0; i < best_gens.size(); i++) {
                int best_synd_diff = best_gens[i]->get_best_synd_diff() ? best_gens[i]->get_best_synd_diff() : -1;
                int best_weight = best_gens[i]->get_best_weight();
                if (synd_diff > 0 && best_synd_diff*weight < synd_diff*best_weight) {
                    best_gen_indices.insert(best_gen_indices.begin()+i, make_tuple(c1, v2));
                    // best_gen_indices.insert(best_gen_indices.begin()+i, c1);
                    best_gens.insert(best_gens.begin()+i, (*lookup_table_ptr)(c1, v2));
                    placed = true;
                    break;
                }
            }

            if (best_gens.size() > k) {
                best_gens.pop_back();
                best_gen_indices.resize(best_gen_indices.size()-1);
            }
            if (synd_diff > 0 && !placed && best_gens.size() < k) {
                best_gen_indices.push_back(make_tuple(c1, v2));
                // best_gen_indices.push_back(v2);
                best_gens.push_back((*lookup_table_ptr)(c1,v2));
            }  
        }
    }
}

//To-do: update less generators
void Decoder::update(int c1, int v2) {
    round = round + 1;
    int synd_diff = (*lookup_table_ptr)(c1,v2)->get_best_synd_diff();

    update_qbits_flips(c1, v2);
    update_synd_matrix(c1, v2);
    synd_weight = synd_weight - synd_diff;

    for (int i = 0; i < dc; ++i) {
    	int v1 = (*check_nbhd_ptr)(c1,i);
    	for (int j = 0; j < dv; ++j) {
    	    int c2 = (*bit_nbhd_ptr)(v2,j);
    	    for (int i_ = 0; i_ < dc; ++i_) {
    		    int v2_ = (*check_nbhd_ptr)(c2,i_);
    		    for (int j_ = 0; j_ < dv; ++j_) {
    		        int c1_ = (*bit_nbhd_ptr)(v1,j_);
    		        if ((*last_update_ptr)(c1_,v2_) != round) {
    			        update_score_generator(c1_,v2_);
    			        (*last_update_ptr)(c1_,v2_) = round;
    		        }
    		    }
    	    }
     	}
    }
    // cout << "end update" << endl;
}

void Decoder::update_synd_matrix(int c1, int v2) {
    for (int i = 0; i < dc; i++) {
        for (int j = 0; j < dv; j++) {
            (*synd_matrix_ptr)((*check_nbhd_ptr)(c1,i),(*bit_nbhd_ptr)(v2,j)) ^=
		(*lookup_table_ptr)(c1,v2)->get_best_rows_flips(i) ^
		(*lookup_table_ptr)(c1,v2)->get_best_col_flips(j);
        }
    }
}


void Decoder::update_qbits_flips(int c1, int v2) {
    for (int i = 0; i < dc; i++) {
        (*vv_qbits_ptr)((*check_nbhd_ptr)(c1,i),v2) ^= (*lookup_table_ptr)(c1,v2)->get_best_rows_flips(i);
    }
    for (int j = 0; j < dv; j++) {
        (*cc_qbits_ptr)(c1,(*bit_nbhd_ptr)(v2,j)) ^= (*lookup_table_ptr)(c1,v2)->get_best_col_flips(j);
    }
}

void Decoder::update_score_generator(int c1, int v2) {
    (*lookup_table_ptr)(c1,v2)->score_gen(gray_code, *bit_nbhd_ptr, *check_nbhd_ptr , *synd_matrix_ptr);
}

void Decoder::decode(const mat<bool>& vv_errors, const mat<bool>& cc_errors) {
    compute_syndrome_matrix_ptr(vv_errors, cc_errors);

    for (int c1 = 0; c1 < m; c1++) {
        for (int v2 = 0; v2 < n; v2++) {
	        update_score_generator(c1, v2);
        }
    }

    find_best_gen();

    int c1_ = best_gen[0];
    int v2_ = best_gen[1];
    
    while((*lookup_table_ptr)(c1_,v2_)->get_best_synd_diff() > 0) {
        update(c1_,v2_);          
        find_best_gen();
        c1_ = best_gen[0];
        v2_ = best_gen[1];
    }
}

void Decoder::decode_list(const mat<bool>& vv_errors, const mat<bool>& cc_errors, int k) {
    compute_syndrome_matrix_ptr(vv_errors, cc_errors);
    // cout << "beginning syndrome weight: " << synd_weight << endl;
    // can parallelize this too ig
    for (int c1 = 0; c1 < m; c1++) {
        for (int v2 = 0; v2 < n; v2++) {
	        update_score_generator(c1, v2);
        }
    }
    
    deque<Decoder> decoders;
    deque<Decoder> finished_decoders;

    Decoder root = Decoder(*this);
    // root.find_best_gen(k);
    // for (size_t i = 0; i < root.best_gen_indices.size(); i++) {
    //     cout << root.best_gen_indices[i] << " ";
    // }
    // cout << endl;
    // root.update(5, 0);
    // root.find_best_gen(k);
    // for (size_t i = 0; i < root.best_gen_indices.size(); i++) {
    //     cout << root.best_gen_indices[i] << " ";
    // }
    // cout << endl;
    // cout << float((*root.lookup_table_ptr)(5, 0)->get_best_synd_diff())/float((*root.lookup_table_ptr)(5, 0)->get_best_weight()) << endl;
    // root.update(5, 0);
    // cout << float((*root.lookup_table_ptr)(5, 0)->get_best_synd_diff())/float((*root.lookup_table_ptr)(5, 0)->get_best_weight()) << endl;

    // tmp_gen.find_best_gen(1);
    // for (size_t i = 0; i < tmp_gen.best_gen_indices.size(); i++) {
    //     cout << tmp_gen.best_gen_indices[i] << " ";
    // }
    // cout << endl;
    // find_best_gen(k);
    // cout << "og: ";
    // for (size_t i = 0; i < best_gen_indices.size(); i++) {
    //     cout << best_gen_indices[i] << " ";
    // }
    // cout << endl;

    decoders.push_back(root);

    while (decoders.size()) {
    // for (int m = 0; m < 2; m++) {
        size_t dec_size = decoders.size();
        // cout << "dec list size " << dec_size << endl;
        // parallelize this
        for (size_t i = 0; i < dec_size; i++) {
            decoders[i].find_best_gen(k);

            if (!decoders[i].best_gen_indices.size()) {
                // cout << "done" << endl;
                finished_decoders.push_back(Decoder(decoders[i]));
                continue;
            }
            // cout << decoders[i].best_gen_indices.size() << endl;
            for (size_t j = 0; j < decoders[i].best_gen_indices.size(); j++) {
                Decoder tmp_dec = Decoder(decoders[i]);
                // cout << "copy of copy: ";
                // for (size_t i = 0; i < tmp_dec.best_gen_indices.size(); i++) {
                //     cout << tmp_dec.best_gen_indices[i] << " ";
                // }

                // cout << "before access" << endl;
                // int c1_ = tmp_dec.best_gen_indices[j];
                int c1_ = get<0>(tmp_dec.best_gen_indices[j]);
                // int v2_ = tmp_dec.best_gen_indices[j+1];
                int v2_ = get<1>(tmp_dec.best_gen_indices[j]);

                // cout << c1_ << " " << v2_ << endl;

                // tmp_dec.vv_qbits_ptr->print_true();
                // tmp_dec.cc_qbits_ptr->print_true();
                // cout << "before update" << endl;
                tmp_dec.update(c1_, v2_);
                // tmp_dec.vv_qbits_ptr->print_true();
                // tmp_dec.cc_qbits_ptr->print_true();
                // tmp_dec.find_best_gen(k);
                decoders.push_back(tmp_dec);
                // cout << "no copy?" << endl;
            }
        }
        // cout << "erasing-----------------------" << endl;

        for (size_t i = 0; i < dec_size; i++) { // remove old decoders
            decoders.pop_front();
        }
        // check for duplicate syndromes here

        decoders.erase(unique(decoders.begin(), decoders.end()), decoders.end());
        // for (size_t i = 0; i < decoders.size(); i++) {
        //     decoders[i].vv_qbits_ptr->print_true();
            // decoders[i].cc_qbits_ptr->print_true();
            // decoders[i].synd_matrix_ptr->print_true();
            // cout << decoders[i].synd_weight << endl;
        // }

        // cout << endl;
    }

    // for (int i = 0; i < finished_decoders.size(); i++) {
    //     finished_decoders[i].vv_qbits_ptr->print_true();
    //     cout << finished_decoders[0].synd_weight << endl;
    // }
    
    // finished_decoders[0].vv_qbits_ptr->print_true();
}

