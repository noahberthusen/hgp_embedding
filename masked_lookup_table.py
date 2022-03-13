from lookup_table import LookupTable
import numpy as np

class MaskedLookupTable(LookupTable):
    def __init__(self, ccode, synd_matrix, mask):
        self.mask = mask # list of syndrome bits that should not be used

        self.masked_synd_matrix = synd_matrix.copy()
        for (v1, c2) in self.mask:
            self.masked_synd_matrix[v1][c2] = None

        LookupTable.__init__(self, ccode, synd_matrix)

        # print(np.array(self.masked_synd_matrix))

    def score_gen(self, synd_gen):
        """
        Input:
        'synd_gen' is a 0,1 matrix which reprensents the syndrome of the current generator
        'gray_code' is the output of 'compute_gray_code'
        Output:
        'best_flips' = (ver_flips,hor_flips) are two lists of lines and columns which are optimal for the generator
        'best_synd_diff' is the syndrome difference for these flips
        'best_wweight' = dv * len(ver_flips) + dc * len(hor_flips)
        We go through all the possible flips of columns and use the function 'hor_subset_score'
        At the end, best_weight > 0 even it is better to flip nothing
        """
        i = 0
        j = 0

        hor_weight = 0
        hor_synd_diff = 0

        best_weight = 0
        best_synd_diff = 0

        hor_weight = 0 # number of columns flipped * dc (which is number of rows). so number of syndrome bits affected by column flips
        hor_flips_array = [False for j in range(self.dv)] 
        hor_synd_diff = 0 
        ver_synd_diff = [0 for i in range(self.dc)] # array containing what would happen to the syndrome weight if each row of the 
        # generator syndrome was flipped independently. Old syndrome weight minus new syndrome weight. 
        # Want positive difference (new syndrome weight less than old)
        

        for i in range(self.dc): # this initial ver_synd_diff is if no columns are flipped
            for j in range(self.dv): # difference in syndrome weights when you flip line i of synd_gen. Minus means syndrome weight increased
                # if a syndrome bit is 0 it will be flipped to 1, increasing the weight of the syndrome 
                # If a syndrome bit is 1 it will be flipped to 0, decreasing the weight of the syndrome
                
                # ver_synd_diff[i] = ver_synd_diff[i] + 2*synd_gen[i][j] - 1 
                if (synd_gen[i][j] != None):
                    if (synd_gen[i][j]):
                        ver_synd_diff[i] += 1
                    else:
                        ver_synd_diff[i] -= 1

        (best_synd_diff, ver_flips) = self.hor_subset_score(hor_synd_diff, hor_weight, ver_synd_diff)

        best_weight = len(ver_flips) # * self.dv
        best_flips = (ver_flips, [])

        for j in self.gray_code: # go though all possible flips of the columns of synd_gen
            if hor_flips_array[j]: # the way the gray code works is it toggles specific columns. If on -> off.
                hor_weight = hor_weight - 1 # - self.dc
                hor_flips_array[j] = False
                for i in range(self.dc): # go through each of the rows. 
                    # ver_synd_diff[i] = ver_synd_diff[i] + 4*synd_gen[i][j] - 2
                    # hor_synd_diff = hor_synd_diff - 2*synd_gen[i][j] + 1
                    if (synd_gen[i][j] != None):
                        if (synd_gen[i][j]):
                            ver_synd_diff[i] += 2
                            hor_synd_diff -= 1
                        else:
                            ver_synd_diff[i] -= 2
                            hor_synd_diff += 1
            else:
                hor_weight = hor_weight + 1 # + self.dc
                hor_flips_array[j] = True
                for i in range(self.dc):
                    # Only check column j. The other columns stay the same. 
                    # If a syndrome bit is 1, it will get flipped due to the column flip so 
                    #       flipping it with the row will increase the weight (relative to the previous syndrome flip) by two.

                    # ver_synd_diff[i] = ver_synd_diff[i] - 4*synd_gen[i][j] + 2 
                    # hor_synd_diff = hor_synd_diff + 2*synd_gen[i][j] - 1
                    if (synd_gen[i][j] != None):
                        if (synd_gen[i][j]):
                            ver_synd_diff[i] -= 2
                            hor_synd_diff += 1
                        else:
                            ver_synd_diff[i] += 2
                            hor_synd_diff -= 1

            (synd_diff, ver_flips) = self.hor_subset_score(hor_synd_diff, hor_weight, ver_synd_diff)

            weight = hor_weight + len(ver_flips) # * self.dv # this is total number of syndrome bits affected by the flips

            if synd_diff * best_weight > best_synd_diff * weight: # synd_diff / weight > best_synd_diff / best_weight
                best_synd_diff = synd_diff
                best_weight = weight
                best_flips = (ver_flips, [j for j in range(self.dv) if hor_flips_array[j]])

        return (best_synd_diff, best_weight, best_flips)

    def update_score_generator(self, gen):
        """
        Computes the best column and row flips for a given generator gen
        """
        c1 = 0
        v2 = 0
        i = 0
        j = 0
        (c1, v2) = gen
        ver = self.ccode.check_nbhd[c1] # list of qubits in c1
        hor = self.ccode.bit_nbhd[v2] # list of checks v2 is part of
        # dc x dv matrix that represents the support of an ~opposite~ type generator, creates a rectange in the syndrome
        synd_gen = [[self.masked_synd_matrix[ver[i]][hor[j]]
            for j in range(self.ccode.dv)] for i in range(self.ccode.dc)] 

        self.lookup_table[c1][v2] = self.score_gen(synd_gen)

    def update(self, gen):
        """
        update the lookup table under the assumption that we flip the best subset of the generator 'gen'
        """
        c1 = 0
        c2 = 0
        v1 = 0
        v2 = 0

        self.round = self.round + 1
        (c1, v2) = gen
        (synd_diff, _, flips) = self.lookup_table[c1][v2]
        synd = self.compute_synd(gen, flips)

        self.synd_weight = self.synd_weight - synd_diff

        for (v1, c2) in synd:
            if (self.masked_synd_matrix[v1][c2] != None):
                self.masked_synd_matrix[v1][c2] = not self.masked_synd_matrix[v1][c2]

        for (v1, c2) in synd:
            for v2 in self.ccode.check_nbhd[c2]:
                for c1 in self.ccode.bit_nbhd[v1]:
                    if self.last_update[c1][v2] != self.round:
                        self.update_score_generator((c1, v2))
                        self.last_update[c1][v2] = self.round

        return self.compute_qbits(gen, flips)
