import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
import scipy as sp
import random

def smallest_circle(P, R):
    
    def circle_from_two_points(R):
        mid = ((R[0][0] + R[1][0]) / 2, (R[0][1] + R[1][1]) / 2)
        dist = math.sqrt((R[0][0] - R[1][0])**2 + (R[0][1] - R[1][1])**2)
        return (mid[0], mid[1], dist/2)
    
    def circle_from_three_points(R):
        # https://stackoverflow.com/questions/62483582/solving-matrix-equations-circle-from-3-points
        A = np.array([[2*R[0][0], 2*R[0][1], 1],
                        [2*R[1][0], 2*R[1][1], 1],
                        [2*R[2][0], 2*R[2][1], 1]])
        b = np.array([-(R[0][0]**2 + R[0][1]**2), 
                    -(R[1][0]**2 + R[1][1]**2), 
                    -(R[2][0]**2 + R[2][1]**2)])
        x = sp.linalg.solve(A, b)
        return (-x[0], -x[1], math.sqrt(x[0]**2 + x[1]**2 - x[2]))

    def in_circle(D, R):
        for p in R:
            if (round(math.sqrt((p[0] - D[0])**2 + (p[1] - D[1])**2), 5) <= round(D[2], 5)):
                continue
            else:
                return False
        return True

    def compute_minimum_circle(R):
        if (len(R) == 0):
            return ((0, 0, -1), R)
        elif (len(R) == 1):
            return ((R[0][0], R[0][1], 0), R)
        elif (len(R) == 2):
            return (circle_from_two_points(R), R)
        elif (len(R) == 3):
            new_R = [[R[0], R[2]], [R[1], R[2]], [R[0], R[1], R[2]]]
            circs = []

            for r in new_R:
                if (len(r) == 2):
                    circs.append(circle_from_two_points(r))
                elif (len(r) == 3):
                    if ((r[2][1] - r[1][1])*(r[1][0] - r[0][0]) == (r[1][1] - r[0][1])*(r[2][0] - r[1][0])):
                        # for collinear points, circle will be one of [R[0], R[2]] or [R[1], R[2]]
                        circs.append((0, 0, -1))
                    else:
                        circs.append(circle_from_three_points(r))

            areas = [np.pi*c[2]**2 for c in circs]
            contains_all = [not in_circle(c, R) for c in circs]
            areas = np.ma.MaskedArray(areas, mask=contains_all)
            ind_min = np.argmin(areas)

            return (circs[ind_min], new_R[ind_min])
        elif (len(R) == 4):
            new_R = [[R[0], R[3]], [R[1], R[3]], [R[2], R[3]], [R[0], R[1], R[3]], [R[0], R[2], R[3]], [R[1], R[2], R[3]]]
            circs = []

            for r in new_R:
                if (len(r) == 2):
                    circs.append(circle_from_two_points(r))
                elif (len(r) == 3):
                    if ((r[2][1] - r[1][1])*(r[1][0] - r[0][0]) == (r[1][1] - r[0][1])*(r[2][0] - r[1][0])):
                        circs.append((0, 0, -1))
                    else:
                        circs.append(circle_from_three_points(r))

            areas = [np.pi*c[2]**2 for c in circs]
            contains_all = [not in_circle(c, R) for c in circs]
            areas = np.ma.MaskedArray(areas, mask=contains_all)
            ind_min = np.argmin(areas)

            return (circs[ind_min], new_R[ind_min])

    C = compute_minimum_circle([P[0], P[1]])
    for i in range(2, len(P)):
        if (in_circle(C, [P[i]])):
            continue
        else:
            C = smallest_circle(P[:i], P[i])
    return C

    # while (len(P) != 0):
    #     # ind = np.random.choice(len(P), 1)[0]
    #     ind = len(P)-1
    #     p = P.pop(ind) 

    #     # D, R = compute_minimum_circle(R)

    #     if (in_circle(D, [p])):
    #         continue

    #     else:
    #         R.append(p)

    #         D_old = D
    #         D, R = compute_minimum_circle(R)

    #         if (D_old[2] != D[2]):
    #             print("restart")
    #             P = p_copy
    
    # return D

def mec(points):
    random.shuffle(points)
    return smallest_circle(points, [])


points = [(1, 3), (2, 7), (3, 2), (6, 6)][::-1]
# points = [(6, 1), (8, 3), (7, 6), (2, 8)]
# points = [(1,0), (3,0)]
for i in range(1):
    circ = smallest_circle(points.copy(), [])
    print(circ)

