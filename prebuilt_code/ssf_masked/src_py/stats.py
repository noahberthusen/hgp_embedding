import sys
import default_names
from print_erase import*
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
file_name_list = ["../ccode/36_30_5_6.code"]
# file_name_list = ["../ccode/20_15_3_4.code"]
# file_name_list = ["../ccode/7_3_1_4.code"]
# file_name_list = ["../ccode/16_12_3_4.code"]

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


def get_error():
    # error = ([(4, 5), (6, 3), (4, 0), (34, 15), (3, 13), (28, 10), (6, 5), (7, 32), (6, 25), (34, 9), (27, 14)], [(12, 22), (24, 13), (26, 5), (29, 6)]) #0.789
    error = ([(0, 9), (6, 0), (6, 4), (2, 15), (9, 9), (7, 15), (16, 35)], [(22, 0), (10, 3), (3, 16), (24, 2), (23, 25), (7, 21), (17, 24), (23, 10)]) #1
    return error

if __name__ == "__main__":
    start = time.time()
    code_list = read_ccode(file_name_list, n_list, m_list, dv_list, dc_list, id_list)
    rs = []
    # code_list = code_list[:no_codes]
    if len(code_list) == 0:
        raise NameError('No such code')
    
    for i in range(len(code_list)):

        ccode = code_list[i]
        logical2 = decoder.Logical2(ccode)
        
        s = " dv = " + str(ccode.dv) + ", dc = " + str(ccode.dc) + ", n = " + str(ccode.n) + ", m = " + str(ccode.m)
        print("Code " + str(i+1) + s)

        error = get_error()
        synd_matrix = decoder.compute_synd_matrix(ccode, error)
        print(f"Syndrome weight: {np.count_nonzero(synd_matrix)}")
        print(f"Maximum possible syndrome weight: {len(error[0])*ccode.dv + len(error[1])*ccode.dc}")