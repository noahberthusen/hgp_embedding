import sys
import default_names
from configuration_model import configuration_model, compute_rand_bit_nbhd, bit_nbhd_to_check_nbhd, Bip_graph, Bip_graph2, Bip_graph3
from read_ccodes import write_ccode
from decoder import Classical_code
import argparse
import uuid



#Run this file to generate classical codes

###################################################   
n = 360
m = 300
dv = 5
dc = 6
no_codes = 10
##############
# 'no_steps' is not used for configuration model
no_steps = 10000
##############
# 'patience'
patience = 10000000000000000000000

###################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--swap', default = 3,type=int,help = "Swap trick is used to remove short cycles. \n 0: Do not use swap trick \n 1: use simple swap trick \n >2: use elaborate swap trick")
    parser.add_argument('-o', default = "", help = "file where we store the codes")
    args = parser.parse_args()
    if args.o == "":
        args.o = default_names.ccode_file_name(n,m,dv,dc,args.swap)
        

    

def generate_config(n,m,dv,dc,patience,no_codes, output_file):
    s = "n = " + str(n) + " ,m = " + str(m) + " ,dv = " + str(dv) + " ,dc = " + str(dc)
    print(s)

    #Code stored as n_m_dv_dc.code
    for i in range(no_codes):
        ccode = configuration_model(n,m,dv,dc, patience)
        write_ccode(output_file, ccode)



def generate_swap(n,m,dv,dc, no_steps, output_file, no_codes):
    for _ in range(no_codes):
        bit_nbhd = compute_rand_bit_nbhd(n, m, dv, dc)
        graph = Bip_graph(n,m,bit_nbhd)
        graph.remove_short_cycles(no_steps)
        ccode = graph.to_ccode(n,m,dv,dc)
        write_ccode(output_file,ccode)


def generate_swap2(n,m,dv,dc, no_steps, output_file, no_codes):
    for _ in range(no_codes):
        bit_nbhd = compute_rand_bit_nbhd(n, m, dv, dc)
        graph = Bip_graph2(n,m,bit_nbhd,dv,dc)
        graph.remove_short_cycles(no_steps)
        ccode = graph.to_ccode(n,m,dv,dc)
        write_ccode(output_file,ccode)


def generate_swap3(n,m,dv,dc, no_steps, output_file, no_codes):
    for a in range(no_codes):
        print("\nattempt = " + str(a))
        bit_nbhd = compute_rand_bit_nbhd(n, m, dv, dc)
        check_nbhd = bit_nbhd_to_check_nbhd(n,m,bit_nbhd)
        code_id = "swap3_" + str(uuid.uuid4())[:8]
        print("code_id = ", code_id)
        ccode = Classical_code(n, m, bit_nbhd, check_nbhd, dv, dc, code_id, not_regular = True)
        graph = Bip_graph3(ccode)
        ccode = graph.remove_short_cycles(no_steps)
        write_ccode(output_file,ccode)

        
print("output file = ", args.o)
if args.swap == 0:
    generate_config(n,m,dv,dc,patience,no_codes, args.o)
elif args.swap == 1:
    generate_swap(n,m,dv,dc, no_steps, args.o, no_codes)
elif args.swap == 2:
    generate_swap2(n,m,dv,dc, no_steps, args.o, no_codes)
else:
    generate_swap3(n,m,dv,dc, no_steps, args.o, no_codes)

