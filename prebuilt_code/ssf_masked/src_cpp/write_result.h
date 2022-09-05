#ifndef DEF_RESULT
#define DEF_RESULT
#include<vector>

class Result
{
 public:
  
  Result(int algo,int dv,int dc,int n,int m,std::string code_id,double p_phys,double p_mask,int no_test,int no_success,int no_stop);
  Result(std::string line);
  std::string to_line();
  bool test_combine_res(Result r);
  // Be carefull: use this function only if test_combine_res(r1, r2) is true
  Result combine_res(Result r);
    
 private:
  
  int algo, dv, dc, n, m;
  std::string code_id;
  double p_phys, p_mask;
  int no_test, no_success, no_stop;
  
};

class Result_ensemble
{
 public:

    void add_result(Result r);
    void add_result(int algo,int dv,int dc,int n,int m,std::string code_id,double p_phys,double p_mask,int no_test,int no_success,int no_stop);
    // Hypothesis: the file exists
    void add_file(const std::string file_name);
    // Deletes file_name
    void to_file(const std::string file_name);
    
 private:
    
    vector<Result> result_vector;
    
};


/* void save_new_res(std::string file_name, int algo,int dv,int dc,int n,int m,std::string code_id,double p_phys,int no_test,int no_success,int no_stop); */


#endif
