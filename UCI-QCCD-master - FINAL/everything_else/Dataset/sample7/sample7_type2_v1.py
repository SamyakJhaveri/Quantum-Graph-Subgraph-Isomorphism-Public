l = 100
u = 2000
for num in range(l, u + 1):
    order = len(str(num))
    s = 0
    temp = num
    while temp > 0:
        d = temp % 10
        s += d ** order
        temp //= 10
    if num == s:
        print(num)