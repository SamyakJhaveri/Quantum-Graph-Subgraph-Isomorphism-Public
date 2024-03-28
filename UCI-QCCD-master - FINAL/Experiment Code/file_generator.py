import os, sys, csv
import pandas as pd
root_path = os.path.split(os.getcwd())[0] # "/home/samyaknj/Research/UCI Quantum Code Clone Detection Project/"
# print("root_path:{}".format(root_path))
dataset_folder_path = os.path.join(root_path, 'Dataset')
# print("dataset_folder_path:{}".format(dataset_folder_path))

codes = []
names = []
for i in range(4, 10, 1):
    filename = "" 
    sample_folder_path = os.path.join(dataset_folder_path, 'sample' + str(i))
    print('sample_folder_path: {}'.format(sample_folder_path))
    for j in range(1, 4, 1):
        for k in range(1, 6, 1):
            filename = "sample" + str(i) + "_type"+ str(j) + "_v" + str(k) + ".py"
            file_path = os.path.join(sample_folder_path, filename)
            if os.path.exists(file_path):
                print("file_path:{}".format(file_path))
                with open(file_path) as fin :
                    srccode = fin.read()
                codes.append(srccode)
                names.append(filename)
print(codes)
print(names)
# codes_smaller = codes[1:3] # [codes[0], codes[2], codes[4], codes[7]]  
# names_smaller = names[1:3] # [names[0], names[2], names[4], names[7]] 
# print(codes_smaller)
# print(names_smaller)
print(len(names))

output_folder_path = os.path.join(root_path, 'programs')

output_file_path = os.path.join(output_folder_path, 'programs_sample4_9.csv')
print("output_file_path: {}".format(output_file_path))

# output_file_path_smaller = os.path.join(output_folder_path, 'two-sample programs')
# output_file_path_smaller = os.path.join(output_file_path_smaller, 'programs_sample1_2.csv')
# print("output_file_path_smaller:{}".format(output_file_path_smaller))

with open(output_file_path, 'w', newline = '') as output_file:
    csvwriter = csv.writer(output_file, quoting = csv.QUOTE_MINIMAL) 
    # for name, code in zip(names, codes):
    #    csvwriter.writerow([name, code])
    for name, code in zip(names, codes):
        csvwriter.writerow([name, code])
    

