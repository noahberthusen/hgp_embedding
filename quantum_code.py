import numpy as np
from lookup_table_cy import LookupTable, MaskedLookupTable
# from masked_lookup_table_cy import MaskedLookupTable
from classical_code import *

class QuantumCode(object):
    def __init__(self, ccode):
        self.ccode = ccode
        self.dv = ccode.dv
        self.dc = ccode.dc


    def compute_synd_matrix(self, error):
        """
        Returns the syndrome of the list of errors
        """
        v1 = 0
        v2 = 0
        c1 = 0
        c2 = 0

        (vv_error, cc_error) = error
        synd_matrix = [[False for c2 in range(self.ccode.m)] for v1 in range(self.ccode.n)]

        for (v1, v2) in vv_error:
            for c2 in self.ccode.bit_nbhd[v2]:
                synd_matrix[v1][c2] = not synd_matrix[v1][c2]
        for (c1, c2) in cc_error:
            for v1 in self.ccode.check_nbhd[c1]:
                synd_matrix[v1][c2] = not synd_matrix[v1][c2]

        return synd_matrix


    def random_error(self, p):
        """
        Return a random iid error of probability 'p'
        """
        vv_xerror = [(v1,v2) for v1 in range(self.ccode.n) for v2 in range(self.ccode.n) if p > np.random.uniform(0,1)]
        cc_xerror = [(c1,c2) for c1 in range(self.ccode.m) for c2 in range(self.ccode.m) if p > np.random.uniform(0,1)]

        return (vv_xerror, cc_xerror)


    def error_to_list(self, error_array):
        """
        Create two lists of qbits given two 0,1 matrices which represent these qbits
        """
        v1 = 0
        v2 = 0
        c1 = 0
        c2 = 0

        (vv_error_array, cc_error_array) = error_array
        return (
            [(v1, v2) for v1 in range(self.ccode.n)
            for v2 in range(self.ccode.n) if vv_error_array[v1][v2]],
            [(c1, c2) for c1 in range(self.ccode.m) for c2 in range(self.ccode.m) if cc_error_array[c1][c2]])


    def decode(self, synd_matrix, mask=[]):
        """
        Run the decoder for a given syndrome
        """
        v1 = 0
        v2 = 0
        c1 = 0
        c2 = 0

        vv_guessed_error = [
            [False for v2 in range(self.ccode.n)] for v1 in range(self.ccode.n)]
        cc_guessed_error = [
            [False for c2 in range(self.ccode.m)] for c1 in range(self.ccode.m)]
        lookup_table = MaskedLookupTable(self.ccode, synd_matrix, mask)

        # print("synd weight before decoding:", lookup_table.synd_weight)

        gen = lookup_table.find_best_gen()
        while gen != None:
            (vv_qbits, cc_qbits) = lookup_table.update(gen)
            # print(vv_qbits, cc_qbits)
            for (v1, v2) in vv_qbits:
                vv_guessed_error[v1][v2] = not vv_guessed_error[v1][v2]
            for (c1, c2) in cc_qbits:
                cc_guessed_error[c1][c2] = not cc_guessed_error[c1][c2]
            # print("synd weight:", lookup_table.synd_weight)
            gen = lookup_table.find_best_gen()
        
        return (lookup_table.synd_weight, self.error_to_list((vv_guessed_error, cc_guessed_error)))

"""
# ccode = read_code('./ldpc_codes/16_12_3_4.txt')
ccode = read_code('./ldpc_codes/36_30_5_6.txt')
qcode = QuantumCode(ccode)


num_runs = 1000
mask_p = 0.3
ps = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
# ps = [0.01]

# ps = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]

for p in ps:
    sum = 0

    for i in range(num_runs):
        error = qcode.random_error(p)
        # error = ([(0,0)], [])
        synd = qcode.compute_synd_matrix(error)
        mask = [(v1,v2) for v1 in range(ccode.n) for v2 in range(ccode.m) if mask_p > np.random.uniform(0,1)]
        # mask = [(0, 10)]
        # mask = []
        # print(mask)
        # table = MaskedLookupTable(ccode, synd, mask)
        # table = LookupTable(ccode, synd)

        # gen = table.find_best_gen()
        # print(gen)
        # print(table.lookup_table[gen[0]][gen[1]])
        synd_weight, guessed_error = qcode.decode(synd, mask)
        # print(synd_weight)
        # print(mask)
        # print(synd_weight)
        # print(error)
        # print(guessed_error)
        # print()

        passed = True
        if (len(error[0]) == len(guessed_error[0]) and len(error[1]) == len(guessed_error[1])):
            for vv_error in error[0]:
                if (vv_error not in guessed_error[0]):
                    passed = False
            for cc_error in error[1]:
                if (cc_error not in guessed_error[1]):
                    passed = False
        else:
            passed = False
        
        if passed:
            sum += 1

        # if (not synd_weight):
            # sum += 1

    print(sum, (num_runs-sum)/num_runs)

# table = MaskedLookupTable(ccode, synd, [])
# synd_gen = [
#     [False, False, None],
#     [None, True, None],
#     [None, False, True],
#     [True, False, True]
# ]
# print(table.score_gen(synd_gen))
"""