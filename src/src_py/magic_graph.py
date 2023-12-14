import numpy as np

def bit_nbhd_to_check_nbhd(n,m,bit_nbhd):
    """
    Return check_nbhd given n,m,bit_nbhd (see the description of the class Classical_code)
    """
    check_nbhd = [[] for j in range(m)]
    for i in range(n):
        for j in bit_nbhd[i]:
            check_nbhd[j].append(i)
    return check_nbhd

############ Magic graph model ############

def magic_graph(n,m,dv):
	"""
	Generates a left-regular graph with degree dv
	"""
	bit_nbhd = [[] for v in range(n)]

	for v in range(n):
		while len(bit_nbhd[v]) < dv:
			nbr = np.random.randint(m)
			bit_nbhd[v] = list(set(bit_nbhd[v] + [nbr]))

	check_nbhd = bit_nbhd_to_check_nbhd(n,m,bit_nbhd)

	return bit_nbhd,check_nbhd