#ifndef SWAP_EDGES
#define SWAP_EDGES

#include "ccode.hpp"
#include "../mat.h"

#include <vector>


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////


class Score {
public:

    Score(Ccode const * ccode, int* no_cycles_vector0);
    Score(const Score &); // Not implemented (rule of three)
    Score& operator=(const Score &); // Not implemented (rule of three)
    ~Score();

    int compare(Score* score);
    void print();
    
private:

    // To compute the number of path between two vertices
    int path_len;
    mat<int>* path;
    mat<int>* old_path;
    void path_step(Ccode const * ccode);
    int* no_cycles_vector;
    
    vector<std::pair<int,int>> no_cycles_hist1; // The elements (-i,-n) of this vector means that n bit-nodes have i cycles of size girth.
    int cycle_len1;
    vector<std::pair<int,int>> no_cycles_hist2; // The elements (-i,-n) of this vector means that n bit-nodes have i cycles of size girth.
    
    void compute_cycle_hist(vector<std::pair<int,int>> * no_cycles_hist);
    void compute_score(Ccode const * ccode);
};



void remove_cycles(Ccode * ccode, int no_steps, const char * file_name, int delay_saving, int delay_print);


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////    






// class Bfs {
// public:
    
//     Bfs(Ccode* ccode, int u, int w, int girth, bool is_bit);
//     Bfs(const Bfs &); // Not implemented (rule of three)
//     Bfs& operator=(const Bfs &); // Not implemented (rule of three)
//     ~Bfs();

//     int bit_has_been_seen(int bit);
//     int check_has_been_seen(int check);

// private:

//     Ccode const * ccode;
    
//     int* u_to_bit;
//     int* u_to_check;

//     int step_bit_to_check(std::pair<int,int>* edges_seen, int no_edges_seen, std::pair<int,int>* new_edges_seen);
//     int step_check_to_bit(pair<int,int>* edges_seen, int no_edges_seen, pair<int,int>* new_edges_seen);
    
// };


// ///////////////////////////////////////////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////

// class Edge_set {
// public:

//     Edge_set(int max_no_edges);
//     Edge_set(const Edge_set &); // Not implemented (rule of three)
//     Edge_set& operator=(const Edge_set &); // Not implemented (rule of three)
//     ~Edge_set();

//     void clear();

//     void put(int v, int c); // Do not use put once init_pop has been called
//     void init_pop(); 
//     std::pair<int,int> pop(); // Call init_pop before pop
//     std::pair<int,int> last_pop(); // Call init_pop before last_pop
//     int get_no_possible_edges();

//     std::pair<int,int> random_elem(); // No need to call init_pop before that

// private:

//     int* v_array;
//     int* c_array;
//     int size;
//     int last_try;
//     int no_possible_edges;
// };


// ///////////////////////////////////////////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////

// class Find_swap{
// public:
    
//     Find_swap(int no_edges);
//     Find_swap(const Find_swap &); // Not implemented (rule of three)
//     Find_swap& operator=(const Find_swap & L); // Not implemented (rule of three)
//     ~Find_swap();

//     void restart(Ccode const * ccode, mat<int>* path, mat<int>* old_path, int path_len, int max_no_cycles, int const* no_cycles_vector);
//     std::pair<std::pair<int,int>,std::pair<int,int>> random_swap(Ccode* ccode); //ccode must be the same than the one used in restart
//     std::pair<std::pair<int,int>,std::pair<int,int>> return_swap(Ccode* ccode); //ccode must be the same than the one used in restart

//     int get_no_possible_edges1();
//     int get_no_possible_edges2();

// private:

//     int path_len;
//     Edge_set* edge_set1;
//     Edge_set* edge_set2;
    
// };




/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////


// template<typename T>
// class Fifo {
// public:

//     Fifo(int max_size);
//     Fifo(const Fifo<T> &); // Not implemented (rule of three)
//     Fifo<T>& operator=(const Fifo<T> & L); // Not implemented (rule of three)
//     ~Fifo();

//     bool is_empty();
//     void put(T & elem);
//     T pop();

// private:

//     T* elem_array
//     int size
// };

// template<typename T>
// Fifo<T>::Fifo(int max_size) {
//     elem_array = new T[max_size];
//     size = 0;
// }

// Fifo<T>::~Fifo() {
//     delete[] elem_array
// }

// Fifo<T>::Fifo(const Fifo<T>& fifo){
//     throw invalid_argument("Not implemented: trying to copy a fifo");
// }

// Fifo<T> Fifo<T>::operator=(const Fifo<T>&){
//     throw invalid_argument("Not implemented: trying to copy a fifo");
// }

// void Fifo<T>::put(T & elem){
//     elem_array[size] = elem;
//     ++size;
// }

// T Fifo<T>::pop(){
//     --size;
//     return elem_array[size]
// }

// bool Fifo<T>::is_empty() {
//     return size == 0;
// }

#endif
