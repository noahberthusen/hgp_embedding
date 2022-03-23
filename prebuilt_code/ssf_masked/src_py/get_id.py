import sys
from read_ccodes import read_ccode, Classical_code



def get_id():
    code_list = read_ccode(sys.argv[1:], [],[],[],[],[])
    print("swac_average_" + str(code_list[0].dv) + "_" + str(code_list[0].dc) + "_"  + str(code_list[0].n) + "_"  + str(code_list[0].m) + " = ", end = "")
    print("[", end = "")
    for code in code_list:
        print ('"' + code.id + '",', end = " ")
    print("\b\b]")
get_id()
