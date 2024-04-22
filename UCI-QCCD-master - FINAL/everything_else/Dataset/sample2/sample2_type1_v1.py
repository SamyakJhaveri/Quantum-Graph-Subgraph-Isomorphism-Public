num_list = [2, 3, 4, 6, 7, 8]
sum = 0
for num in num_list:
    if num % 2 == 0:
        sum += num
print("Sum of even numbers in the list:", sum)