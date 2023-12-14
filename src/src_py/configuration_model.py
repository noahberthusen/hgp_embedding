import numpy as np
from print_erase import *
import math
import uuid
from decoder import Classical_code


def bit_nbhd_to_check_nbhd(n,m,bit_nbhd):
    """
    Return check_nbhd given n,m,bit_nbhd (see the description of the class Classical_code)
    """
    check_nbhd = [[] for j in range(m)]
    for i in range(n):
        for j in bit_nbhd[i]:
            check_nbhd[j].append(i)
    return check_nbhd

############ Tests ############
# code = bit_nbhd_to_ccode(4,2,[[0],[0],[0,1],[1]])
# print(code.check_nbhd)
###############################


############ Configuration model ############



def configuration_model(n, m, dv, dc, patience = 1):
    """
    Input: n, m, dv, dc, patience
    Output: object of the class Classical_code

    Description:
    ------------
    Generates bipartite (multi-)graph using configuration model.
    Loops configuration model until valid regular graph is created or until we run out of patience
    Graph has n variable nodes of deg. dv and m check nodes of deg. dc.
    """

    maximum = 0
    index_set = [i for i in range(n*dv)]
    bit_nbhd = [[0 for j in range(dv)] for i in range(n)]

    print_erase = Print_erase()
    
    for count in range(patience):
        
        perm = np.random.permutation(index_set)

        i = 0
        while i < n:
            for j in range(dv):
                nbr = math.floor(perm[i*dv + j]/dc)
                bit_nbhd[i][j] = nbr
            if len(set(bit_nbhd[i])) == dv:
                i = i + 1
            else:
                if maximum < i:
                    maximum = i

                s = "configuration model, attempt " + str(count) + "     "
                s = s + str(maximum) + "/" + str(len(bit_nbhd)) + "     "
                s = s + str(i) + "/" + str(len(bit_nbhd)) + "     "
                print_erase.print(s)
                
                i = n + 1
                
        if i == n:
            check_nbhd = bit_nbhd_to_check_nbhd(n,m,bit_nbhd)
            return Classical_code(n, m, bit_nbhd, check_nbhd, dv, dc, str(uuid.uuid4())[:8])


############ Tests ############
# n = 20; m = 10; dv = 2; dc = 4; patience = 10
# code = configuration_model(n, m, dv, dc, patience)
# print(is_regular(code,dv))
# print(code.bit_nbhd)
# print(code.check_nbhd)
###############################


############ Swap edges ############
# The goal is to construct regular bipartite graphs with large girth using swap of edges.
# We first generate a random graph using the configuration model and then remove small cycles.
# In order to remove a cycle we swap a random edge of this cycle with a random edge in the graph
# swap((u1,u2),(u3,u4)) --> (u1,u4),(u2,u3) 
from random import randint
from queue import Queue


# Can return graph with multiple edges
def compute_rand_bit_nbhd(n, m, dv, dc):
    """
    Similar to the function configuration_model but without the parameter patience

    Input: n, m, dv, dc
    Output: bit_nbhd (as defined in the class Classical_codes but multiple edges are allowed)

    Description:
    ------------
    Generates bipartite (multi-)graph using configuration model.
    Graph has n variable nodes of deg. dv and m check nodes of deg. dc.
    Multiple edges are allowed
    """
    bit_nbhd = [[0 for j in range(dv)] for i in range(n)]
    perm = np.random.permutation([i for i in range(n*dv)])
    for i in range(n):
        for j in range(dv):
            nbr = math.floor(perm[i*dv + j]/dc)
            bit_nbhd[i][j] = nbr
    return bit_nbhd

    

def replace(l,a,b):
    """
    Input:
      'l' a liste
      'a' an element in l
      'b'
    Output:
      The list l where the first occurence of 'a' has been replace by 'b'.
      We raise an error if 'a' \notin l
    """
    for i in range(len(l)):
        if l[i] == a:
            l[i] = b
            return None
    raise NameError('Not replaced')

        
class Bip_graph:
    """
    This class represents a bipartite graph as a non-bipartite graph with an adjacency matrix.
    The goal is to remove short cycle and then return a object of the class Classical_code
    Be carefull, the method find_shortest_cycle_for_vertex would not work if the graph was not bipartite.
    See "almost minimum circuit":
    http://perso.ens-lyon.fr/eric.thierry/Graphes2007/adrien-panhaleux.pdf (in french)
    or the original article "FINDING A MINIMUM CIRCUIT IN A GRAPH*":
    http://www.cs.technion.ac.il/~itai/publications/Algorithms/min-circuit.pdf
    """
    def __init__(self, n,m,bit_nbhd):
        """
        Input: n,m,bit_nbhd as defined in the class Classical_code
        create the adjacency matrix of the graph given 'bit_nbhd'
        adj_list[:n] represents the adjency lists of the n left vertices
        adj_list[n:] represents the adjency lists of the m right vertices
        """
        self.no_vertices = n + m
        self.n = n
        self.adj_list = [[c + n for c in bit_nbhd[v]] for v in range(n)] +\
                        bit_nbhd_to_check_nbhd(n,m,bit_nbhd)


    def is_left(self,u):
        """
        Returns True when the vertex 'u' is a left vertex of the bipartite graph
        """
        return u < self.n

    def to_ccode(self,n,m,dv,dc):
        """
        Returns the object of the class Classical_code represented by 'self'
        """
        bit_nbhd = [[u - n for u in nbhd] for nbhd in self.adj_list[:n]]
        check_nbhd = self.adj_list[n:]
        # is_regular(bit_nbhd, dv)
        # print(self.adj_list)
        return Classical_code(n,m,bit_nbhd,check_nbhd,dv,dc, "swap_" + str(uuid.uuid4())[:8])

    def find_shortest_cycle_for_vertex(self,u):
        """
        Input:
          'u' a vertex of the graph
        Ouput:
          A list of vertices of the graph representing a cycle in the graph
          This cycle does not necessarly contains 'u' but its size is smaller than the shorter cycle containing 'u'
        The idea of the algorithm is to perform a breadth-first search from 'u' and stop when we have already seen some vertex 'u2'.
        At this point we have two paths from 'u' to 'u2' of minimal length. Since the graph is bipartite, these paths have the same length.
        Given these two paths we can construct a cycle (which does not necessarly contains 'u').
        For more details see the article "FINDING A MINIMUM CIRCUIT IN A GRAPH*"
        """
        fifo = Queue(self.no_vertices)
        fifo.put(u,block = False)
        pred_array = [None for w in range(self.no_vertices)]
        pred_array[u] = u
        while not fifo.empty():
            u1 = fifo.get()
            # the boolean 'seen' is used to not use the same edge than previously
            seen = False
            for u2 in self.adj_list[u1]:
                if pred_array[u2] == None:                        
                    fifo.put(u2, block = False)
                    pred_array[u2] = u1
                elif not seen and u2 == pred_array[u1]:
                    seen = True
                else:
                    u3 = pred_array[u2]
                    u4 = u1
                    cycle = [u3,u2,u4]
                    while u3 != u4:
                        u3 = pred_array[u3]
                        u4 = pred_array[u4]
                        cycle.append(u4)
                        cycle.insert(0,u3)
                    return cycle
        # Should not happen for a regular bipartite graph:
        raise NameError('No cycle found')
    

    def find_shortest_cycle(self):
        """
        Returns the shortest cycle in the graph represented by a list of vertices
        """
        shortest_cycle = [0 for _ in range(self.no_vertices + 2)]
        for u in range(self.no_vertices):
            cycle = self.find_shortest_cycle_for_vertex(u)
            # print(" u = ", u, " cycle = ", cycle)
            if len(shortest_cycle) > len(cycle):
                shortest_cycle = cycle
        return shortest_cycle

    def swap_edges(self,edge1, edge2):
        """
        Input: edge1 and edge2 two edges in the graph we want to swap
        Be carefull: if (u1,u2) = edge1 and (u3,u4) = edge2 then u1 and u3 must be left vertices
          (thus u2 and u4 must be right vertices) otherwise we don't get a bipartite graph at the end.
        """
        # print(edge1, edge2)
        (u1,u2) = edge1
        (u3,u4) = edge2
        replace(self.adj_list[u1],u2,u4)
        replace(self.adj_list[u2],u1,u3)
        replace(self.adj_list[u3],u4,u2)
        replace(self.adj_list[u4],u3,u1)
        
    
    def remove_short_cycles(self, no_steps):
        """
        This function finds the shortest cycle and remove them
        """
        print_erase = Print_erase()
        cycle = self.find_shortest_cycle()
        for step in range(no_steps):
            s = "step=" + str(step) + ", cycle length=" + str(len(cycle)) + ", cycle=" + str(cycle) + "           "
            print_erase.print(s)
            
            i = randint(0,len(cycle) - 2)
            u1 = cycle[i]
            u2 = cycle[i + 1]
            if not self.is_left(u1):
                u1,u2 = u2,u1
            u3 = randint(0,self.no_vertices - 1)
            u4 = self.adj_list[u3][randint(0,len(self.adj_list[u3]) - 1)]
            if not self.is_left(u3):
                u3,u4 = u4,u3
            self.swap_edges((u1,u2),(u3,u4))
            # print(self.adj_list)
            previous_cycle = cycle
            cycle = self.find_shortest_cycle()
            if len(previous_cycle) > len(cycle):
                self.swap_edges((u1,u4),(u3,u2))
                cycle = previous_cycle
            

############ Swap edges 2 ############
# The goal is to construct regular bipartite graphs with large girth using swap of edges.
# We first generate a random graph using the configuration model and then remove small cycles.
# In order to remove a cycle we swap a random edge of this cycle with a random edge in the graph
# swap((u1,u2),(u3,u4)) --> (u1,u4),(u2,u3)


class Bip_graph2:
    """
    This class represents a bipartite graph as a non-bipartite graph with an adjacency matrix.
    The goal is to remove short cycle and then return a object of the class Classical_code
    Be carefull, the method find_shortest_cycle_for_vertex would not work if the graph was not bipartite.
    See "almost minimum circuit":
    http://perso.ens-lyon.fr/eric.thierry/Graphes2007/adrien-panhaleux.pdf (in french)
    or the original article "FINDING A MINIMUM CIRCUIT IN A GRAPH*":
    http://www.cs.technion.ac.il/~itai/publications/Algorithms/min-circuit.pdf
    """
    def __init__(self, n,m,bit_nbhd,dv,dc):
        """
        Input: n,m,bit_nbhd as defined in the class Classical_code
        create the adjacency matrix of the graph given 'bit_nbhd'
        adj_list[:n] represents the adjency lists of the n left vertices
        adj_list[n:] represents the adjency lists of the m right vertices
        """
        self.no_vertices = n + m
        self.n = n
        self.adj_list = [[c + n for c in bit_nbhd[v]] for v in range(n)] +\
                        bit_nbhd_to_check_nbhd(n,m,bit_nbhd)
        self.cycle_max_size = 10*math.ceil(math.log(n)/math.log(dv * dc))


    def is_left(self,u):
        """
        Returns True when the vertex 'u' is a left vertex of the bipartite graph
        """
        return u < self.n

    def to_ccode(self,n,m,dv,dc):
        """
        Returns the object of the class Classical_code represented by 'self'
        """
        bit_nbhd = [[u - n for u in nbhd] for nbhd in self.adj_list[:n]]
        check_nbhd = self.adj_list[n:]
        # is_regular(bit_nbhd, dv)
        # print(self.adj_list)
        return Classical_code(n,m,bit_nbhd,check_nbhd,dv,dc, "swap2_" + str(uuid.uuid4())[:8])

    def find_shortest_cycle_for_vertex(self,u):
        """
        Input:
          'u' a vertex of the graph
        Ouput:
          A list of vertices of the graph representing a cycle in the graph
          This cycle does not necessarly contains 'u' but its size is smaller than the shorter cycle containing 'u'
        The idea of the algorithm is to perform a breadth-first search from 'u' and stop when we have already seen some vertex 'u2'.
        At this point we have two paths from 'u' to 'u2' of minimal length. Since the graph is bipartite, these paths have the same length.
        Given these two paths we can construct a cycle (which does not necessarly contains 'u').
        For more details see the article "FINDING A MINIMUM CIRCUIT IN A GRAPH*"
        """
        fifo = Queue(self.no_vertices)
        fifo.put(u,block = False)
        pred_array = [None for w in range(self.no_vertices)]
        pred_array[u] = u
        while not fifo.empty():
            u1 = fifo.get()
            # the boolean 'seen' is used to not use the same edge than previously
            seen = False
            for u2 in self.adj_list[u1]:
                if pred_array[u2] == None:                        
                    fifo.put(u2, block = False)
                    pred_array[u2] = u1
                elif not seen and u2 == pred_array[u1]:
                    seen = True
                else:
                    u3 = pred_array[u2]
                    u4 = u1
                    cycle = [u3,u2,u4]
                    while u3 != u4:
                        u3 = pred_array[u3]
                        u4 = pred_array[u4]
                        cycle.append(u4)
                        cycle.insert(0,u3)
                    if u3 == u:
                        return cycle
        # Should not happen for a regular bipartite graph:
        raise NameError('No cycle found')

    def cycle_size_to_index(self, cycle_size):
        return (cycle_size - 3)//2

    def find_shortest_cycle(self):
        """
        Returns the shortest cycle in the graph represented by a list of vertices
        """
        shortest_cycle_list = []
        shortest_cycle_size = self.no_vertices + 2
        cycle_hist = [0 for _ in range(self.cycle_size_to_index(self.cycle_max_size) + 1)]
        for u in range(self.no_vertices):
            cycle = self.find_shortest_cycle_for_vertex(u)
            # print(" u = ", u, " cycle = ", cycle)
            cycle_hist[self.cycle_size_to_index(len(cycle))] += 1
            if shortest_cycle_size > len(cycle):
                shortest_cycle_list = [cycle]
                shortest_cycle_size = len(cycle)
            elif shortest_cycle_size == len(cycle):
                shortest_cycle_list.append(cycle)
        return (shortest_cycle_list, tuple(cycle_hist))

    def swap_edges(self,edge1, edge2):
        """
        Input: edge1 and edge2 two edges in the graph we want to swap
        Be carefull: if (u1,u2) = edge1 and (u3,u4) = edge2 then u1 and u3 must be left vertices
          (thus u2 and u4 must be right vertices) otherwise we don't get a bipartite graph at the end.
        """
        # print(edge1, edge2)
        (u1,u2) = edge1
        (u3,u4) = edge2
        replace(self.adj_list[u1],u2,u4)
        replace(self.adj_list[u2],u1,u3)
        replace(self.adj_list[u3],u4,u2)
        replace(self.adj_list[u4],u3,u1)
        
    
    def remove_short_cycles(self, no_fails):
        """
        This function finds the shortest cycle and remove them
        """
        print_erase = Print_erase()
        shortest_cycle_list, cycle_hist = self.find_shortest_cycle()
        fails = 0
        while fails < no_fails:
            s = "fails=" + str(fails) + ", cycle histograme=" + str(cycle_hist) + ", shortest cycle = " + str(shortest_cycle_list[0]) + "           "
            print_erase.print(s)

            j = randint(0,len(shortest_cycle_list) - 1)
            cycle = shortest_cycle_list[j]
            i = randint(0,len(cycle) - 2)
            u1 = cycle[i]
            u2 = cycle[i + 1]
            if not self.is_left(u1):
                u1,u2 = u2,u1
            u3 = randint(0,self.no_vertices - 1)
            u4 = self.adj_list[u3][randint(0,len(self.adj_list[u3]) - 1)]
            if not self.is_left(u3):
                u3,u4 = u4,u3
            self.swap_edges((u1,u2),(u3,u4))
            # print(self.adj_list)
            shortest_previous_cycle_list = shortest_cycle_list
            previous_cycle_hist = cycle_hist
            shortest_cycle_list, cycle_hist = self.find_shortest_cycle()
            if cycle_hist > previous_cycle_hist:
                self.swap_edges((u1,u4),(u3,u2))
                shortest_cycle_list = shortest_previous_cycle_list
                cycle_hist = previous_cycle_hist
                fails += 1
            elif cycle_hist < previous_cycle_hist:
                fails = 0
            

############ Swap edges 3 ############
# The goal is to construct regular bipartite graphs with large girth using swap of edges.
# We first generate a random graph using the configuration model and then remove small cycles.
# In order to remove a cycle we swap a random edge of this cycle with a random edge in the graph
# swap((u1,u2),(u3,u4)) --> (u1,u4),(u2,u3)


class My_queue:
    def __init__(self, max_size):
        self.size = 0
        self.array = [0 for _ in range(max_size)]

    def put(self, e):
        self.array[self.size] = e
        self.size += 1

    def get_size(self):
        return self.size

    def random_elem(self):
        return self.array[randint(0,self.size-1)]

    def return_first(self):
        return self.array[0]

    def reset(self):
        self.size = 0

# Removes the first occurence of "a" in "L"
def remove_elem(L,a):
    for i in range(len(L)):
        if a == L[i]:
            return L[:i] + L[i+1:]
    raise NameError('Problem remove_elem')


class Bip_graph3:
    """
    This class represents a bipartite graph as a non-bipartite graph with an adjacency matrix.
    The goal is to remove short cycle and then return a object of the class Classical_code
    Be carefull, the method find_shortest_cycle_for_vertex would not work if the graph was not bipartite.
    See "almost minimum circuit":
    http://perso.ens-lyon.fr/eric.thierry/Graphes2007/adrien-panhaleux.pdf (in french)
    or the original article "FINDING A MINIMUM CIRCUIT IN A GRAPH*":
    http://www.cs.technion.ac.il/~itai/publications/Algorithms/min-circuit.pdf
    """
    def __init__(self, ccode):
        """
        Input: n,m,bit_nbhd as defined in the class Classical_code
        create the adjacency matrix of the graph given 'bit_nbhd'
        adj_list[:n] represents the adjency lists of the n left vertices
        adj_list[n:] represents the adjency lists of the m right vertices
        """
        self.ccode = ccode
        self.bit_adj_mat = np.zeros((self.ccode.n, self.ccode.m), int)
        for v in range(self.ccode.n):
            for c in self.ccode.bit_nbhd[v]:
                self.bit_adj_mat[v,c] += 1
        self.check_adj_mat = self.bit_adj_mat.transpose()
        self.init_dijkstra()

    def init_dijkstra(self):
        self.old_path = np.zeros((self.ccode.n, self.ccode.m), int)
        self.path = np.eye(self.ccode.n, self.ccode.n, dtype = int)
        self.path_len = 0
    
    def path_step(self):
        old_old_path, self.old_path = self.old_path, self.path
        if self.path_len % 2:
            self.path = np.dot(self.old_path, self.check_adj_mat) - (self.ccode.dv - 1) * old_old_path
        else:
            self.path = np.dot(self.old_path, self.bit_adj_mat) - (self.ccode.dc - 1) * old_old_path
        self.path_len += 1

    def compute_score(self):
        # if (self.path_len % 2) == 0:
        #     for v1 in range(self.path.shape[0]):
        #         for v2 in range(self.path.shape[0]):
        #             if self.path[v1,v2] != self.path[v2,v1]:
        #                 print("PROBLEM: v1 = ", v1, ", v2 = ", v2, "path[v1,v2] = ", self.path[v1,v2], "path[v2,v1] = ", self.path[v2,v1])
        no_cycles_list = [0 for v in range(self.ccode.n)]
        for v in range(self.ccode.n):
            for u in range(self.path.shape[1]):
                # if self.path[v,u] < 0:
                #     print("PROBLEM444: v = ", v, ", u = ", u, "self.path[v,u] = ", self.path[v,u])
                no_cycles_list[v] += self.path[v,u] * (self.path[v,u] - 1)

        max_no_cycles = 0
        self.bad_vertices = []
        for v in range(self.ccode.n):
            if no_cycles_list[v] > max_no_cycles:
                max_no_cycles = no_cycles_list[v]
                self.bad_vertices = [v]
            elif no_cycles_list[v] == max_no_cycles:
                self.bad_vertices.append(v)
                
        if max_no_cycles == 0:
            self.path_step()
            return self.compute_score()
        
        hist = [0 for no_cycles in range(max_no_cycles + 1)]
        for no_cycles in no_cycles_list:
            hist[no_cycles] += 1
        cycle_length = 2*self.path_len

        # for v in self.bad_vertices:
        #     good = False
        #     for u in range(self.path.shape[1]):
        #         if self.path[v,u] > 1:
        #             good = True
        #     if not good:
        #         print("PROBLEM222: v = ", v)

        # if hist[max_no_cycles] != len(self.bad_vertices):
        #     print("PROBLEM333: hist[max_no_cycles] = ", hist[max_no_cycles], ", len(self.bad_vertices) = ", len(self.bad_vertices))

        return tuple([cycle_length] + [(-no_cycles, -hist[no_cycles]) for no_cycles in range(len(hist)-1,-1,-1) if hist[no_cycles] != 0])

    
    def swap_edges(self,edge1, edge2):
        """
        Input: edge1 and edge2 two edges in the graph we want to swap
        Be carefull: if (u1,u2) = edge1 and (u3,u4) = edge2 then u1 and u3 must be left vertices
        (thus u2 and u4 must be right vertices) otherwise we don't get a bipartite graph at the end.
        """
        # print(edge1, edge2)
        (v1,c1) = edge1
        (v2,c2) = edge2
        
        replace(self.ccode.bit_nbhd[v1], c1,c2)
        replace(self.ccode.bit_nbhd[v2], c2,c1)
        replace(self.ccode.check_nbhd[c1], v1,v2)
        replace(self.ccode.check_nbhd[c2], v2,v1)
        self.bit_adj_mat[v1,c1] -= 1
        self.bit_adj_mat[v1,c2] += 1
        self.bit_adj_mat[v2,c2] -= 1
        self.bit_adj_mat[v2,c1] += 1
        # No need to update updates check_adj_mat because when we update bit_adj_mat, check_adj_mat is updated
        

        
    def remove_short_cycles(self, no_fails):
        """
        This function finds the shortest cycle and remove them
        Be carefull: if (u1,u2) = edge1 and (u3,u4) = edge2 then u1 and u3 must be left vertices
        (thus u2 and u4 must be right vertices) otherwise we don't get a bipartite graph at the end.
        """
        print_erase = Print_erase()
        best_score = self.compute_score()
        best_bad_vertices = self.bad_vertices
        best_path = self.path
        best_old_path = self.old_path
        best_path_len = self.path_len
        fails = 0
        while fails < no_fails:
            s = "fails=" + str(fails) + ", score=" + str(best_score) + "           "
            print_erase.print(s)

            (v1,c1) = compute_random_bad_edge(self.ccode, best_bad_vertices, best_path, best_old_path, best_path_len)
            v2 = randint(0,self.ccode.n - 1)
            c2 = self.ccode.bit_nbhd[v2][randint(0,len(self.ccode.bit_nbhd[v2]) - 1)]
            self.swap_edges((v1,c1), (v2,c2))
            self.init_dijkstra()
            new_score = self.compute_score()
            if new_score > best_score:
                fails = 0
            else:
                fails += 1
            if new_score >= best_score:
                best_score = new_score
                best_bad_vertices = self.bad_vertices
                best_path = self.path
                best_old_path = self.old_path
                best_path_len = self.path_len
            else:
                self.swap_edges((v1,c2),(v2,c1))
        del(print_erase)
        print("final_score = " + str(best_score))
        return self.ccode



def compute_random_bad_edge(ccode, bad_vertices, path, old_path, path_len):
    # for v in bad_vertices:
    #     good = False
    #     for u in range(path.shape[1]):
    #         if path[v,u] > 1:
    #             good = True
    #     if not good:
    #         print("PROBLEM: v = ", v)
    v0 = bad_vertices[randint(0,len(bad_vertices) - 1)]
    u_list = [u for u in range(path.shape[1]) if path[v0,u] > 1]
    # if len(u_list) == 0:
    #     print()
    #     print("path_len = ", path_len)
    #     print("bad_vertices = ", bad_vertices)
    #     for v0 in range(path.shape[0]):
    #         for u in range(path.shape[1]):
    #             if path[v0,u] > 1:
    #                 print("AAAAAAAAAAAAAAAAAa : path[", v0, ',', u, " = ", path[v0,u])
    u = u_list[randint(0,len(u_list) - 1)]
    
    if path_len % 2:
        c = u
        v_list = [v for v in ccode.check_nbhd[c] if old_path[v0,v] > 0]
        v = v_list[randint(0,len(v_list) - 1)]                      
    else:
        v = u
        c_list = [c for c in ccode.bit_nbhd[v] if old_path[v0,c] > 0]
        c = c_list[randint(0,len(c_list) - 1)]
    return (v,c)
