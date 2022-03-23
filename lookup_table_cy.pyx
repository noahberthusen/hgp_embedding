import random

class LookupTable(object):
    """
    'synd_matrix' is a n*m matrix which represents the syndrome of the current error
    self.lookup_table contains the score of the generators
    """
    def __init__(self, ccode, synd_matrix):
        self.ccode = ccode
        self.synd_matrix = synd_matrix
        self.dv = ccode.dv
        self.dc = ccode.dc

        # The weight should not be necessary but we print it
        self.synd_weight = sum([sum(filter(None, l)) for l in self.synd_matrix])
        self.gray_code = self.compute_gray_code()

        cdef int c1 = 0
        cdef int v2 = 0

        self.round = 0
        self.last_update = [[self.round for v2 in range(
            self.ccode.n)] for c1 in range(self.ccode.m)]

        self.lookup_table = [[(0, 0, ([], [])) for v2 in range(
            self.ccode.n)] for c1 in range(self.ccode.m)] # an entry for every check in the form of c1 x v2
        for c1 in range(self.ccode.m):
            for v2 in range(self.ccode.n):
                self.update_score_generator((c1, v2))


    def hor_subset_score(self, int hor_synd_diff, int hor_weight, ver_synd_diff):
        """
        'hor' means horizontal
        'ver' means vertical
        Input:
        'hor_synd_diff' is |s| - |s xor synd(F)| for the current F which is a flip of the columns
        'hor_wweight' is the weighted weight of the horizontal flips = dc * hor_flips
        ver_synd_diff[i] is the difference of syndrome size when we flip the line 'i'
        Output:
        'ver_flips' the optimal set of lines to flip for this given flips of columns
        'synd_diff' the syndrome difference for this flips
        When hor_weight = 0, i.e F = 0 then len(ver_flips) > 0 even if the flipping ver_flips increases the syndrome weight <------ why
        wweight = weighted weight = dv * len(ver_flips) + dc * len (hor_flips)
        """
        cdef int s = 0
        cdef int i = 0
        cdef int weight = 0

        cdef int synd_diff = hor_synd_diff # old syndrome weight - new syndrome weight for just the columns
        # print(synd_diff, hor_synd_diff, ver_synd_diff)
        ver_flips = []
        sorted_ver_synd_diff = [(ver_synd_diff[i], i)  # sorted by index?. Positive difference means syndrome weight decreased
                                for i in range(len(ver_synd_diff))]
        sorted_ver_synd_diff.sort(reverse=True)  # best line flip is line with the largest weight difference

        weight = hor_weight # number of syndrome bits affected by the column flips
        for (s, i) in sorted_ver_synd_diff: # Want to check the rows bottom up?
            if s*weight >= synd_diff: # same as s / self.dv >= synd_diff / weight as in the papers
                synd_diff = synd_diff + s
                ver_flips.append(i) # add row to be flipped
                weight = weight + 1 # + self.dv
        
        return (synd_diff, ver_flips)


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
        cdef int i = 0
        cdef int j = 0

        # number of columns flipped * dc (which is number of rows). so number of syndrome bits affected by column flips
        cdef int hor_weight = 0 
        cdef int hor_synd_diff = 0

        cdef int best_weight = 0
        cdef int best_synd_diff = 0

        hor_flips_array = [False for j in range(self.dv)] 
        ver_synd_diff = [0 for i in range(self.dc)] # array containing what would happen to the syndrome weight if each row of the 
        # generator syndrome was flipped independently. Old syndrome weight minus new syndrome weight. 
        # Want positive difference (new syndrome weight less than old)
        

        for i in range(self.dc): # this initial ver_synd_diff is if no columns are flipped
            for j in range(self.dv): # difference in syndrome weights when you flip line i of synd_gen. Minus means syndrome weight increased
                # if a syndrome bit is 0 it will be flipped to 1, increasing the weight of the syndrome 
                # If a syndrome bit is 1 it will be flipped to 0, decreasing the weight of the syndrome
                
                # ver_synd_diff[i] = ver_synd_diff[i] + 2*synd_gen[i][j] - 1 
                if (synd_gen[i][j]):
                    ver_synd_diff[i] = ver_synd_diff[i] + 1
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
        cdef int c1 = 0
        cdef int v2 = 0
        cdef int i = 0
        cdef int j = 0

        (c1, v2) = gen
        ver = self.ccode.check_nbhd[c1] # list of qubits in c1
        hor = self.ccode.bit_nbhd[v2] # list of checks v2 is part of
        # dc x dv matrix that represents the support of an ~opposite~ type generator, creates a rectange in the syndrome
        synd_gen = [[self.synd_matrix[ver[i]][hor[j]]
            for j in range(self.ccode.dv)] for i in range(self.ccode.dc)] 
        self.lookup_table[c1][v2] = self.score_gen(synd_gen)


    def compute_synd(self, gen, flips):
        """
        Compute the syndrome when we flip the row and columns of 'flips' of the syndrome corresponding to the generator 'gen'
        """
        cdef int c1 = 0
        cdef int v2 = 0
        cdef int i = 0
        cdef int j = 0

        (c1, v2) = gen
        (ver_flips, hor_flips) = flips

        synd_matrix = [[False for j in range(self.dv)] for i in range(self.dc)]
        for i in ver_flips:
            for j in range(self.ccode.dv):
                synd_matrix[i][j] = not synd_matrix[i][j]
        for j in hor_flips:
            for i in range(self.ccode.dc):
                synd_matrix[i][j] = not synd_matrix[i][j]

        synd = []
        for i in range(self.ccode.dc):
            for j in range(self.ccode.dv):
                if synd_matrix[i][j]:
                    v1 = self.ccode.check_nbhd[c1][i]
                    c2 = self.ccode.bit_nbhd[v2][j]
                    synd.append((v1, c2))
        return synd
        
    def compute_qbits(self, gen, flips):
        """
        compute the qbits which correspond to the rows and columns of 'flips' for the generator 'gen'
        """
        cdef int c1 = 0
        cdef int v2 = 0
        cdef int i = 0
        cdef int j = 0

        (c1, v2) = gen
        (ver_flips, hor_flips) = flips

        vv_qbits = []
        for i in ver_flips:
            vv_qbits.append((self.ccode.check_nbhd[c1][i], v2))
        cc_qbits = []
        for j in hor_flips:
            cc_qbits.append((c1, self.ccode.bit_nbhd[v2][j]))

        return (vv_qbits, cc_qbits)

    def find_best_gen(self):
        """
        returns the best generator to flip for the current syndrome
        """
        best_gen = None
        cdef int synd_diff = 0
        cdef int best_synd_diff = 0
        cdef int weight = 0
        cdef int best_weight = 1
        cdef int c1 = 0
        cdef int v2 = 0

        for c1 in range(self.ccode.m):
            for v2 in range(self.ccode.n):
                (synd_diff, weight, _) = self.lookup_table[c1][v2] # go through all the generators pick max | sigma - sigma + F| / |F|
                if (best_synd_diff * weight < synd_diff * best_weight): # if synd_diff / weight < best_synd_diff / best_weight
                    best_gen = (c1, v2)
                    best_synd_diff = synd_diff
                    best_weight = weight

        return best_gen


    def update(self, gen):
        """
        update the lookup table under the assumption that we flip the best subset of the generator 'gen'
        """
        cdef int c1 = 0
        cdef int c2 = 0
        cdef int v1 = 0
        cdef int v2 = 0

        self.round = self.round + 1
        (c1, v2) = gen
        (synd_diff, _, flips) = self.lookup_table[c1][v2]
        synd = self.compute_synd(gen, flips)

        self.synd_weight = self.synd_weight - synd_diff

        for (v1, c2) in synd:
            self.synd_matrix[v1][c2] = not self.synd_matrix[v1][c2]

        for (v1, c2) in synd:
            for v2 in self.ccode.check_nbhd[c2]:
                for c1 in self.ccode.bit_nbhd[v1]:
                    if self.last_update[c1][v2] != self.round:
                        self.update_score_generator((c1, v2))
                        self.last_update[c1][v2] = self.round

        return self.compute_qbits(gen, flips)


    def compute_gray_code(self):
        """
        returns the gray code
        If you begin with [0 for i in range(dv)] and flip the bits res[0], res[1], ..., res[dv-2] then you go through {0,1}^dv
        """
        res = []
        for i in range(self.dv):
            res = res + [i] + res
        return res


# -----------------------------------------------------------------------------------------------------


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
        cdef int i = 0
        cdef int j = 0
        
        # number of columns flipped * dc (which is number of rows). so number of syndrome bits affected by column flips
        cdef int hor_weight = 0
        cdef int hor_synd_diff = 0

        cdef int best_weight = 0
        cdef int best_synd_diff = 0

        hor_flips_array = [False for j in range(self.dv)] 
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
        cdef int c1 = 0
        cdef int v2 = 0
        cdef int i = 0
        cdef int j = 0

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
        cdef int c1 = 0
        cdef int c2 = 0
        cdef int v1 = 0
        cdef int v2 = 0

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


# ------------------------------------------------------------------------------------------------------


def compute_synd_matrix(ccode, error):
    """
    Returns the syndrome of the list of errors
    """
    cdef int v1 = 0
    cdef int v2 = 0
    cdef int c1 = 0
    cdef int c2 = 0

    (vv_error, cc_error) = error
    synd_matrix = [[False for c2 in range(ccode.m)] for v1 in range(ccode.n)]

    for (v1, v2) in vv_error:
        for c2 in ccode.bit_nbhd[v2]:
            synd_matrix[v1][c2] = not synd_matrix[v1][c2]
    for (c1, c2) in cc_error:
        for v1 in ccode.check_nbhd[c1]:
            synd_matrix[v1][c2] = not synd_matrix[v1][c2]

    return synd_matrix


def random_error(ccode, p):
    """
    Return a random iid error of probability 'p'
    """
    vv_xerror = [(v1,v2) for v1 in range(ccode.n) for v2 in range(ccode.n) if p > random.uniform(0,1)]
    cc_xerror = [(c1,c2) for c1 in range(ccode.m) for c2 in range(ccode.m) if p > random.uniform(0,1)]

    return (vv_xerror, cc_xerror)


def error_to_list(ccode, error_array):
    """
    Create two lists of qbits given two 0,1 matrices which represent these qbits
    """
    cdef int v1 = 0
    cdef int v2 = 0
    cdef int c1 = 0
    cdef int c2 = 0

    (vv_error_array, cc_error_array) = error_array
    return (
        [(v1, v2) for v1 in range(ccode.n)
        for v2 in range(ccode.n) if vv_error_array[v1][v2]],
        [(c1, c2) for c1 in range(ccode.m) for c2 in range(ccode.m) if cc_error_array[c1][c2]])


def decode(ccode, synd_matrix, mask=[]):
    """
    Run the decoder for a given syndrome
    """
    cdef int v1 = 0
    cdef int v2 = 0
    cdef int c1 = 0
    cdef int c2 = 0

    vv_guessed_error = [
        [False for v2 in range(ccode.n)] for v1 in range(ccode.n)]
    cc_guessed_error = [
        [False for c2 in range(ccode.m)] for c1 in range(ccode.m)]
    lookup_table = MaskedLookupTable(ccode, synd_matrix, mask)

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
    
    return (lookup_table.synd_weight, error_to_list(ccode, (vv_guessed_error, cc_guessed_error)))
