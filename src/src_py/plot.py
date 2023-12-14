import matplotlib
import default_names
import numpy as np
import matplotlib.pyplot as plt
from read_result import file_to_res_list
import argparse
import math

# id_list_4_8 = ["swap_566a5203","swap_21c6740d","swap_ca41e16b","swap_a501cc2e"]
# id_list_5_10 = ["swap_1a33b842", "swap_6822f6e8","swap_adc9817d", "swap_07d96dd9"]
id_list_5_6 = [
    "swap_84f2e5cd",
    "swap_12f5a4a2",
    "swap_82698d8d",
    "swap_2e55c0b2",
    "swap_877f956a",
    "swap_54d39ebd"
]
# id_list_6_7 = ["swap_b5f4dc91","swap_c9cc9a21","swap_5ca99d9d","swap_3975e341","swap_dee99e3d","swap_8cab59e4"]
# id_list_8_9 = ["swap_48aae4fa","swap_24daeba6","swap_0c8ee978","swap_3deb9a09","swap_48aae4fa","swap_93d4cf34"]

swac_2_3 = ["swac_14hurvlg","swac_r76atqit","swac_171zvbxe","swac_85ekmrn4"]
swac_3_4 = ["swac_7l1sv8iy","swac_3n2f0xa1","swac_rar3cas1","swac_ow6ao3z2","swac_sdel6k8v"]
swac_4_5 = ["swac_r9ozxmw0", "swac_vp6jg8gh", "swac_8jqa7eoy", "swac_zcfyv65i","swac_q4akt8vh","swac_yg5w33i9"]
swac_5_6 = ["swac_zxe5e53k", "swac_aa0e3did", "swac_3bs3ixvl", "swac_7sxu71qo", "swac_gahdc3t2", "swac_4pi117ny"]
swac_6_7 = ["swac_5v3dbny1", "swac_tehn0c5b", "swac_898mw3gp","swac_v4mfwfuf"]
swac_7_8 = ["swac_r7jn5dba","swac_pz9pubqq","swac_0c2mm9k1","swac_xtj4iqdq"]

swac_3_6 = ["swac_hclkvm7d","swac_gs7k6hnl","swac_7lpo8kki","swac_ndvmu7g3"]
swac_4_8 = ["swac_g65zrxe9","swac_orcmleza","swac_psgkt83v","swac_nbalf2gt"]
swac_5_10 = ["swac_kh5gx202", "swac_v8k8bnsa", "swac_k2egpilf", "swac_29a1o97d", "swac_0bayd0vy", "swac_bjrt8akm"]
swac_6_12 = ["swac_332a94ia","swac_l2nq9cel","swac_l6sd5atn"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', default = default_names.summary_res_file, help = "file where the results are stored")
    args = parser.parse_args()


# Input:
#   'res_list' = list of objects of class Result we want to plot
#   'abscissa' = the parameter of the object on abscissa
#   'ordinate' = the parameter of the object on ordinate
#   'fixed_param_list' = list of parameters for a given color in the plot. For example fixed_param_list = ['code_id'] means that each code_id will have its own color
#   'fct_abscissa' the function applied to the r.abscissa before plotting (for log scale...)
#   'fct_ordinate' the function applied to the r.ordinate before plotting (for log scale...)
def plot(res_list, abscissa = 'p_phys', ordinate = 'p_log', fixed_param_list = ['algo','dv','dc','nv','nc','code_id'], fct_abscissa = lambda x: x, fct_ordinate = lambda x: x, xlabel = 'Physical error rate', ylabel = 'Block error rate'):

    res_dict_list = [r.__dict__ for r in res_list]
    for res_dict in res_dict_list:
        res_dict['p_log'] = 1 - res_dict['no_success']/res_dict['no_test']

    points = dict()
    for res_dict in res_dict_list:
        label = tuple(res_dict[p] for p in fixed_param_list)
        res_point = (fct_abscissa(res_dict[abscissa]), fct_ordinate(res_dict[ordinate]))
        if label in points.keys():
            points[label].append(res_point)
        else:
            points[label] = [res_point]

    label_list = list(points.keys())
    label_list.sort()

    #mark = ["X","D","P","*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    mark = ["*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    i_mark = 0
    for label in label_list:
        marker=mark[i_mark]
        i_mark = (i_mark+1) % len(mark)
        s = ''
        for i in range(len(fixed_param_list)):
            s += fixed_param_list[i] + ' = ' + str(label[i]) + ', '
        x_list = [p[0] for p in points[label]]
        y_list = [p[1] for p in points[label]]
        plt.scatter(x_list,y_list, label = s, marker=marker, s = 60)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(prop={'size':8})
    plt.show()



from math import log

def fct_log(p):
    if p == 0:
        return -10
    return log(p,10)



#################################################################################################
# The function log_plot plots p_phys in absica and p_log in oridinate with log scale for ordinate and with error bar
#################################################################################################
import scipy.stats
plt.style.use('seaborn-whitegrid')

# One curve represents one code, p_log in ordinate and p_phys in absica
class Curve:
    def __init__(self,res):

        #self.label = 'n = '  + str(res.nv) + ', m = '  + str(res.nc)
        self.label = '[[' + str(res.nv*res.nv + res.nc*res.nc) + ',' + str(res.nv*res.nv + res.nc*res.nc - 2*res.nv*res.nc) + ']]'
        # self.label = 'algo = ' + str(res.algo) + \
        #         ', n = '  + str(res.nv) + \
        #         ', m = '  + str(res.nc) + \
        #         ', dv = '  + str(res.dv) + \
        #         ', dc = '  + str(res.dc) + \
        #         ', id = '  + res.code_id
        # self.label = 'n = '  + str(res.nv) + \
        #     ', m = '  + str(res.nc) + \
        #     ', dv = '  + str(res.dv) + \
        #     ', dc = '  + str(res.dc)
        self.p_phys_list = []
        self.p_log_list = []
        self.standard_error_list = []
        self.label_dict = dict()
        self.label_dict['algo'] = res.algo
        self.label_dict['nv'] = res.nv
        self.label_dict['nc'] = res.nc
        # self.label_dict['dv'] = res.dv
        # self.label_dict['dc'] = res.dc
        # self.label_dict['code_id'] = res.code_id

    def add(self, res, block_success_rate = False):
        if block_success_rate:
            p_log = res.no_success/res.no_test
        else:
            p_log = 1 - res.no_success/res.no_test
        if p_log != 0:
            self.p_phys_list.append(res.p_phys)
            standard_error = math.sqrt(p_log * (1 - p_log) / res.no_test)
            self.p_log_list.append(p_log)
            self.standard_error_list.append(standard_error)

    def __lt__(self, other):
        label_list = ['algo','nv','nc','dv','dc','code_id']
        for l in label_list:
            if self.label_dict[l] < other.label_dict[l]:
                return True
            elif self.label_dict[l] > other.label_dict[l]:
                return False
        return True

    def same_parameter(self,other):
        label_list = ['algo','nv','nc','dv','dc']
        for l in label_list:
            if self.label_dict[l] != other.label_dict[l]:
                return False
        return True



def log_plot(res_list, confidence, block_success_rate = False, linestyle = ''):
    # From http://hamelg.blogspot.com/2015/11/python-for-data-analysis-part-23-point.html
    z_critical = scipy.stats.norm.ppf(q = 1-(1-confidence)/2)

    curve_dict = dict()
    for res in res_list:
        if not(res.code_id in curve_dict.keys()):
            curve_dict[res.code_id] = Curve(res)
        curve_dict[res.code_id].add(res, block_success_rate)

    curve_list = [curve_dict[code_id] for code_id in curve_dict.keys()]
    curve_list.sort()

    #mark = ["X","D","P","*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    mark = ["*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    i_mark = 0
    colors = ['#191970', '#00008B', '#0000FF', '#8A2BE2', '#483D8B', '#7B68EE', '#8B008B']
    for curve in curve_list:
        #marker=mark[i_mark]
        marker = "o"
        coulor=colors[i_mark]
        i_mark = (i_mark+1) % len(mark)
        if confidence == 0:
            yerr = None
        else:
            yerr = [z_critical * se for se in curve.standard_error_list]
        # MODIFIED TO MAKE SPARSE PLOT! REMOVE TO GO BACK TO NORMAL!]
        modified_indices = [i for i in range(len(curve.p_phys_list)) if curve.p_phys_list[i]*(10**(3))%5 == 0]
        x = np.array(curve.p_phys_list)[modified_indices]
        y = np.array(curve.p_log_list)[modified_indices]
        yerr = np.array(yerr)[modified_indices]
        # End added lines, change x, y to curve.p_phys_list and curve.p_log_list resp. below. No need to change yerr.
        plt.errorbar(x, y, yerr = yerr , label = curve.label, marker=marker, ms = 4, ls = 'None', capthick=1, capsize=5, elinewidth=1, linestyle = linestyle, color=coulor)
        plt.plot(x, y, coulor)

    #### Legend
    fontsize = 17
    plt.yscale('log')
    if block_success_rate:
        plt.ylabel('Block success rate',fontsize=fontsize)
    else:
        plt.ylabel('-log(WER)',fontsize=fontsize)
    plt.xlabel('Physical error rate (%)',fontsize=fontsize)
    legend = plt.legend(prop={'size':15}, frameon = True)
    axes = plt.gca()
    #axes.xaxis.set_ticks([0.00 + k*0.008 for k in range(0,7)])
    xlocs = np.array([0.00 + k*0.005 for k in range(0,6)])
    ylocs = np.array([10**(-k) for k in range(0,3)])
    ytics = np.array([k for k in range(0,8)])
    #plt.xticks(xlocs,10*10*10*xlocs/10,rotation=45,horizontalalignment='right',fontsize=fontsize)
    plt.xticks(xlocs,10*10*10*xlocs/10,fontsize=fontsize)
    plt.yticks(ylocs,ytics,fontsize=fontsize)
    plt.grid(True,which="both", linestyle='--')
    plt.show()




# #############
# # Modify here
# # USE QUOTES !
# id_list = id_list_4_8
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [0])
# confidence = 0
# log_plot(res_list, confidence)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_4_5
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2],p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_2_3
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2],p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################



# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_3_4
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2],p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_4_5
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2],p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################

# #############
# # Modify here
# # USE QUOTES !
id_list = swac_5_6
res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [60*k for k in range(1,7)], algo = [2],p_phys = [])
confidence = 0.99
#plot(res_list, confidence, block_success_rate = True)
#log_plot(res_list, confidence, block_success_rate = False)
#fixed_param_list = ['nv','nc','dv','dc']
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_6_7
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2],p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_7_8
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2],p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_3_6
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2], p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_4_8
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2], p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################


#############
# Modify here
# USE QUOTES !
id_list = swac_5_10
res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2], p_phys = [])
confidence = 0.99
log_plot(res_list, confidence, block_success_rate = False)
##fixed_param_list = ['nv','nc','dv','dc']
########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_6_12
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2], p_phys = [])
# confidence = 0.99
# log_plot(res_list, confidence, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################



# #############
# # Modify here
# # USE QUOTES !
# id_list = id_list_4_8
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [0])
# plot(res_list, fixed_param_list = ['algo', 'nv','nc','dv','dc', 'code_id'], fct_ordinate = fct_log, ylabel = 'log(p_log)')
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################

# #############
# # Modify here
# # USE QUOTES !
#id_list = id_list_5_6
#res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2])
#plot(res_list, fixed_param_list = ['algo', 'nv','nc','dv','dc', 'code_id'], fct_ordinate = fct_log, ylabel = 'log(p_log)')
#fixed_param_list = ['nv','nc','dv','dc']
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# id_list = id_list_4_8
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [])
# plot(res_list, fixed_param_list = ['nv','nc','dv','dc', 'code_id'])
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# id_list = ["swap_b5f4dc91","swap_c9cc9a21","swap_5ca99d9d","swap_3975e341","swap_dee99e3d","swap_8cab59e4"]
# id_list = id_list + ["swap_48aae4fa","swap_24daeba6","swap_0c8ee978","swap_3deb9a09","swap_48aae4fa","swap_93d4cf34"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[4], dc = [8], code_id = id_list, nv = [], algo = [2])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# id_list = ["swap_b5f4dc91","swap_c9cc9a21","swap_5ca99d9d","swap_3975e341","swap_dee99e3d","swap_8cab59e4"]
# id_list = id_list + ["swap_48aae4fa","swap_24daeba6","swap_0c8ee978","swap_3deb9a09","swap_48aae4fa","swap_93d4cf34"]
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [1,2])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = ["swap_24daeba6", "swap_0c8ee978","swap_3deb9a09","swap_48aae4fa"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[8], dc = [9], code_id = id_list, nv = [], algo = [2])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[8], dc = [9], code_id = id_list, nv = [], algo = [1,2,3,4,5,6,7,8])
# plot(res_list)
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[8], dc = [9], code_id = id_list, nv = [540])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[8], dc = [9], code_id = id_list, nv = [720])
# plot(res_list)
# ########################################



# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[8], dc = [9], code_id = id_list, nv = [900])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = ["swap_24daeba6", "swap_0c8ee978"]
# res_list = file_to_res_list(args.i, dv=[8], dc = [9], code_id = id_list, nv = [])
# plot(res_list)
# ########################################




# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[8], dc = [9], code_id = id_list, nv = [540])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = ["swap_68d86811"]
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [])
# plot(res_list,fct_ordinate = lambda p: math.sqrt(p))
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[8], dc = [16], code_id = id_list, nv = [])
# plot(res_list)
# ########################################*


# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = ["swap_90bc683e", "swap_e7c8873e", "swap_9bef0811", "swap_e2ec6688","0c350536"]
# res_list = file_to_res_list(args.i, dv=[4], dc = [5], algo = [],code_id = id_list, nv = [])
# plot(res_list)
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[6], dc = [7], code_id = id_list, nv = [70])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[6], dc = [7], code_id = id_list, nv = [140])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[6], dc = [7], code_id = id_list, nv = [210])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[6], dc = [7], code_id = id_list, nv = [280])
# plot(res_list)
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[6], dc = [7], code_id = id_list, nv = [350])
# plot(res_list)
# ########################################


# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[6], dc = [7], code_id = id_list, nv = [420])
# plot(res_list)
########################################



# #############
# # Modify here
# # USE QUOTES !
# # id_list = ["62451bf5","77ef9586","0c350536","ee718ff0"]
# id_list = []
# res_list = file_to_res_list(args.i, dv=[6], dc = [7], code_id = id_list, nv = [700])
# plot(res_list)
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# id_list = ["swap_8cab59e4","swap_dee99e3d","swap_b5f4dc91","swap_c9cc9a21", "swap_5ca99d9d", "swap_3975e341"]
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [1])
# plot(res_list, fixed_param_list = ['nv','nc','dv','dc', 'code_id'], fct_ordinate = lambda p: fct_log(1-p), ylabel = 'log(1 - p_log)')
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################

# #############
# # Modify here
# # USE QUOTES !
# id_list = ["swap_8cab59e4","swap_dee99e3d","swap_b5f4dc91","swap_c9cc9a21", "swap_5ca99d9d"]
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [0])
# plot(res_list, fixed_param_list = ['nv','nc','dv','dc'])
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################

########################################

#############
# # Modify here
# # USE QUOTES !
# id_list = ["62451bf5","77ef9586","0c350536","ee718ff0", "swap_5ca99d9d"]
# # id_list = []
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [1], p_phys = [])

# from math import log

# def fct_log(p):
#     if p == 0:
#         return 0
#     return log(p,10)

# plot(res_list, fct_ordinate = fct_log, abscissa = 'nv', ordinate = 'p_log', fixed_param_list = ['p_phys'])
# ########################################




################ Comparition with toric code ################
# One curve represents one code family for a given p_phys, p_log in ordinate and the number of logical qubits in ordinate
class Curve2:
    def __init__(self,res, confidence):
        # From http://hamelg.blogspot.com/2015/11/python-for-data-analysis-part-23-point.html
        self.z_critical = scipy.stats.norm.ppf(q = 1-(1-confidence)/2)

        self.label = "Hypergraph product, p = "  + str(res.p_phys)

        # self.label = 'algo = ' + str(res.algo) + \
        #         ', dv = '  + str(res.dv) + \
        #         ', dc = '  + str(res.dc) + \
        #         ', p_phys = '  + str(res.p_phys)
        self.no_logicals_list = []
        self.p_log_list = []
        self.p_log_errorbar_list = []
        self.n_list = []
        self.p_phys = res.p_phys

    def add(self, res):
        p_log = 1 - res.no_success/res.no_test
        if p_log != 0:
            self.no_logicals_list.append(res.nv * res.nv + res.nc * res.nc - 2 * res.nv * res.nc)
            p_log_errorbar = self.z_critical * math.sqrt(p_log * (1 - p_log) / res.no_test)
            self.p_log_list.append(p_log)
            self.p_log_errorbar_list.append(p_log_errorbar)
            self.n_list.append(res.nv)

    def __lt__(self, other):
        return self.label < other.label



import scipy.optimize as opt;



# TODO: add confidence for toric code
def log_plot2(res_list, confidence, no_logicals_max, func_to_fit, n_not_to_fit = [], plot_toric = True):
    # Results for L = 8 toric code {p_phys: (no_success, no_tests)}
    res_toric = {0.005: (50,80000000), 0.01: (105,10000000), 0.015: (703,10000000), 0.02: (2599,10000000), 0.025: (7381,10000000), 0.03: (17321,10000000)}

    curve_dict = dict()
    for res in res_list:
        key = (res.dv,res.dc,res.p_phys)
        if not(key in curve_dict.keys()):
            curve_dict[key] = Curve2(res, confidence)
        curve_dict[key].add(res)

    curve_list = [curve_dict[key] for key in curve_dict.keys()]
    curve_list.sort(reverse = True)

    #mark = ["X","D","P","*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    mark = ["*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    i_mark = 0
    color_list = ["black", "red", "blue", "green", "yellow", "purple"]
    i_color = 0

    #### Plots hypergraph product curves
    for curve in curve_list:
        marker=mark[i_mark]
        i_mark = (i_mark+1) % len(mark)
        color = color_list[i_color]
        i_color = (i_color+1) % len(color_list)
        plt.errorbar(curve.no_logicals_list, curve.p_log_list, yerr = curve.p_log_errorbar_list , label = curve.label, marker=marker, ms = 15, ls = 'None', capthick=1, capsize=5, elinewidth=1, color = color)

        # Plots the fit
        # no_logicals_list, p_log_list, p_log_errorbar_list = [],[],[]

        # for i in range(len(curve.n_list)):
        #     if curve.n_list[i] not in n_not_to_fit:
        #         no_logicals_list.append(curve.no_logicals_list[i])
        #         p_log_list.append(curve.p_log_list[i])
        #         p_log_errorbar_list.append(curve.p_log_errorbar_list[i])
        # optimizedParameters, pcov = opt.curve_fit(func_to_fit, no_logicals_list, p_log_list, sigma = p_log_errorbar_list);
        # x = range(no_logicals_max)
        # plt.plot(x, [func_to_fit(x0, *optimizedParameters) for x0 in x], '--', color = color);
        # print(optimizedParameters)


        #### Plots toric code curves
        if plot_toric:
            no_logicals_list = range(no_logicals_max)
            no_success = res_toric[curve.p_phys][0]
            no_tests = res_toric[curve.p_phys][1]
            p_log = no_success/no_tests
            p_log_list = [1 - (1 - p_log)**(k/2) for k in no_logicals_list]
            plt.plot(no_logicals_list, p_log_list, color = color#, label = 'Toric code L = 8, p = ' + str(curve.p_phys), # , marker=marker, ms = 8, ls = 'None', capthick=1, capsize=5, elinewidth=1
            )

        # ### With filling
        # no_success = res_toric[p_phys][0]
        # no_tests = res_toric[p_phys][1]
        # p_log = no_success/no_tests
        # size_error_bar = scipy.stats.norm.ppf(q = 1-(1-confidence)/2) * math.sqrt(p_log * (1 - p_log) / res.no_test)
        # k = np.arange(0, 15000, 300)
        # y1 = 1 - (1 - p_log - size_error_bar)**(k/2)
        # y2 = 1 - (1 - p_log + size_error_bar)**(k/2)

        # plt.fill_between(k, y1, y2)

    #### Legend
    fontsize = 20
    plt.yscale('log')
    plt.ylabel('Block error rate', fontsize=fontsize)
    plt.xlabel('number logical qubits', fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.plot([0], [0], color = "black", label = 'Copies of toric codes L = 8')
    legend = plt.legend(prop={'size':fontsize}, frameon = True , loc = 1
    )
    plt.show()




# ###################################
# id_list = id_list_5_6
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2], p_phys = [0.005, 0.01,0.02,0.03]
# )
# confidence = 0.99
# def func(x, a, b):
#     return a * np.exp(-0.00001 * b * (x))
# log_plot2(res_list, confidence, 15000, func,n_not_to_fit = [])
# ###################################

# DO THIS FOR TORIC COMPARISON
###################################
# id_list = swac_5_6
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2], p_phys = [0.005, 0.01,0.015, 0.02])
# confidence = 0.99
# def func(x, a, b):
#     return a * np.exp(-0.00001 * b * np.sqrt(x))
# log_plot2(res_list, confidence, 3800, func,plot_toric = True, n_not_to_fit = [60,120,180])
###################################

# ###################################
# id_list = swac_5_10
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2], p_phys = [0.005, 0.01,0.015, 0.02]
# )
# confidence = 0.99
# def func(x, a, b):
#     return a * np.exp(-0.00001 * b * np.sqrt(x))
# log_plot2(res_list, confidence, 25000, func,plot_toric = False, n_not_to_fit = [])
# ###################################


# no_logicals_list = [1600,3600,6400,10000,14400]

# p_log_toric_list = []




# x_list = [1600,3600,6400,10000,14400]
# y1_list = [0.07688,0.1647,0.273,0.3934,0.5132]
# y2_list = [0.752,0.45,0.18,0.105,0.038]
# plt.scatter(x_list,y1_list, label = "toric, L = 11", marker="X", s = 60)
# plt.scatter(x_list,y2_list, label = "HPG 5,6", marker="D", s = 60)
# plt.ylabel("$p_{log$}")
# plt.xlabel("number of logical qubits")
# plt.legend(prop={'size':12})
# plt.show()
# #############################################################


############################################################################
############################################################################
############################################################################
############################### Average plot ###############################
############################################################################
############################################################################
############################################################################

#################################################################################################
# The function log_plot plots p_phys in absica and p_log in oridinate with log scale for ordinate and with error bar
#################################################################################################
import scipy.stats
plt.style.use('seaborn-whitegrid')

# One curve represents one code, p_log in ordinate and p_phys in absica
class Curve_average:
    def __init__(self,curve_list):

        label_list = ['algo','nv','nc','dv','dc']
        self.label_dict = dict()
        self.label = ''
        for l in label_list:
            for curve in curve_list:
                if curve.label_dict[l] != curve_list[0].label_dict[l]:
                    raise NameError('code labels is not consistent in Curve_average')
            self.label_dict[l] = curve_list[0].label_dict[l]

        self.label = 'algo = ' + str(curve_list[0].label_dict["algo"]) + \
        ', n = '  + str(curve_list[0].label_dict["nv"]) + \
        ', m = '  + str(curve_list[0].label_dict["nc"]) + \
        ', dv = '  + str(curve_list[0].label_dict["dv"]) + \
        ', dc = '  + str(curve_list[0].label_dict["dc"])


        self.p_phys_list = list({p for p in curve.p_phys_list for curve in curve_list})
        self.p_log_list = []
        self.standard_error_list = []
        for p_phys in self.p_phys_list:
            standard_error = 0
            p_log = 0
            no_codes = 0
            for curve in curve_list:
                if p_phys in curve.p_phys_list:
                    index = curve.p_phys_list.index(p_phys)
                    p_log = p_log + curve.p_log_list[index]
                    standard_error = standard_error + curve.standard_error_list[index]**2
                    no_codes = no_codes + 1
                else:
                    print(p_phys, " not for ", curve.label_dict["code_id"])
            self.p_log_list.append(p_log/no_codes)
            self.standard_error_list.append(math.sqrt(standard_error)/no_codes)




    def __lt__(self, other):
        label_list = ['algo','nv','nc','dv','dc']
        for l in label_list:
            if self.label_dict[l] < other.label_dict[l]:
                return True
            elif self.label_dict[l] > other.label_dict[l]:
                return False
        return True




def log_plot_average(res_list, block_success_rate = False):
    curve_dict = dict()
    for res in res_list:
        if not(res.code_id in curve_dict.keys()):
            curve_dict[res.code_id] = Curve(res)
        curve_dict[res.code_id].add(res, block_success_rate)

    curve_list = [curve_dict[code_id] for code_id in curve_dict.keys()]
    curve_average_list = []

    while curve_list != []:
        curve0 = curve_list[0]
        curve_to_average_list = [curve for curve in curve_list if curve0.same_parameter(curve)]
        curve_list = [curve for curve in curve_list if not curve0.same_parameter(curve)]
        curve_average_list.append(Curve_average(curve_to_average_list))

    curve_average_list.sort()

    #mark = ["X","D","P","*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    mark = ["*","h","<",">","v","s","o","^","8","p","H","+","x","d","|",",","_",".","1","3","4","2"]
    i_mark = 0
    for curve in curve_average_list:
        marker=mark[i_mark]
        i_mark = (i_mark+1) % len(mark)
        yerr = curve.standard_error_list
        plt.errorbar(curve.p_phys_list, curve.p_log_list, yerr = yerr , label = curve.label, marker=marker, ms = 10, ls = 'None', capthick=1, capsize=5, elinewidth=1)

    #### Legend
    fontsize = 30
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.yscale('log')
    if block_success_rate:
        plt.ylabel('Block success rate',fontsize=fontsize)
    else:
        plt.ylabel('Block error rate',fontsize=fontsize)
    plt.xlabel('Physical error rate',fontsize=fontsize)
    legend = plt.legend(prop={'size':15}, frameon = True)
    plt.show()


########################################
swac_average_4_5_50_40 = ["swac_74wo5ovt", "swac_79a6p7dg", "swac_7nrpbbr1", "swac_8go3cani", "swac_fpngqw6p", "swac_hpj2e4yw", "swac_p89m86v1", "swac_r9ozxmw0", "swac_vtrjhqxb", "swac_zfsa6euz"]
swac_average_4_5_100_80 = ["swac_2gpcbodq", "swac_2r4ryq14", "swac_4a9qgewa", "swac_eaadh38x", "swac_ijxak3l6", "swac_lyq2xz9f", "swac_nwxpon0j", "swac_t6md1leb", "swac_ufvducdz", "swac_vp6jg8gh"]
swac_average_4_5_150_120 = ["swac_2nqseroy", "swac_6u8nwfkl", "swac_8jqa7eoy", "swac_8k5kw1lk", "swac_8otv731x", "swac_b1zn3k3r", "swac_bvb6p3ze", "swac_dalf6yy4", "swac_i23x3bxn", "swac_q6tapzf2"]
swac_average_4_5_200_160 = ["swac_1af3mkmr", "swac_7cwl7ljn", "swac_9mvu8r9v", "swac_bw3hdf70", "swac_fxadv5u8", "swac_ishri574", "swac_jqam01n3", "swac_nf7jp30s", "swac_qjl6l7is", "swac_zcfyv65i"]
swac_average_4_5_250_200 = ["swac_4i4xzzd4", "swac_8ujqs84s", "swac_cksk77jy", "swac_d2i5sfdr", "swac_d6l8scwu", "swac_m6vanc5b", "swac_odnw50qn", "swac_q4akt8vh", "swac_tilfswc3", "swac_zqcmvfus"]
swac_average_4_5_300_240 = ["swac_3skk5e38", "swac_aagwiw90", "swac_g4ke89zm", "swac_qxekryuz", "swac_t96hsp5x", "swac_tql3muwd", "swac_vbptqblf", "swac_yeah56jb", "swac_yg5w33i9", "swac_zh4wfzts"]
########################################



# #############
# # Modify here
# # USE QUOTES !
# id_list = swac_average_4_5_50_40 + swac_average_4_5_100_80 + swac_average_4_5_150_120 + swac_average_4_5_200_160 + swac_average_4_5_250_200 + swac_average_4_5_300_240
# res_list = file_to_res_list(args.i, dv=[], dc = [], code_id = id_list, nv = [], algo = [2],p_phys = [])
# log_plot_average(res_list, block_success_rate = False)
# #fixed_param_list = ['nv','nc','dv','dc']
# ########################################
