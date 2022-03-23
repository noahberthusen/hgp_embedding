#ifndef CCODE
#define CCODE

#include "../mat.h"


class Ccode
{
public:

    int n, m, dv, dc;
    std::string id;
    
    Ccode(int N, int M, int DV, int DC);
    Ccode(char const * file_name, int code_index);
    Ccode(const Ccode& ccode); // Not implemented (rule of three)
    Ccode operator=(const Ccode& ccode); // Not implemented (rule of three)
    ~Ccode();
    void to_file(std::string file_name);
    void swap_edges(int v1, int c1, int v2, int c2);

    int get_bit_nbhd(int v, int i) const;
    int get_check_nbhd(int c, int i) const;
    
private:

    mat<int>* bit_nbhd;
    mat<int>* check_nbhd;

};

#endif
