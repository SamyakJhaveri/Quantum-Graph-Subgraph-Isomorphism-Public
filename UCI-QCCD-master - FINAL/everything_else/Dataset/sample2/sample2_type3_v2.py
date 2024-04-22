num_list = [2, 3, 4, 6, 7, 8]
prod = 1
for num in num_list:
    if num % 2 == 0:
        prod *= num
print("Product of even numbers in the list:", prod)