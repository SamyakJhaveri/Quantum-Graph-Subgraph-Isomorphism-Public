n_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
s = 0
for n in n_list:
    if n % 2 == 0:
        s += n
print("Sum of even numbers in the list:", s)