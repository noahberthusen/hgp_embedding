import sys
import default_names
from print_erase import*
import decoder_list
import decoder
from read_ccodes import read_ccode
from read_result import Result, save_new_res
# import resource
import time
import uuid
import argparse
import glob
from flip import run_flip_ccode

###########################################################
# Code parameters
###########################################################
# n_list = [] if you do not want to use this option
n_list = []
m_list = []
dv_list = []
dc_list = []
# Don't forget "" for the id_list
# id_list = ["62451bf5","0c350536","ee718ff0","77ef9586"]
# id_list = ["swap_566a5203","swap_21c6740d","swap_ca41e16b","swap_a501cc2e","swap_12f5a4a2", "swap_82698d8d", "swap_2e55c0b2", "swap_877f956a", "swap_54d39ebd", "swap_b5f4dc91","swap_c9cc9a21","swap_5ca99d9d","swap_3975e341","swap_dee99e3d","swap_8cab59e4", "swap_48aae4fa","swap_24daeba6","swap_0c8ee978","swap_3deb9a09","swap_48aae4fa","swap_93d4cf34"]
# id_list = ["swap_ede32c1d","swap_6fb0da08"]
id_list = []
# file_name_list = ["../ccode/60_50_5_6.code"]
# file_name_list = ["../ccode/swap3_120_100_5_6.code"]
file_name_list = ["../ccode/16_12_3_4.code"]

###########################################################
# Simulation parameters
###########################################################
# Change this value for another algorithm (for example for the parallel version)
algo = 2
# P = [0.0025 * k for k in range(15,16)]
# P = [0.05,0.06,0.07]
P = [0.015]
maskP = [0]
no_runs = 5
###########################################################



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', default = default_names.res_file_name, help = "file where we store the results")
    parser.add_argument('-i', default = glob.glob(default_names.ccode_dir + '/*.code'), nargs = '+', help = "files where we store the codes. e.g -i ccode/*.code")
    parser.add_argument('-t', default = 0, type=int,help = "Minimum time in seconds between two saving of results.")
    args = parser.parse_args()

# Returns true when algo decodes a quantum code and False if it decode the classical code
def is_quantum(algo):
    return algo != 0


# This function chooses the decoding algorithm.
# Input: 'algo' is the algorithm to run; 'ccode' is the classical code we use; 'p' is the probability of flip; 'logical2' is an object of the class 'Logical2' used to test logical errors
# Output: 1 if corrected, 2 if non zero syndrome and 0 if logical error
def run_algo(algo, ccode, p, maskp, logical2):
    # Bit-flip on classical code
    if algo == 0 or algo == -1:
        return run_flip_ccode(ccode, p, algo)
    elif algo == 1:
        return decoder.run_algo_qcode(ccode, p, maskp, logical2)
    elif algo == 2:
        return decoder_list.run_algo_qcode(ccode, p, maskp, logical2, 3)
    else:
        raise NameError('This algo number does not exist')


    
def main_laptop():
    start = time.time()
    code_list = read_ccode(file_name_list, n_list, m_list, dv_list, dc_list, id_list)
    # code_list = code_list[:no_codes]
    if len(code_list) == 0:
        raise NameError('No such code')
    
    for i in range(len(code_list)):

        ccode = code_list[i]
        if is_quantum(algo):
            logical2 = decoder.Logical2(ccode)
        else:
            logical2 = None
        
        s = "dv = " + str(ccode.dv) + " ,dc = " + str(ccode.dc) + " ,n = " + str(ccode.n) + " ,m = " + str(ccode.m)
        print("Code " + str(i+1) + s)

        for p in P:
            for p_mask in maskP:
                print_erase = Print_erase(0)
                no_success = 0
                no_stop = 0
                for test in range(no_runs):
                    print_erase.print(str(p*100) + "% " + str(p_mask*100) + "% : " + "Run number: " + str(test+1) + "/" + str(no_runs) + "\tResult: " + str(no_success) + " (" + str(no_stop) + " :synd != 0)")
                    res = run_algo(algo, ccode, p, p_mask, logical2)
                    if res == 2:
                        r = Result(algo,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,p_mask,1,0,1)
                    else:
                        r = Result(algo,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,p_mask,1,res,0)
                    no_stop = no_stop + r.no_stop
                    no_success = no_success + r.no_success
                    save_new_res(args.o, [r])
                    
            
                print_erase.print("Final result for " + str(p*100) + "% " + str(p_mask*100) + "% : "
                                + str(no_success) + "/" + str(no_runs) + " (" + str(no_stop) + " :synd != 0)")
                del print_erase
            
    stop = time.time()
    print("Time taken: " + str(stop - start) + "\n")




    

# def main():
#     code_list = read_ccode(args.i, n_list, m_list, dv_list, dc_list, id_list)
#     logical_list = [Logical2(ccode) for ccode in code_list]

#     if len(code_list) == 0:
#         raise NameError('No such code')
#     print("number codes: ", len(code_list))

#     saving_time = time.time()
#     res_list = []

#     for _ in range(no_runs):
#         for p in P:
#             for i_code in range(len(code_list)):
#                 ccode = code_list[i_code]
#                 if is_quantum(algo):
#                     logical2 = logical_list[i_code]
#                 else:
#                     logical2 = None
#                 res = run_algo(algo, ccode, p, logical2)
#                 if res == 2:
#                     r = Result(algo,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,1,0,1)
#                 else:
#                     r = Result(algo,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,1,res,0)
                    
#                 res_list.append(r)
#                 if time.time() - saving_time > args.t:
#                     saving_time = time.time()
#                     save_new_res(args.o,res_list)
#                     res_list = []






print("output file = " + args.o)
main_laptop()