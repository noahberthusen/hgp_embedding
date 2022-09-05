import numpy as np
# import galois
import math
import matplotlib.pyplot as plt
from scipy import sparse
# GF = galois.GF(2)


def gen_code(n, deg_v, deg_c):
    # n = 80
    # deg_v = 3 # w_c. Every bit is in this many checks
    # deg_c = 4 # w_r. Every check has this many bits in it
    num_checks = (n*deg_v)//deg_c
    k = n - num_checks

    vs = np.array([[j for i in range(deg_v)] for j in range(n)]).flatten()
    cs = np.array([[j for i in range(deg_c)] for j in range(num_checks)]).flatten()

    H = np.zeros((num_checks, n), dtype=bool)

    while (vs.size and cs.size):
        # choose random 'stub' from each array
        double_edge = True
        while(double_edge):
            v_ind = np.random.randint(0, len(vs))
            c_ind = np.random.randint(0, len(cs))

            if (H[cs[c_ind]][vs[v_ind]] != 1):
                double_edge = False
                H[cs[c_ind]][vs[v_ind]] = 1
                vs = np.delete(vs, v_ind)
                cs =np.delete(cs, c_ind)

    H = sparse.csc_matrix(H)

    return H

    # hx1 = sparse.kron(H, np.eye(H.shape[1], dtype=bool))
    # hx2 = sparse.kron(np.eye(H.shape[0], dtype=bool), H.T)
    # Hx = sparse.csr_matrix(sparse.hstack([hx1, hx2], ))

    # hz1 = sparse.kron(np.eye(H.shape[1], dtype=bool), H)
    # hz2 = sparse.kron(H.T, np.eye(H.shape[0], dtype=bool))
    # Hz = sparse.csr_matrix(sparse.hstack([hz1, hz2]))

def overlap_prob(H, deg_c):
    """
    Returns the probability of a generator overlapping other generators at most one location
    """

    H = H.tocsr()
    overlap_count = [[0 for _ in range(deg_c)] for _ in range(H.shape[0])]
    rows = H.shape[0]
    for j in range(rows):
        for i in range(rows):
            if (j != i):
                num_overlap = len(set(H[j].indices) & set(H[i].indices))
                overlap_count[j][num_overlap] += 1
    
    overlap_count = np.array(overlap_count)

    count = 0
    for c in overlap_count:
        if (np.count_nonzero(c) == 2):
            count += 1

    return count / H.shape[0]

def hgd(N,K,n,k):
    return (math.comb(K,k) * math.comb(N-K,n-k)) / math.comb(N,n)

def calculated_prob(num_checks, deg_c, deg_v):
    prod = 1
    for i in range(1, deg_c):
        prod *= hgd(num_checks-1, deg_v*i-i, deg_v-1, 0)
    return prod

if (__name__ == "__main__"):
    ns = np.arange(40, 500, 40)
    deg_v = 3
    deg_c = 4

    ms = []
    experimental_probs = []
    calculated_probs = []
    for n in ns:
        code = gen_code(n, deg_v, deg_c)
        num_checks = code.shape[0]
        ms.append(num_checks)

        prob = overlap_prob(code, deg_c)
        experimental_probs.append(prob)
        calculated_probs.append(calculated_prob(num_checks, deg_c, deg_v))
        print(n)

    plt.scatter(ms, experimental_probs, label='data')
    plt.plot(ms, calculated_probs, label='test')
    plt.legend(loc='upper right')
    # plt.yscale('log')
    plt.show()
