from turtle import numinput
from classical_code import read_code
import numpy as np
import os

codes = [
    # "swap3_24_20_5_6",
    # "30_25_5_6",
    "swap3_36_30_5_6",
    "swap3_42_35_5_6",
    # "48_40_5_6",
    # "60_50_5_6",
    # "72_60_5_6",
    # "swap3_84_70_5_6"
]
distances = []

def gf2_rank(rows):
    """
    Find rank of a matrix over GF2.

    The rows of the matrix are given as nonnegative integers, thought
    of as bit-strings.

    This function modifies the input list. Use gf2_rank(rows.copy())
    instead of gf2_rank(rows) to avoid modifying rows.
    """
    rank = 0
    while len(rows):
        pivot_row = rows[-1]
        rows = np.delete(rows, -1, 0)
        if np.count_nonzero(pivot_row):
            rank += 1
            lsb = pivot_row & -pivot_row
            for index, row in enumerate(rows):
                if np.count_nonzero(row & lsb):
                    rows[index] = row ^ pivot_row
    return rank
def rref(H):
    r = 0
    n = len(H[0])
    num_checks = len(H)
    k = n - num_checks
    for c in range(0, num_checks):
        if (H[r, c] == 0):
            # need to swap
            for r2 in range(r+1, num_checks):
                if (H[r2, c] == 1):
                    temp = H[r, :].copy()
                    H[r, :] = H[r2, :]
                    H[r2, :] = temp
                    break
                    
        # if (H[r, c] == 0):
        #     print('H is singular')

        # cancel out other rows
        for r2 in range(r+1, num_checks):
            if (H[r2, c] == 1):
                H[r2, :] = H[r2, :] ^ H[r, :]

        # # back substitution
        for r2 in range(0, r):
            if (H[r2, c] == 1):
                H[r2, :] = H[r2, :] ^ H[r, :]

        r += 1
    return H

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

num_iters = 1000
for i, code in enumerate(codes):
    file = os.path.join(path, f'./prebuilt_code/ssf_masked/ccode/{code}.code')
    ccode = read_code(file)
    d = ccode.n
    n = ccode.n
    k = ccode.n - ccode.m

    H = np.zeros((ccode.m, ccode.n), dtype=int)
    for j, row in enumerate(ccode.check_nbhd):
        for r in row:
            H[j][r] = 1

    print(f"Rank: {gf2_rank(H)}")
    rref_H = rref(H.copy())
    G = np.hstack([np.eye(k, dtype=int), rref_H[:,n-k:n].T])

    for j in range(1, 2**k):
        num = bin(j)[2:].zfill(k)
        w = np.array([int(b) for b in num])
        encoded_w = w@G % 2

        # if (np.any(H@encoded_w)):
        #     print('Not a codeword')
        if (np.count_nonzero(encoded_w) < d):
            d = np.count_nonzero(encoded_w)

    distances.append(d)
    print(f"{code} distance: {d}")

print(distances)