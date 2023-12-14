#include <iostream>

#include "mat.h"

int main() {
	mat g;
	mat m(3,4,0);

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j< 3; j++) {
			m(i,j) = (i + j + i*j)%2;
		}
	}
	m(2,2) = 1;

	m.print();
	mat R = m.compute_rref();
	R.print();

}