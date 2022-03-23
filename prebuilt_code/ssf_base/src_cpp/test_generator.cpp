#include <iostream>
#include <math.h>
#include "generator.h"


// To-do: remove this function, it appears on lookup_table.cpp

void compute_gray_code(vector<int> &gray_code, int begin, int end, int dv) {
    /*
    Starting from 0^dv, if you flip the bits res[0], res[1], ..., res[dv-2] then you go through {0,1}^dv
    */
    if (dv > 0) {
      int mid = (begin + end)/2;
        // int mid = (end + begin)/2;
	// cout << "mid  " << mid << " " << dv-1 << endl;
        gray_code[mid] = dv - 1;
        compute_gray_code(gray_code,begin,mid-1,dv-1);
        compute_gray_code(gray_code,mid+1,end,dv-1);
    }
}




// To-do: further tests
int main() {
  int c1 = 0;
  int v2 = 0;
  int dc = 6;
  int dv = 4;
  int size_gray = pow(2,dv)-1;

  vector<int> gray_code(size_gray,0);
  
  compute_gray_code(gray_code, 0, size_gray-1, dv);
  // cout << size_gray << " || ";
  // for (int z = 0; z < size_gray; z++) {
  //   cout << gray_code[z] << " ";
  // }

  
  mat<bool> synd_gen(dc,dv,false);
  synd_gen(0,0) = true;
  synd_gen(0,1) = true;
  synd_gen(0,2) = true;
  synd_gen(0,3) = true;
  
  // synd_gen(1,0) = true;
  // synd_gen(2,0) = true;
  // synd_gen(3,0) = true;
  // synd_gen(4,0) = true;
  // synd_gen(5,0) = true;
  
  // synd_gen(5,0) = true;
  // synd_gen(5,0) = true;
  // synd_gen(5,0) = true;

  
  generator g = generator(c1,v2,dc,dv,&synd_gen);
  g.score_gen(gray_code);
  
  cout << "synd diff:" << g.best_synd_diff << " " << g.best_weight << endl;
  for (int i = 0; i < dc; ++i) {
    if (g.best_ver_flips[i]) {
      cout << i << " ";
    }
  }
  cout << endl;
  for (int i = 0; i < dv; ++i) {
    if (g.best_hor_flips[i]) {
      cout << i << " ";
    }
  }
  cout << endl;
    
  
  return 0;
}
