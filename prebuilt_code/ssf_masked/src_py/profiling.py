#profiling

from print_erase import*
from decoder import*
from configuration_model import*
from line_profiler import LineProfiler
import time


#### If main change

n = 100
m = 80
dv = 4
dc = 5
patience = 1000000000
p = 0.01

ccode = configuration_model(n,m,dv,dc,patience)

xerror = random_error(ccode, p)
synd_matrix = compute_synd_matrix(ccode, xerror)

#lp = LineProfiler()
#lp.add_function(Lookup_table.update_score_generator)
#lp.add_function(Lookup_table.update)
#lp.add_function(Lookup_table.find_best_gen)
#lp.add_function(hor_subset_score)
#lp.add_function(score_gen)
#lp_wrapper = lp(decoder)
#lp_wrapper(ccode,synd_matrix)
#lp.print_stats()

start = time.time()
decoder(ccode,synd_matrix)
duration = time.time() - start
print(duration)

###############################
