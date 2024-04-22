num_list = [1, 2, 3, 4, 1, 3, 5, 6, 4]
unique_list = []
for num in num_list:
    if num not in unique_list:
        unique_list.append(num)
print("Original list:", num_list)
print("List after removing duplicates:", unique_list)