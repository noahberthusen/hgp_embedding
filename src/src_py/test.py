import sys
import default_names
from print_erase import*
import decoder_list
import decoder
from read_ccodes import read_ccode
from read_result import Result, save_new_res
# import resource
import numpy as np
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
# file_name_list = ["../ccode/36_30_5_6.code"]
# file_name_list = ["../ccode/swap3_120_100_5_6.code"]
# file_name_list = ["../ccode/20_15_3_4.code"]
# file_name_list = ["../ccode/7_3_1_4.code"]
file_name_list = ["../ccode/16_12_3_4.code"]

###########################################################
# Simulation parameters
###########################################################
# Change this value for another algorithm (for example for the parallel version)
algo = 1
# P = [0.0025 * k for k in range(15,16)]
# P = [0.05,0.06,0.07]
# P = [6,7]
S = [6]
maskP = [0.1]
no_runs = 10000
no_errors = 10
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
def run_algo(algo, ccode, error, mask, logical2, k):
    # Bit-flip on classical code
    if algo == 0 or algo == -1:
        return run_flip_ccode(ccode, 0.05, algo)
    elif algo == 1:
        return decoder.run_algo_qcode(ccode, error, mask, logical2)
    elif algo == 2:
        return decoder_list.run_algo_qcode(ccode, error, mask, logical2, k)
    else:
        raise NameError('This algo number does not exist')

def print_array(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if (not arr[i][j]):
                print(f"({i},{j}) ")

def get_error():
    return ([(11, 5), (5, 4), (6, 1), (6, 13)], [(10, 4), (11, 4)])
    
def main_laptop():
    start = time.time()
    code_list = read_ccode(file_name_list, n_list, m_list, dv_list, dc_list, id_list)
    rs = []
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

        for s in S:
            for p_mask in maskP:
                for i in range(no_errors):
                    print_erase = Print_erase(0)
                    no_success = 0
                    no_stop = 0
                    cont = 0
                    rs = []
                    while (not cont):
                        error = decoder.random_sized_error(ccode, s)
                        mask = decoder.random_mask(ccode, 0)
                        res = run_algo(algo, ccode, error, mask, logical2, 2)
                        if res == 2:
                            pass
                        else:
                            if (res):
                                cont = 1
                    # error = get_error()
                    # print(error)
                    for test in range(no_runs):
                        # error = decoder.random_error(ccode, p)
                        # error = decoder.random_sized_error(ccode, 2)
                        mask = decoder.random_mask(ccode, p_mask)
                        print_erase.print(str(s) + " " + str(p_mask*100) + "% : " + "Run number: " + str(test+1) + "/" + str(no_runs) + "\tResult: " + str(no_success) + " (" + str(no_stop) + " :synd != 0)")
                        res = run_algo(algo, ccode, error, mask, logical2, 2)
                        if res == 2:
                            print_array(mask)
                            r = Result(i,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,s,p_mask,1,0,1)
                        else:
                            if (not res):
                                print_array(mask)
                            r = Result(i,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,s,p_mask,1,res,0)
                        no_stop = no_stop + r.no_stop
                        no_success = no_success + r.no_success
                        rs.append(r)
                    save_new_res(args.o, rs)
                    print_erase.print("Final result for " + str(s) + " " + str(p_mask*100) + "% : "
                                    + str(no_success) + "/" + str(no_runs) + " (" + str(no_stop) + " :synd != 0)")
                    del print_erase
        
        
        
        # for p in P:
        #     for p_mask in maskP:
        #         print_erase = Print_erase(0)
        #         no_success = 0
        #         no_stop = 0
        #         rs = []
        #         for test in range(no_runs):
        #             # error = decoder.random_error(ccode, p)
        #             error = decoder.random_sized_error(ccode, 2)
        #             mask = decoder.random_mask(ccode, p_mask)
        #             print_erase.print(str(p*100) + "% " + str(p_mask*100) + "% : " + "Run number: " + str(test+1) + "/" + str(no_runs) + "\tResult: " + str(no_success) + " (" + str(no_stop) + " :synd != 0)")
        #             res = run_algo(algo, ccode, error, mask, logical2, 2)
        #             if res == 2:
        #                 print('2', error)
        #                 r = Result(algo,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,p_mask,1,0,1)
        #             else:
        #                 # if (not res):
        #                     # print('0', error)
        #                 r = Result(algo,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,p_mask,1,res,0)
        #             no_stop = no_stop + r.no_stop
        #             no_success = no_success + r.no_success
        #             rs.append(r)
        #         save_new_res(args.o, rs)
                    
            
        #         print_erase.print("Final result for " + str(p*100) + "% " + str(p_mask*100) + "% : "
        #                         + str(no_success) + "/" + str(no_runs) + " (" + str(no_stop) + " :synd != 0)")
        #         del print_erase
            
    stop = time.time()
    print("Time taken: " + str(stop - start) + "\n")







print("output file = " + args.o)
main_laptop()