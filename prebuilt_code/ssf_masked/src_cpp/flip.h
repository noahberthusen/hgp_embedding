#include "mat.h"

class flip {
	public:
		int n;
		int m;

		int dc;
		int dv;

		mat<int>* check_nbhd_ptr;
		mat<int>* bit_nbhd_ptr;

		mat<bool>* synd_matrix_ptr;

		int synd_weight;

		int min_score;
		/* min_score
			Calculates whether there are still any valid qubits to flip
			The score is the amount the total syndrome weight would decrease if we flip b1, b2 (see below)

			Required by: find_best_gen()
		*/
		int b1, b2;
		/* b1, b2
			Best pair corresponding to min_score

			Required by: find_best_gen()
		*/
		bool t;
		/* t
			Type of qubits, VV <-> 0 and CC <-> 1

			Required by: find_best_gen()
		*/

		mat<int>* vv_score_ptr;
		mat<int>* cc_score_ptr;
		/* CC_score_ptr
			Scores corresponding to qubits.
			Generated once at the beginning by generate_score()
			Updated afterwards within update_score()
		*/

		mat<bool>* vv_qbits_ptr;
		mat<bool>* cc_qbits_ptr;
		/*	
			qbits_ptr represent deduced errors
			qbits_ptr(a,b) = 1 if qubit (a,b) is in error
		*/

		flip(int N, int M, int DV, int DC, mat<int>* CHECK_NBHD_PTR, mat<int>* BIT_NBHD_PTR);

		void compute_syndrome_matrix_ptr(mat<bool>& vv_errors, mat<bool>& cc_errors);
		/* compute_syndrome_matrix_ptr
			Same as in Decoder class

			Dependencies: none
			Required by : none
		*/
		void VV_generate_score(int v1, int v2);

		void CC_generate_score(int c1, int c2);
		/* generate_score

		*/


		void find_best_qbit();
		/* find_best_qbit
			finds the qbit such that when flipped, will lead to max decrease in synd weight

		*/

		void update();
		/* update
			amalgamation of all the updates (update_score, update_qbits_flips) and also updates synd_weight

			Dependencies: update_score, update_qbits_flips
			Required by: decoder

		*/

		void update_score(int v1, int c2, bool synd);
		/* update_score

			Dependencies: none
			Required by: update

		*/

		void update_qbits_flips();
		/* update_qbits_flips

			Dependencies: none
			Required by: update

		*/

		void decode();
		/* decode
			Runs find_best_qbit until flipping will not lead to decrease in syndrome

			Dependencies: update, find_best_qbit
		*/

		~flip();
};
