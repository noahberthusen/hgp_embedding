from read_code import read_code
from result import Result, save_new_res
from pymatching import Matching
import numpy as np
from code_utils import par2gen, SGSOP
import uuid

file_name = "../codes/5_4_360.txt"

p_mask = 0
# Ts = np.linspace(0,100,11,dtype=np.uint8)
# Ts = [100, 200, 300, 400, 500]
# Ts = np.linspace(1, 1000, 30, dtype=np.uint8)
# Ts = np.arange(100, 201)
Ts = np.arange(110, 151, 10)
p0 = 0.003
no_test = 100000000000


def decode_iterative(masked_matching, unmasked_matching, H, logicals, p, p_mask, T):
    noise = np.zeros(H.shape[1], dtype=np.uint8)
    mask = np.where(np.random.random(H.shape[0]) < p_mask)[0]

    for t in range(1, T+1):
        noise = noise ^ (np.random.random(H.shape[1]) < p).astype(np.uint8)
        shots = (noise @ H.T) % 2

#        if (t % 2) == 1:
        masked_matching.set_boundary_nodes(set(mask))
        shots[mask] = 0
#        else:
#            masked_matching.set_boundary_nodes(set())

        predicted_error = masked_matching.decode(shots)
        noise = noise ^ predicted_error

    noise = noise ^ (np.random.random(H.shape[1]) < p).astype(np.uint8)
    shots = (noise @ H.T) % 2
    actual_observables = (noise @ logicals.T) % 2
    predicted_observables = unmasked_matching.decode(shots)

    return np.any(predicted_observables != actual_observables)


if __name__ == "__main__":
    params, H = read_code(file_name)

    n = H.shape[1]
    m = H.shape[0]
    m1 = params['m1']
    m2 = params['m2']
    r = params['r']
    s = params['s']
    Hx = H[:m1]
    Hz = H[m1:]

    Gx, col_Gx = par2gen(Hx)
    Gz, col_Gz = par2gen(Hz)
    logicals, generators = SGSOP(Gx, Gz, n)

    logX = np.array([l[1][n:] for l in logicals])
    logZ = np.array([l[0][:n] for l in logicals])

    unmasked_matching_X = Matching.from_check_matrix(Hx, faults_matrix=logX)
    masked_matching_X = Matching.from_check_matrix(Hx)
    unmasked_matching_Z = Matching.from_check_matrix(Hz, faults_matrix=logZ)
    masked_matching_Z = Matching.from_check_matrix(Hz)

    res_file_name = "../results/hyperbolic.res"

    rs = []
    for i in range(no_test):
        for t in Ts:
            res_X = decode_iterative(masked_matching_X, unmasked_matching_X, Hx, logX, p0, p_mask, t)
            res_Z = decode_iterative(masked_matching_Z, unmasked_matching_Z, Hz, logZ, p0, p_mask, t)

            res1 = Result(t, r, s, n, p0, p_mask, 1, int(not res_X))
            res2 = Result(t, r, s, n, p0, p_mask, 1, int(not res_Z))

            rs.append(res1)
            rs.append(res2)

        if (i % 1000 == 0):
            save_new_res(res_file_name, rs)
            rs = []
