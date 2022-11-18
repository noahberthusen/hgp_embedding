import os

code = "48_40_5_6"
# code = "60_50_5_6"

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
data_path = os.path.join(path, "./data")

cluster_filenames = []
error_filenames = []
for file in os.listdir(data_path):
    if "cluster" in file:
        cluster_filenames.append(os.path.join(data_path, file))
    elif "error" in file:
        error_filenames.append(os.path.join(data_path, file))
        
with open(os.path.join(path, f"./data/{code}_error_size.res"), "w") as outfile:
    for fname in error_filenames:
        with open(fname) as infile:
            for line in infile.readlines()[:-1]:
                outfile.write(line)

with open(os.path.join(path, f"./data/{code}_cluster_size.res"), "w") as outfile:
    for fname in cluster_filenames:
        with open(fname) as infile:
            for line in infile.readlines()[:-1]:
                outfile.write(line)