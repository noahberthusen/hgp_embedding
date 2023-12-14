from asyncore import write
import default_names
from print_erase import*
import decoder
from read_ccodes import read_ccode
from read_result import Result, save_new_res
import time
import argparse
import glob
from flip import run_flip_ccode
import networkx as nx

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
file_name_list = ["../ccode/24_20_5_6.code"]
# file_name_list = ["../ccode/swap3_120_100_5_6.code"]
# file_name_list = ["../ccode/20_15_3_4.code"]
# file_name_list = ["../ccode/7_3_1_4.code"]
# file_name_list = ["../ccode/16_12_3_4.code"]
cluster_size_file = default_names.cluster_size_file_name
error_size_file = default_names.error_size_file_name

###########################################################
# Simulation parameters
###########################################################
# Change this value for another algorithm (for example for the parallel version)
algo = 1
# P = [0.0025 * k for k in range(15,16)]
# P = [0.05,0.06,0.07]
# P = [6,7]
# P = [0.005]
maskP = [0.4]
time_vector = [100]
no_runs = 1000
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
    else:
        raise NameError('This algo number does not exist')

def get_graph(ccode):
    # returns syndrome adjacency graph for just x gens
    G = nx.Graph()

    vv_qubits = [(v1,v2,0) for v1 in range(ccode.n) for v2 in range(ccode.n)]
    cc_qubits = [(c1,c2,1) for c1 in range(ccode.m) for c2 in range(ccode.m)]
    G.add_nodes_from(vv_qubits + cc_qubits)

    # only x gen
    for qb in vv_qubits:
        for check in ccode.bit_nbhd[qb[1]]:
            for bit in ccode.check_nbhd[check]:
                G.add_edge(qb, (qb[0],bit,0))
            for bit in ccode.bit_nbhd[qb[0]]:
                G.add_edge(qb, (bit,check,1))

    for qb in cc_qubits:
        for bit in ccode.check_nbhd[qb[0]]:
            for check in ccode.bit_nbhd[bit]:
                G.add_edge(qb, (check,qb[1],1))
            for check in ccode.check_nbhd[qb[1]]:
                G.add_edge(qb, (bit,check,0))

    G.remove_edges_from(nx.selfloop_edges(G))
    return G

def get_largest_cluster(G, error):
    vv_errors = [(vv[0],vv[1],0) for vv in error[0]]
    cc_errors = [(cc[0],cc[1],1) for cc in error[1]]
    H = G.subgraph(vv_errors + cc_errors)
    comps = list(nx.connected_components(H))

    if (comps):
        return len(max(comps, key=len))
    else:
        return 0

def write_to_files(ccode, error, mask, G, error_f, cluster_f):
    error_size = len(error[0]) + len(error[1])
    cluster_size = get_largest_cluster(G, error)
    synd_weight = decoder.compute_syndrome_weight(ccode, error, mask)
    if (synd_weight):
        error_f.write(f"{error_size}*")
        cluster_f.write(f"{cluster_size}*")
    else:
        error_f.write(f"{error_size}")
        cluster_f.write(f"{cluster_size}")

p = 0.001
def main_laptop():
    start = time.time()
    code_list = read_ccode(file_name_list, n_list, m_list, dv_list, dc_list, id_list)
    cluster_f = open(cluster_size_file, "w")
    error_f = open(error_size_file, "w")

    # code_list = code_list[:no_codes]
    if len(code_list) == 0:
        raise NameError('No such code')
    
    for i in range(len(code_list)):
        ccode = code_list[i]
        G = get_graph(ccode)

        if is_quantum(algo):
            logical2 = decoder.Logical2(ccode)
        else:
            logical2 = None
        
        s = "dv = " + str(ccode.dv) + " ,dc = " + str(ccode.dc) + " ,n = " + str(ccode.n) + " ,m = " + str(ccode.m)
        print("Code " + str(i+1) + s)

        for r in range(no_runs):
            for p_mask in maskP:
                mask = decoder.random_mask(ccode, p_mask)
                rs = []
                # partial synd mask

                for t_i in time_vector:
                    no_success = 0
                    no_stop = 0
                    error = decoder.random_error(ccode, 0)

                    for t in range(t_i+1):
                        error_f.write("(")
                        cluster_f.write("(")
                        tmp_error = decoder.random_error(ccode, p)
                        write_to_files(ccode, tmp_error, mask, G, error_f, cluster_f)

                        error = (list(set(error[0]) ^ set(tmp_error[0])), list(set(error[1]) ^ set(tmp_error[1])))

                        # after adding random error, before decoding
                        # write_to_files(ccode, error, mask, G, error_f, cluster_f)
                        error_f.write(",")
                        cluster_f.write(",")
                        # after decoding
                        res, guessed_error = run_algo(algo, ccode, error, mask, logical2, 1)
                        error = (list(set(error[0]) ^ set(guessed_error[0])), list(set(error[1]) ^ set(guessed_error[1])))
                        write_to_files(ccode, error, mask, G, error_f, cluster_f)
                        error_f.write(");")
                        cluster_f.write(");")

                    error_f.write("(")
                    cluster_f.write("(")
                    tmp_error = decoder.random_error(ccode, p)
                    write_to_files(ccode, tmp_error, mask, G, error_f, cluster_f)

                    error = (list(set(error[0]) ^ set(tmp_error[0])), list(set(error[1]) ^ set(tmp_error[1])))
                    # write_to_files(ccode, error, mask, G, error_f, cluster_f)
                    error_f.write(",")
                    cluster_f.write(",")
                    res, guessed_error = run_algo(algo, ccode, error, decoder.random_mask(ccode, 0), logical2, 1)
                    error = (list(set(error[0]) ^ set(guessed_error[0])), list(set(error[1]) ^ set(guessed_error[1])))
                    write_to_files(ccode, error, mask, G, error_f, cluster_f)

                    if res == 2:
                        error_f.write("*+)\n")
                        cluster_f.write("*+)\n")

                        r = Result(t,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,p_mask,1,0,1)
                    else:
                        if (res):
                            error_f.write(")\n")
                            cluster_f.write(")\n")
                        else:
                            error_f.write("+)\n")
                            cluster_f.write("+)\n")

                        r = Result(t,ccode.dv,ccode.dc,ccode.n,ccode.m,ccode.id,p,p_mask,1,res,0)
                    no_stop = no_stop + r.no_stop
                    no_success = no_success + r.no_success
                    rs.append(r)

                save_new_res(args.o, rs)
            
    stop = time.time()
    error_f.close()
    cluster_f.close()
    print("Time taken: " + str(stop - start) + "\n")

print("output file = " + args.o)
main_laptop()