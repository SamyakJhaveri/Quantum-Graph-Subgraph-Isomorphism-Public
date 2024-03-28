n = 13
prime = True
for i in range(2, int(n/2)+1):
    if n % i == 0:
        prime = False
        break
if prime:
    print(n, "is a prime number")
else:
    print(n, "is not a prime number")
