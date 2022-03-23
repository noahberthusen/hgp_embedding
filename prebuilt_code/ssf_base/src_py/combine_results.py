from read_result import create_summary_file
import default_names
import argparse
import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', default = glob.glob(default_names.res_dir + '/*.res'), nargs = '+', help = "the files we want to merge. e.g -i results/*.res")
    parser.add_argument('-o', default = default_names.summary_res_file, help = "file where we store the merge of files")
    args = parser.parse_args()


create_summary_file(args.i, args.o)
# create_summary_file(args.d, args.o, result_extension = args.e)
