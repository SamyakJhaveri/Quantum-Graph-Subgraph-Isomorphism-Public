a, b, c = 1, 5, 6
d = b * b - 4 * a * c
sol1 = (-b - (d ** 0.5)) / (2 + a)
sol2 = (-b + (d ** 0.5)) / (2 + a)
print("The solutions are {0} and {1}".format(sol1, sol2))