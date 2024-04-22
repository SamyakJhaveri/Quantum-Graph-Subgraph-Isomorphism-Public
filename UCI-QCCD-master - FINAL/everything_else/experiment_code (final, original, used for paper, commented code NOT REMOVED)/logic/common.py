import os
import random


def construct_output_file(original_file_path, output_path, clone_type):
    newfilename = os.path.basename(original_file_path)  # `test_Me1.py`
    newfilename = os.path.splitext(newfilename)[0]
    new_file_path = os.path.join(
        output_path, newfilename + "_type" + str(clone_type) + "_clone"
    )
    newdir = os.path.dirname(new_file_path)
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    print("new_file_path:{}".format(new_file_path))
    return new_file_path
