#include "swap_edges.hpp"
#include "timer.hpp"

using namespace std;


/////////////////////////////////////////////////////////////////////////////////////
//// Score
/////////////////////////////////////////////////////////////////////////////////////




/////////////////////////////////////////////////////////////////////////////////////
// Constructors and destructors
/////////////////////////////////////////////////////////////////////////////////////


// no_cycles_vector is an array of size n with zeros.
Score::Score(Ccode const * ccode, int* no_cycles_vector0){
    
    // max_no_cycles = 0;
    // no_cycles_vector = new int[ccode->n];
    // for (int i = 0; i < ccode->n ;++i){
    // 	no_cycles_vector[i] = 0;
    // }
    no_cycles_vector = no_cycles_vector0;
    path_len = 0;
    path = new mat<int>(ccode->n, ccode->n, 0);
    for (int i = 0; i < ccode->n; ++i)
	(*path)(i,i) = 1;
    old_path = new mat<int>(ccode->n, ccode->m, 0);
    
    
    compute_score(ccode);
}


Score::Score(const Score &) {
    throw invalid_argument("Not implemented: trying to copy a Score");
}

Score& Score::operator=(const Score &){
    throw invalid_argument("Not implemented: trying to copy a Score");
}

Score::~Score(){
    // delete[] no_cycles_vector;
    delete path;
    delete old_path;
}


/////////////////////////////////////////////////////////////////////////////////////
// Functions used to compute the value of the score
/////////////////////////////////////////////////////////////////////////////////////

void Score::compute_cycle_hist(vector<std::pair<int,int>> * no_cycles_hist){
    int n = path->get_no_rows();
    int max_no_cycles = 0;
	
    for (int v1 = 0; v1 < n; ++v1){
	for (int vc = 0; vc < path->get_no_cols(); ++vc){
	    no_cycles_vector[v1] += (*path)(v1,vc) * ((*path)(v1,vc) - 1);
	}
    }
    
    
    for (int v = 0; v < n; ++v) {
	if (no_cycles_vector[v] > max_no_cycles) {
	    max_no_cycles = no_cycles_vector[v];
	}
    }
	
    if (max_no_cycles != 0) {
	int hist[max_no_cycles + 1];
	for (int no_cycles = 0; no_cycles < max_no_cycles + 1; ++no_cycles) { 
	    hist[no_cycles] = 0;
	}
	for (int i = 0; i < n; ++i) { 
	    hist[no_cycles_vector[i]] += 1;
	}
	
	for (int no_cycles = max_no_cycles; no_cycles >= 0; -- no_cycles) {
	    if (hist[no_cycles] != 0) {
		no_cycles_hist->push_back(pair<int,int>(-no_cycles, -hist[no_cycles]));
	    }
	}
	for (int i = 0; i < n; ++i){
	    no_cycles_vector[i] = 0;
	}
    }
}


// no_cycles_vector is an array of size n with zeros.
void Score::compute_score(Ccode const * ccode){
    // no_cycles_hist.clear();
    while (no_cycles_hist1.empty()) {
	path_step(ccode);
	compute_cycle_hist(&no_cycles_hist1);
    }
    
    cycle_len1 = 2*path_len;
	
    if (no_cycles_hist1.back().first == 0) {
	path_step(ccode);
	compute_cycle_hist(&no_cycles_hist2);
    }
}


void Score::path_step(Ccode const * ccode){
    mat<int>* old_old_path = old_path;
    old_path = path;
    if (path_len % 2 == 1){
	path = new mat<int>(ccode->n, ccode->n, 0);
	for (int v1 = 0; v1 < ccode->n; ++v1) {
	    for (int c = 0; c < ccode->m; ++c) {
		for (int i = 0; i < ccode->dc; ++i) {
		    (*path)(v1,ccode->get_check_nbhd(c, i)) += (*old_path)(v1,c);
		}
	    }
	    for (int v2 = 0; v2 < ccode->n; ++v2) {
		(*path)(v1,v2) -= (ccode->dv - 1) * (*old_old_path)(v1,v2);
	    }
	}
    }
    else {
	path = new mat<int>(ccode->n, ccode->m, 0);
	for (int v1 = 0; v1 < ccode->n; ++v1) {
	    for (int v2 = 0; v2 < ccode->n; ++v2) {
		for (int j = 0; j < ccode->dv; ++j) {
		    (*path)(v1,ccode->get_bit_nbhd(v2, j)) += (*old_path)(v1,v2);
		}
	    }
	    for (int c = 0; c < ccode->m; ++c) {
		(*path)(v1,c) -= (ccode->dc - 1) * (*old_old_path)(v1,c);
	    }
	}
    }
    path_len++;
    delete old_old_path;
}


/////////////////////////////////////////////////////////////////////////////////////
// Extra functions
/////////////////////////////////////////////////////////////////////////////////////

int Score::compare(Score* score){
    // cout << endl << endl;
    // print();
    // cout << endl;
    // score->print();
    // cout << endl << endl;
    if (cycle_len1 < score->cycle_len1)
    	return -1;
    if (cycle_len1 > score->cycle_len1)
    	return 1;
    if (no_cycles_hist1 < score->no_cycles_hist1)
	return -1;
    if (no_cycles_hist1 > score->no_cycles_hist1)
	return 1;
    if (no_cycles_hist2 < score->no_cycles_hist2)
	return -1;
    if (no_cycles_hist2 > score->no_cycles_hist2)
	return 1;
    return 0;
}




void Score::print(){
    cout << cycle_len1 << " ";
    for (vector<pair<int,int>>::const_iterator i = no_cycles_hist1.begin(); i != no_cycles_hist1.end(); ++i){
	cout << "(" << (*i).first << ',' << (*i).second << ") ";
    }
    cout << cycle_len1 + 2 << " ";
    for (vector<pair<int,int>>::const_iterator i = no_cycles_hist2.begin(); i != no_cycles_hist2.end(); ++i){
	cout << "(" << (*i).first << ',' << (*i).second << ") ";
    }
    // cout << "(";
    // for (vector<int>::const_iterator i = bad_vertices.begin(); i != bad_vertices.end(); ++i){
    // 	cout << *i << ',';
    // }
    // cout << ")";
}



void remove_cycles(Ccode * ccode, int no_steps, const char * file_name, int delay_saving, int delay_print){
    Timer timer_saving(delay_saving);
    Timer timer_print(delay_print);
    
    int no_cycles_vector[ccode->n];
    for (int i = 0; i < ccode->n; ++i){
	no_cycles_vector[i] = 0;
    }
    Score* score = new Score(ccode, no_cycles_vector);
    Score* best_score = score;
    int steps;
    for (steps = 0; steps < no_steps; ++steps) {
	if (timer_saving.test()) {
	    cout << "\n";
	    remove(file_name);
	    ccode->to_file(file_name);
	}
	if (timer_print.test()) {
	    cout << "\r";
	    cout << "steps = " << steps << "\t score = ";
	    best_score->print();
	    cout << "          " << flush;
	}
	int v1 = rand() % ccode->n;
	int c1 = ccode->get_bit_nbhd(v1, rand() % ccode->dv);
	int v2 = rand() % ccode->n;
	int c2 = ccode->get_bit_nbhd(v2, rand() % ccode->dv);
	ccode->swap_edges(v1,c1,v2,c2);
	
	score = new Score(ccode, no_cycles_vector);
	int comp = best_score->compare(score);
	// cout << endl << comp;
	if (comp < 1) {
	    delete best_score;
	    best_score = score;
	}
	else {
	    delete score;
	    ccode->swap_edges(v1, c2, v2, c1);
	}
    }
    cout << "\n";
    cout << "Final: "; 
    cout << "steps = " << steps << "\t score = ";
    best_score->print();
    cout << "\n";
    delete best_score;
}



/////////////////////////////////////////////////////////////////////////////////////
// Functions used to find a good swap
/////////////////////////////////////////////////////////////////////////////////////

// // ccode must be the code used to initialize the class
// tuple<int,int,int,int> Score::return_swap(Ccode const * ccode){
//     int v1 = bad_vertices[rand() % bad_vertices.size()];
//     int c1 = ccode->get_bit_nbhd(v1, rand() % ccode->dv);
//     int v2 = rand() % ccode->n;
//     int c2 = ccode->get_bit_nbhd(v2, rand() % ccode->dv);
//     return make_tuple(v1,c1,v2,c2);
// }


// // ccode must be the code used to initialize the class
// void Score::restart_find_swap(Find_swap* find_swap, Ccode const * ccode) {
//     find_swap->restart(ccode, path, old_path, path_len, max_no_cycles, no_cycles_vector);
// }



/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////
//// Edge_set
/////////////////////////////////////////////////////////////////////////////////////




// Edge_set::Edge_set(int max_no_edges) {
//     v_array = new int[max_no_edges];
//     c_array = new int[max_no_edges];
//     size = 0;
//     last_try = 0;
//     no_possible_edges = 0;
// }

// Edge_set::~Edge_set() {
//     delete[] v_array;
//     delete[] c_array;
// }

// Edge_set::Edge_set(const Edge_set&){
//     throw invalid_argument("Not implemented: trying to copy a Edge_set");
// }

// Edge_set& Edge_set::operator=(const Edge_set&){
//     throw invalid_argument("Not implemented: trying to copy a Edge_set");
// }

// void Edge_set::clear(){
//     size = 0;
//     last_try = 0;
//     no_possible_edges = 0;
// }

// void Edge_set::put(int v, int c){
//     v_array[size] = v;
//     c_array[size] = c;
//     ++size;
// }

// // Be carrefull: size must be != 0
// void Edge_set::init_pop() {
//     last_try = rand() % size;
//     no_possible_edges = size;
// }

// pair<int,int> Edge_set::pop(){
//     no_possible_edges--;
//     last_try = (last_try + 1) % size;
//     return pair<int,int>(v_array[last_try], c_array[last_try]);
// }


// pair<int,int> Edge_set::last_pop(){
//     return pair<int,int>(v_array[last_try], c_array[last_try]);
// }

// // No need to call init_pop before that
// pair<int,int> Edge_set::random_elem(){
//     int i = rand() % size;
//     return pair<int,int>(v_array[i], c_array[i]);
// }


// int Edge_set::get_no_possible_edges(){
//     return no_possible_edges;
// }


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////


/////////////////////////////////////////////////////////////////////////////////////
//// Bfs
/////////////////////////////////////////////////////////////////////////////////////




// Bfs::Bfs(Ccode* ccode0, int u, int w, int girth, bool is_bit): ccode(ccode0){
//     u_to_bit = new int[ccode->n];
//     for (int i = 0; i < ccode->n; ++i){
// 	u_to_bit[i] = -1;
//     }
    
//     u_to_check = new int[ccode->m];
//     for (int i = 0; i < ccode->m; ++i){
// 	u_to_check[i] = -1;
//     }

//     if (girth > 2) {
// 	if (is_bit) {
// 	    u_to_bit[u] = u;
// 	    pair<int,int> bit_check_edges_seen[ccode->m];
// 	    pair<int,int> check_bit_edges_seen[ccode->n];
// 	    int no_edges_seen = 0;
	
// 	    for (int i = 0; i < ccode->dv; ++i) {
// 		int check = ccode->get_bit_nbhd(u,i);
// 		if (w != check) {
// 		    bit_check_edges_seen[no_edges_seen] = pair<int,int>(u,check);
// 		    ++no_edges_seen;
// 		    u_to_check[check] = u;
// 		}
// 	    }
// 	    for (int step = 0; step < girth/2 - 2; ++step){
// 		no_edges_seen = step_check_to_bit(bit_check_edges_seen, no_edges_seen, check_bit_edges_seen);
// 		no_edges_seen = step_bit_to_check(check_bit_edges_seen, no_edges_seen, bit_check_edges_seen);
// 	    }
// 	}
// 	else {
// 	    u_to_check[u] = u;
// 	    pair<int,int> bit_check_edges_seen[ccode->m];
// 	    pair<int,int> check_bit_edges_seen[ccode->n];
// 	    int no_edges_seen = 0;
	
// 	    for (int i = 0; i < ccode->dc; ++i) {
// 		int bit = ccode->get_check_nbhd(u,i);
// 		if (w != bit) {
// 		    check_bit_edges_seen[no_edges_seen] = pair<int,int>(u,bit);
// 		    ++no_edges_seen;
// 		    u_to_bit[bit] = u;
// 		}
// 	    }
// 	    for (int step = 0; step < girth/2 - 2; ++step){
// 		no_edges_seen = step_bit_to_check(check_bit_edges_seen, no_edges_seen, bit_check_edges_seen);
// 		no_edges_seen = step_check_to_bit(bit_check_edges_seen, no_edges_seen, check_bit_edges_seen);
// 	    }
// 	}
//     }
// }

// Bfs::~Bfs() {
//     delete[] u_to_check;
//     delete[] u_to_bit;
// }

// Bfs::Bfs(const Bfs& bfs): ccode(bfs.ccode){
//     throw invalid_argument("Not implemented: trying to copy a Bfs");
// }

// Bfs& Bfs::operator=(const Bfs&){
//     throw invalid_argument("Not implemented: trying to copy a Bfs");
// }

// int Bfs::step_bit_to_check(pair<int,int>* edges_seen, int no_edges_seen, pair<int,int>* new_edges_seen){
//     int new_no_edges_seen = 0;
//     for (int i = 0; i < no_edges_seen; ++i) {
// 	pair<int,int> edge = edges_seen[i];
// 	int check = edge.first;
// 	int bit = edge.second;
// 	for (int j = 0; j < ccode->dv; ++j) {
// 	    int new_check = ccode->get_bit_nbhd(bit,j);
// 	    if (check != new_check) {
// 		if (u_to_check[new_check] == -1) {
// 		    u_to_check[new_check] = bit;
// 		    new_edges_seen[new_no_edges_seen] = pair<int,int>(bit,new_check);
// 		    ++new_no_edges_seen;
// 		}
// 		else{
// 		    u_to_check[new_check] = ccode->m;
// 		}
// 	    }
// 	}
//     }
//     return new_no_edges_seen;
// }


// int Bfs::step_check_to_bit(pair<int,int>* edges_seen, int no_edges_seen, pair<int,int>* new_edges_seen){
//     int new_no_edges_seen = 0;
//     for (int i = 0; i < no_edges_seen; ++i) {
// 	pair<int,int> edge = edges_seen[i];
// 	int bit = edge.first;
// 	int check = edge.second;
// 	for (int j = 0; j < ccode->dc; ++j) {
// 	    int new_bit = ccode->get_check_nbhd(check,j);
// 	    if (bit != new_bit) {
// 		if (u_to_bit[new_bit] == -1) {
// 		    u_to_bit[new_bit] = check;
// 		    new_edges_seen[new_no_edges_seen] = pair<int,int>(check,new_bit);
// 		    ++new_no_edges_seen;
// 		}
// 		else{
// 		    u_to_bit[new_bit] = ccode->m;
// 		}
// 	    }
// 	}
//     }
//     return new_no_edges_seen;
// }


// int Bfs::bit_has_been_seen(int bit){
//     return u_to_bit[bit];
// }


// int Bfs::check_has_been_seen(int check){
//     return u_to_check[check];
// }


/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////


/////////////////////////////////////////////////////////////////////////////////////
//// Find_swap
/////////////////////////////////////////////////////////////////////////////////////





// Find_swap::Find_swap(int no_edges) {
//     edge_set1 = new Edge_set(no_edges);
//     edge_set2 = new Edge_set(no_edges);
// }

// Find_swap::~Find_swap() {
//     delete edge_set1;
//     delete edge_set2;
// }

// Find_swap::Find_swap(const Find_swap&){
//     throw invalid_argument("Not implemented: trying to copy a Find_swap");
// }

// Find_swap& Find_swap::operator=(const Find_swap&){
//     throw invalid_argument("Not implemented: trying to copy a Find_swap");
// }

// void Find_swap::restart(Ccode const * ccode, mat<int>* path, mat<int>* old_path, int path_len0, int max_no_cycles, int const * no_cycles_vector){
//     path_len = path_len0;
//     edge_set1->clear();
//     edge_set2->clear();
//     if (path_len % 2 == 0) {
// 	for (int v = 0; v < ccode->n; ++v) {
// 	    if (no_cycles_vector[v] == max_no_cycles)
// 		{
// 		int no_possible_c = ccode->dv;
// 		int possible_c[ccode->dv];
// 		for (int i = 0; i < ccode->dv; ++i) {
// 		    possible_c[i] = ccode->get_bit_nbhd(v,i);
// 		}
		
// 		for (int v0 = 0; v0 < ccode->n; ++v0) {
// 		    if ((*path)(v0,v) > 1) {
// 			int i = 0;
// 			while(i < no_possible_c){
// 			    if ((*old_path)(v0,possible_c[i]) > 0) {
// 				edge_set1->put(v,possible_c[i]);
// 				no_possible_c--;
// 				possible_c[i] = possible_c[no_possible_c];
// 			    }
// 			    else {
// 				i++;
// 			    }
// 			}
// 		    }		    
// 		}
// 	    }
// 	}
//     }
    
//     else {
// 	for (int c = 0; c < ccode->m; ++c) {
// 	    int no_possible_v = 0;
// 	    int possible_v[ccode->dc];
// 	    for (int i = 0; i < ccode->dc; ++i) {
// 		if (no_cycles_vector[ccode->get_check_nbhd(c,i)] == max_no_cycles)
// 		    {
// 		    possible_v[no_possible_v] = ccode->get_check_nbhd(c,i);
// 		    ++no_possible_v;
// 		}		
// 		for (int v0 = 0; v0 < ccode->n; ++v0) {
// 		    if ((*path)(v0,c) > 1) {
// 			int i = 0;
// 			while(i < no_possible_v){
// 			    if ((*old_path)(v0,possible_v[i]) > 0) {
// 				edge_set1->put(possible_v[i],c);
// 				no_possible_v--;
// 				possible_v[i] = possible_v[no_possible_v];
// 			    }
// 			    else {
// 				i++;
// 			    }
// 			}
// 		    }	
// 		}
	
// 	    }
// 	}
//     }
//     edge_set1->init_pop();
// }




// //ccode must be the same than the one used in restart
// pair<pair<int,int>,pair<int,int>> Find_swap::random_swap(Ccode* ccode){
//     pair<int,int> edge1 = edge_set1->random_elem();
//     int v2 = rand() % ccode->n;
//     int c2 = ccode->get_bit_nbhd(v2, rand() % ccode->dv);
//     pair<int,int> edge2 = pair<int,int>(v2,c2);
//     return pair<pair<int,int>,pair<int,int>>(edge1,edge2);
// }




// //ccode must be the same than the one used in restart
// pair<pair<int,int>,pair<int,int>> Find_swap::return_swap(Ccode* ccode){
//     if (get_no_possible_edges2() == 0) {
// 	if (get_no_possible_edges1() == 0) {
// 	    return pair<pair<int,int>,pair<int,int>>(pair<int,int>(-1,-1),pair<int,int>(-1,-1));
// 	}
// 	pair<int,int> edge1 = edge_set1->pop();
// 	edge_set2->clear();
// 	int v1 = edge1.first;
// 	int c1 = edge1.second;

// 	Bfs bfs_v(ccode, v1, c1, 2*path_len, true);
// 	Bfs bfs_c(ccode, c1, v1, 2*path_len, false);

// 	for (int v2 = 0; v2 < ccode->n; ++v2) {
// 	    int forbiden_check = bfs_c.bit_has_been_seen(v2);
// 	    for (int i = 0; i < ccode->dv; ++i) {
// 		int c2 = ccode->get_bit_nbhd(v2,i);
// 		if (c2 != forbiden_check && v2 != bfs_v.check_has_been_seen(c2)) {
// 		    edge_set2->put(v2,c2);
// 		}
// 	    }
// 	}
// 	edge_set2->init_pop();
//     }
//     pair<int,int> edge1 = edge_set1->last_pop();
//     pair<int,int> edge2 = edge_set2->pop();
//     return pair<pair<int,int>,pair<int,int>> (edge1, edge2);
// }


// int Find_swap::get_no_possible_edges1(){
//     return edge_set1->get_no_possible_edges();
// }

// int Find_swap::get_no_possible_edges2(){
//     return edge_set2->get_no_possible_edges();
// }

    
// /////////////////////////////////////////////////////////////////////////////////////
// /////////////////////////////////////////////////////////////////////////////////////
// /////////////////////////////////////////////////////////////////////////////////////
// /////////////////////////////////////////////////////////////////////////////////////
// /////////////////////////////////////////////////////////////////////////////////////
// /////////////////////////////////////////////////////////////////////////////////////


// #define FIND_SWAP 3
// // 1: tester tous les swaps possibles
// // 2: ?
// // 3: prendre swap aleatoire

// #if FIND_SWAP==1
// void remove_cycles(Ccode * ccode, int){
//     Timer timer_print(1);
//     Find_swap find_swap(ccode->n * ccode->dv);
//     Score* score = new Score(ccode);
//     Score* best_score = score;
//     best_score->restart_find_swap(& find_swap, ccode);
//     while (find_swap.get_no_possible_edges1() > 0 or find_swap.get_no_possible_edges2() > 0 ) {
// 	if (timer_print.test()) {
// 	    cout << "\r";
// 	    cout << "no_edges1 = " << find_swap.get_no_possible_edges1();
// 	    cout << "   no_edges2 = " << find_swap.get_no_possible_edges2();
// 	    cout << "    score = ";
// 	    best_score->print();
// 	    cout << "          " << flush;
// 	}
// 	pair<pair<int,int>,pair<int,int>> swap = find_swap.return_swap(ccode);
// 	int v1 = swap.first.first;
// 	int c1 = swap.first.second;
// 	int v2 = swap.second.first;
// 	int c2 = swap.second.second;
// 	ccode->swap_edges(v1,c1,v2,c2);
	
// 	score = new Score(ccode);
// 	if (best_score->lt(score)) {
// 	    delete best_score;
// 	    best_score = score;
// 	    best_score->restart_find_swap(& find_swap, ccode);
// 	}
// 	else {
// 	    delete score;
// 	    ccode->swap_edges(v1, c2, v2, c1);
// 	}
//     }
//     cout << "\n";
//     cout << "Final: "; 
//     cout << "no_edges1 = " << find_swap.get_no_possible_edges1();
//     cout << "   no_edges2 = " << find_swap.get_no_possible_edges2();
//     cout << "    score = ";
//     best_score->print();
//     cout << "          " << flush;
//     cout << "\n";
//     delete best_score;
// }
// #endif

// #if FIND_SWAP==2
// void remove_cycles(Ccode * ccode, int no_steps){
//     Timer timer_print(1);
//     Find_swap* find_swap = new Find_swap(ccode->n * ccode->dv);
//     Score* score = new Score(ccode);
//     Score* best_score = score;
//     best_score->restart_find_swap(find_swap, ccode);
//     int steps;
//     for (steps = 0; steps < no_steps; ++steps) {
// 	if (timer_print.test()) {
// 	    cout << "\r";
// 	    cout << "steps = " << steps << "\t score = ";
// 	    best_score->print();
// 	    cout << "          " << flush;
// 	}
// 	pair<pair<int,int>,pair<int,int>> swap = find_swap->random_swap(ccode);
// 	int v1 = swap.first.first;
// 	int c1 = swap.first.second;
// 	int v2 = swap.second.first;
// 	int c2 = swap.second.second;
// 	ccode->swap_edges(v1,c1,v2,c2);
	
// 	score = new Score(ccode);
// 	if (best_score->lt(score)) {
// 	    delete best_score;
// 	    best_score = score;
// 	    best_score->restart_find_swap(find_swap, ccode);
// 	}
// 	else {
// 	    delete score;
// 	    ccode->swap_edges(v1, c2, v2, c1);
// 	}
//     }
//     cout << "\n";
//     cout << "Final: "; 
//     cout << "steps = " << steps << "\t score = ";
//     best_score->print();
//     cout << "\n";
//     delete best_score;
//     delete find_swap;
// }
// #endif


// #if FIND_SWAP==3
// void remove_cycles(Ccode * ccode, int no_steps){
//     string file_name0 = "ccode/" + ccode->id + ".code";
//     const char * file_name = file_name0.c_str();
//     Timer timer_saving(60);
//     Timer timer_print(1);
//     Score* score = new Score(ccode);
//     Score* best_score = score;
//     int steps;
//     for (steps = 0; steps < no_steps; ++steps) {
// 	if (timer_saving.test()) {
// 	    cout << "\n";
// 	    remove(file_name);
// 	    ccode->to_file(file_name);
// 	}
// 	if (timer_print.test()) {
// 	    cout << "\r";
// 	    cout << "steps = " << steps << "\t score = ";
// 	    best_score->print();
// 	    cout << "          " << flush;
// 	}
// 	int v1 = rand() % ccode->n;
// 	int c1 = ccode->get_bit_nbhd(v1, rand() % ccode->dv);
// 	int v2 = rand() % ccode->n;
// 	int c2 = ccode->get_bit_nbhd(v2, rand() % ccode->dv);
// 	ccode->swap_edges(v1,c1,v2,c2);
	
// 	score = new Score(ccode);
// 	if (best_score->lteq(score)) {
// 	    delete best_score;
// 	    best_score = score;
// 	}
// 	else {
// 	    delete score;
// 	    ccode->swap_edges(v1, c2, v2, c1);
// 	}
//     }
//     cout << "\n";
//     cout << "Final: "; 
//     cout << "steps = " << steps << "\t score = ";
//     best_score->print();
//     cout << "\n";
//     delete best_score;
// }
// #endif



/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////



/////////////////////////////////////////////////////////////////////////////////////
//// Dijkstra
/////////////////////////////////////////////////////////////////////////////////////

// Replaces the first occurence of "a" by "b" in "v"
// Be carefull: if "a" is not in "v" => seg fault

// void Dijkstra::delete_attributes() {
//     delete path;
//     delete old_path;
// }

// void Dijkstra::init_attributes() {
//     path_len = 0;
//     path = new mat<int>(ccode->n, ccode->n, 0);
//     for (int i = 0; i < ccode->n; ++i)
// 	(*path)(i,i) = 1;
//     old_path = new mat<int>(ccode->n, ccode->m, 0);
// }

// Dijkstra::Dijkstra(Ccode * ccode0) {
//     ccode = ccode0;
//     init_attributes();
// }

// Dijkstra::Dijkstra(const Dijkstra &) {
//     throw invalid_argument("Not implemented: trying to copy a Dijkstra");
// }

// Dijkstra& Dijkstra::operator=(const Dijkstra &){
//     throw invalid_argument("Not implemented: trying to copy a Dijkstra");
// }

// Dijkstra::~Dijkstra(){
//     delete_attributes();
// }

// void Dijkstra::dijkstra_step(){
//     mat<int>* old_old_path = old_path;
//     old_path = path;
//     if (path_len % 2 == 1){
// 	path = new mat<int>(ccode->n, ccode->n, 0);
// 	for (int v1 = 0; v1 < ccode->n; ++v1) {
// 	    for (int c = 0; c < ccode->m; ++c) {
// 		for (int i = 0; i < ccode->dc; ++i) {
// 		    (*path)(v1,ccode->get_check_nbhd(c, i)) += (*old_path)(v1,c);
// 		}
// 	    }
// 	    for (int v2 = 0; v2 < ccode->n; ++v2) {
// 		(*path)(v1,v2) -= (ccode->dv - 1) * (*old_old_path)(v1,v2);
// 	    }
// 	}
//     }
//     else {
// 	path = new mat<int>(ccode->n, ccode->m, 0);
// 	for (int v1 = 0; v1 < ccode->n; ++v1) {
// 	    for (int v2 = 0; v2 < ccode->n; ++v2) {
// 		for (int j = 0; j < ccode->dv; ++j) {
// 		    (*path)(v1,ccode->get_bit_nbhd(v2, j)) += (*old_path)(v1,v2);
// 		}
// 	    }
// 	    for (int c = 0; c < ccode->m; ++c) {
// 		(*path)(v1,c) -= (ccode->dc - 1) * (*old_old_path)(v1,c);
// 	    }
// 	}
//     }
//     path_len++;
//     delete old_old_path;
// }


// Score Dijkstra::compute_score(){
//     dijkstra_step();
//     Score score(ccode, path_len, *path);
//     while (!score.is_relevant()) {
// 	dijkstra_step();
// 	score = Score(ccode, path_len, *path);
//     }
//     return score;
// }

/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////
