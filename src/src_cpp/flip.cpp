#include "flip.h"

flip::flip(int N, int M, int DV, int DC, mat<int>* CHECK_NBHD_PTR, mat<int>* BIT_NBHD_PTR) {
    n = N;
    m = M;

    dc = DC;
    dv = DV;

    check_nbhd_ptr = CHECK_NBHD_PTR;
    bit_nbhd_ptr = BIT_NBHD_PTR;

    synd_matrix_ptr = new mat<bool>(n,m,false);

    synd_weight = 0;

    b1 = 0;
    b2 = 0;
    t = 0;

	vv_score_ptr = new mat<int>(n,n,0);
	cc_score_ptr = new mat<int>(m,m,0);

    vv_qbits_ptr = new mat<bool>(n,n,false);
    cc_qbits_ptr = new mat<bool>(m,m,false);
}

void flip::compute_syndrome_matrix_ptr(mat<bool>& vv_errors, mat<bool>& cc_errors) {
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

    for (int v1 = 0; v1 < n; v1++) {
	    for (int c2 = 0; c2 < m; c2++ ) {
	        synd_weight += (*synd_matrix_ptr)(v1,c2);
	    }
    }

}

void flip::VV_generate_score(int v1, int v2) {
	for (v2 = 0; v2 < n; v2++) {
		(*vv_score_ptr)(v1,v2) = dv;
		for (int i = 0; i < dv; i++) {
			int c2 = (*bit_nbhd_ptr)(v2,i);
			(*vv_score_ptr)(v1,v2) += -2*(*synd_matrix_ptr)(v1,c2);
		}
	}
}

void flip::CC_generate_score(int c1, int c2) {
	for (c1 = 0; c1 < m; c1++) {
		(*cc_score_ptr)(c1,c2) = dc;
		for (int j = 0; j < dc; j++) {
			int v1 = (*check_nbhd_ptr)(c1,j);
			(*cc_score_ptr)(c1,c2) += -2*(*synd_matrix_ptr)(v1,c2);
		}
	}
}

void flip::find_best_qbit() {
	min_score = 0;
	b1 = None;
	b2 = None;
	t = 0;
	for (int v1 = 0; v1 < n; v1++) {
		for (int v2 = 0; v2 < n; v2++) {
			if (min_score > (*vv_score_ptr)(v1,v2)) {
				min_score = (*vv_score_ptr)(v1,v2);
				b1 = v1;
				b2 = v2;
				t = 0;
			}
		}
	}
	for (int c1 = 0; c1 < m; c1++) {
		for (int c2 = 0; c2 < m; c2++) {
			if (min_score > (*cc_score_ptr)(c1,c2)) {
				min_score = (*cc_score_ptr)(c1,c2);
				b1 = c1;
				b2 = c2;
				t = 1;
			}
		}
	}
}

void flip::update() {
	if (t == 0) {
		for (int i = 0; i < dv; i++) {
			int c2 = (*bit_nbhd_ptr)(b2,i);
			update_score(b1, c2, (*synd_matrix_ptr)(b1,c2));
			(*synd_matrix_ptr)(b1,c2) = !(*synd_matrix_ptr)(b1,c2);
		}
	}
	else {
		for (int j = 0; j < dc; j++) {
			int v1 = (*check_nbhd_ptr)(b1,j);
			update_score(v1, b2, (*synd_matrix_ptr)(v1,b2));
			(*synd_matrix_ptr)(v1,b2) = !(*synd_matrix_ptr)(v1,b2);
		}
	}

	synd_weight += min_score;

	update_qbits_flips();
}

void flip::update_score(int v1, int c2, bool synd) {
	for (int i = 0; i < dv; i++) {
		int c1 = (*bit_nbhd_ptr)(v1,i);
		(*cc_score_ptr)(c1,c2) += 4*synd-2;
	}
	for (int j = 0; j < dc; j++) {
		int v2 = (*check_nbhd_ptr)(c2,j);
		(*vv_score_ptr)(v1,v2) += 4*synd-2;
	}
}

void flip::update_qbits_flips() {
	if (t == 0) {
		(*vv_qbits_ptr)(b1,b2) ^= 1;
	}
	else {
		(*cc_qbits_ptr)(b1,b2) ^= 1;
	}
}

void flip::decode() {
	for (int v1 = 0; v1 < n; v1++) {
		for (int v2 = 0; v2 < n; v2++) {
			VV_generate_score(v1,v2);
		}
	}

	for (int c1 = 0; c1 < m; c1++) {
		for (int c2 = 0; c2 < m; c2++) {
			CC_generate_score(c1,c2);
		}
	}

	find_best_qbit();

	int i = 0;
	while (min_score < 0) {
		update();
		find_best_qbit();
		i = i+1;
		if (i > 100) {
			break;
		}
	}
}

flip::~flip() {
	delete synd_matrix_ptr;
	delete vv_score_ptr;
	delete cc_score_ptr;
	delete vv_qbits_ptr;
	delete cc_qbits_ptr;
}