import os, sys, csv
import pandas as pd

root_path = os.path.split(os.getcwd())[0]
dataset_folder_path = os.path.join(root_path, "Dataset")

codes = []
names = []
for i in range(4, 10, 1):
    filename = ""
    sample_folder_path = os.path.join(dataset_folder_path, "sample" + str(i))
    print("sample_folder_path: {}".format(sample_folder_path))
    for j in range(1, 4, 1):
        for k in range(1, 6, 1):
            filename = "sample" + str(i) + "_type" + str(j) + "_v" + str(k) + ".py"
            file_path = os.path.join(sample_folder_path, filename)
            if os.path.exists(file_path):
                print("file_path:{}".format(file_path))
                with open(file_path) as fin:
                    srccode = fin.read()
                codes.append(srccode)
                names.append(filename)

print("Codes:\n", codes)
print("Names:\n", names)
print("Len(names):\n", len(names))

output_folder_path = os.path.join(root_path, "programs")

output_file_path = os.path.join(output_folder_path, "programs_sample4_9.csv")
print("output_file_path: {}".format(output_file_path))

with open(output_file_path, "w", newline="") as output_file:
    csvwriter = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
    for name, code in zip(names, codes):
        csvwriter.writerow([name, code])
