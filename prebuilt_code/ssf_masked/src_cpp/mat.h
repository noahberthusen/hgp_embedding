//mat.h
#ifndef mat_H
#define mat_H

#include "input_params.h"
#include <iostream>
using namespace std;


template<typename T>
class mat{

 public:
    mat(int NO_ROWS, int NO_COLS, T INIT);
    mat(const mat<T> &); // Not implemented (rule of three)
    mat<T>& operator=(const mat<T> & L); // Not implemented (rule of three)
    ~mat();

    bool operator==(const mat<T>& rhs);

    void print() const;
    void print_true() const;

    T* operator()(int rowNo) const;
    T& operator()(int rowNo, int colNo) const;

    // For boolean matrices:
    void compute_rref(); // rref = reduced row echelon form
    mat<T>& operator^=(const mat<T>& matrix_right);

    int get_no_rows() const;
    int get_no_cols() const;	

 private:
    int no_rows, no_cols;
    T** M;
    
    // For boolean matrices:
    int first_line_true(int rank, int j) const; // Returns the first i >= rank such that mat(i,j) = true
    void swap_rows(int i, int j);
};


template<typename T>
mat<T>::mat(int NO_ROWS, int NO_COLS, T INIT) {
    no_rows = NO_ROWS;
    no_cols = NO_COLS;

    M = new T*[no_rows];

    for (int i = 0; i < no_rows; i++) {
	M[i] = new T[no_cols];
	for (int j = 0; j < no_cols; j++) {
	    M[i][j] = INIT;
	}
    }

}

//Copy-constructor
template<typename T>
mat<T>::mat(const mat<T> & matrix) {
    no_rows = matrix.no_rows;
    no_cols = matrix.no_cols;

    M = new T*[no_rows];

    for (int i = 0; i < no_rows; i++) {
        M[i] = new T[no_cols];
        for (int j = 0; j < no_cols; j++) {
	    M[i][j] = matrix(i,j);
        }
    }
}

//Affectation
template<typename T>
mat<T>& mat<T>::operator=(const mat<T> & L) {
    if (this != &L){
	no_rows = L.no_rows;
	no_cols = L.no_cols;

	for (int i = 0; i < no_rows; i++) {
	    for (int j = 0; j < no_cols; j++) {
		(*this)(i,j) = L(i,j);
	    }
	}
    }
    return *this;
}

template<typename T>
mat<T>::~mat() {
    for (int i = 0; i < no_rows; i++) {
        delete [] M[i];
    }
    delete [] M;
}


// check for equality
template<typename T>
bool mat<T>::operator==(const mat<T>& matrix_right) {
    if (no_rows != matrix_right.no_rows || no_cols != matrix_right.no_cols) {
    	return false;
    } 

    for (int i = 0; i < no_rows; i++) {
        for (int j = 0; j < no_cols; j++) {
            if ((*this)(i,j) != matrix_right(i,j)) {
                return false;
            }
        }
    }

    return true;
}


// Prints the matrix beautifully
template<typename T>
void mat<T>::print() const {
    std::cout << "Matrix: " << std::endl;
    for (int i = 0; i < no_rows; i++) {
        for (int j = 0; j < no_cols; j++) {
	    std::cout << "[" << (*this)(i,j) << "] ";
        }
	std::cout << std::endl;
    }
}

template<typename T>
T* mat<T>::operator()(int rowNo) const {
#if DEBUG
    if (rowNo > no_rows) {
	throw std::invalid_argument("Out of bounds");
    }
#endif
    return this->M[rowNo];
}

template<typename T>
T& mat<T>::operator()(int rowNo, int colNo) const {
#if DEBUG
    if ((rowNo > no_rows) || (colNo > no_cols)) {
	cout << "Trying to access row: " << rowNo << " and col " << colNo << endl;
	throw std::invalid_argument("Out of bounds");
    }
#endif
    return this->M[rowNo][colNo];
}

template<typename T>
void mat<T>::swap_rows(int i, int j) {
    for (int a = 0; a < no_cols; a++) {
	int temp = (*this)(i,a);
	(*this)(i,a) = (*this)(j,a);
	(*this)(j,a) = temp;
    }
}



template<typename T>
int mat<T>::first_line_true(int rank, int j) const {
    for (int i = rank; i < no_rows; i++) {
	if ((*this)(i,j)) {
            return i;
        }
    }
    return None;
}

        
// rref = reduced row echelon form
template<typename T>
void mat<T>::compute_rref() {
    
    int rank = 0;
    int i0;
    
    for (int j = 0; j < no_cols; j++) {
        i0 = first_line_true(rank, j);
        if (i0 != None) {
            swap_rows(i0, rank);
            for (int i = rank+1; i < no_rows; i++) {
                if ((*this)(i,j)) {
                    for (int j2 = j; j2 < no_cols; j2++) {
                        (*this)(i,j2) = (*this)(i,j2) ^ (*this)(rank,j2);
                    }
                }
            }
            rank = rank + 1;
        }
    }
}


template<typename T>
void mat<T>::print_true() const {
    std::cout << "Matrix indices: " << std::endl;
    for (int i = 0; i < no_rows; i++) {
        for (int j = 0; j < no_cols; j++) {
	    if ((*this)(i,j)) {
		std::cout << "(" << i << "," << j << ") ";
	    }
        }
    }
    std::cout << std::endl;
}


template<typename T>
mat<T>& mat<T>::operator^=(const mat<T>& matrix_right) {
    if (no_rows != matrix_right.no_rows || no_cols != matrix_right.no_cols) {
    	throw std::invalid_argument("Matrices do not have same size");
    }
    for (int i = 0; i < matrix_right.no_rows; i++) {
    	for (int j = 0; j < matrix_right.no_cols; j++) {
	    (*this)(i,j) ^= matrix_right(i,j);
        }
    }
    return *this;
}


template<typename T>
mat<T> operator^(const mat<T>& matrix_left,const mat<T>& matrix_right) {
    mat<T> matrix(matrix_left);
    matrix ^= matrix_right;
    return matrix;
}



template<typename T>
int mat<T>::get_no_rows() const{
    return no_rows;
}

template<typename T>
int mat<T>::get_no_cols() const{
    return no_cols;
}

#endif
