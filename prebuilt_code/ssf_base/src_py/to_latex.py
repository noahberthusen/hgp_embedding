import default_names
from read_result import file_to_res_list
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', default = default_names.summary_res_file, help = "file where the results are stored")
    args = parser.parse_args()


id_list_5_6 = [
    "swap_84f2e5cd",
    "swap_12f5a4a2",
    "swap_82698d8d",
    "swap_2e55c0b2",
    "swap_877f956a",
    "swap_54d39ebd"
]        


nv_list = [120,240,360,480,600,720]
for nv in nv_list:
    res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list_5_6, nv = [nv], algo = [2],p_phys = [0.005*k for k in range(11)])

    print("\\begin{figure}[!h]")
    print("\\begin{tabular}{| l | l | l | l |}")
    print("\\hline")
    print("$p$ & number success & number tests & logical failure rate\\\\")
    print("\\hline")
    for res in res_list:
        print(
            str(res.p_phys) + " & "\
            + str(res.no_success) + " & "\
            + str(res.no_test) + " & " +\
            str(1 - res.no_success/res.no_test)\
            + "\\\\"
        )
        print("\\hline")
    print("\\end{tabular}")
    print("\\caption{test}")
    print("\\end{figure}")
    print()



#######################################
