#1 Code Golf from `Exercises in Programming Style`
import re, string, sys

stops = set(open("../stop_words.txt").read().split(",") + list(string.ascii_lowercase))
words = [x.lower() for x in re.split("[^a-zA-Z]+", open(sys.argv[1]).read()) if len(x) > 0 and x.lower() not in stops]
unique_words = list(set(words))
unique_words.sort(key=lambda x: words.count(x), reverse=True)
print("\n".join(["%s - %s" % (x, words.count(x)) for x in unique_words[:25]]))

# ----------
#2 Code Golf from `Exercises in Programming Style`
#!/usr/bin/env python
# My golf score is slightly lower!  
# Best wishes, Peter Norvig
import re, sys, collections

stopwords = set(open('../stop_words.txt').read().split(','))
words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
counts = collections.Counter(w for w in words if w not in stopwords)
for (w, c) in counts.most_common(25):
    print(w, '-', c)

# ----------
#3 Code Golf from `Exercises in Programming Style`
#!/usr/bin/env python
import heapq, re, sys

words = re.findall("[a-z]{2,}", open(sys.argv[1]).read().lower())
for w in heapq.nlargest(25, set(words) - set(open("../stop_words.txt").read().split(",")), words.count):
    print(w, '-', words.count(w))

# ----------
#4 Add Two Numbers
# Store input numbers
num1 = input('Enter first number: ')
num2 = input('Enter second number: ')

# Add two numbers
sum = float(num1) + float(num2)

# Display the sum
print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))

# ----------
#5 Find square root of real or complex numbers
# Importing the complex math module
import cmath

num = 1+2j

# To take input from the user
#num = eval(input('Enter a number: '))

num_sqrt = cmath.sqrt(num)
print('The square root of {0} is {1:0.3f}+{2:0.3f}j'.format(num ,num_sqrt.real,num_sqrt.imag))

# ----------
#6 Python Program to find the area of triangle

a = 5
b = 6
c = 7

# Uncomment below to take inputs from the user
a = float(input('Enter first side: '))
b = float(input('Enter second side: '))
c = float(input('Enter third side: '))

# calculate the semi-perimeter
s = (a + b + c) / 2

# calculate the area
area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
print('The area of the triangle is %0.2f' %area)

# ----------
#7 Solve the quadratic equation ax**2 + bx + c = 0

# import complex math module
import cmath

a = 1
b = 5
c = 6

# calculate the discriminant
d = (b**2) - (4*a*c)

# find two solutions
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)

print('The solution are {0} and {1}'.format(sol1,sol2))


# ----------
#8 Program to check Armstrong numbers in a certain interval

lower = 100
upper = 2000

for num in range(lower, upper + 1):

   # order of number
   order = len(str(num))
    
   # initialize sum
   sum = 0

   temp = num
   while temp > 0:
       digit = temp % 10
       sum += digit ** order
       temp //= 10

   if num == sum:
       print(num)


# ----------
#9 code from saini's paper
def sequence(start, stop):
   builder = []


   i = start
   
   while (i < stop):
      # check condition first
      if (i > start):
         builder.append(',')
      
      builder.append(i)
      i += 1
   
   return ''.join(builder)
# ----------
#10
# Python program to find the factorial of a number provided by the user.

# change the value for a different result
num = 7

# To take input from the user
#num = int(input("Enter a number: "))

factorial = 1

# check if the number is negative, positive or zero
if num < 0:
   print("Sorry, factorial does not exist for negative numbers")
elif num == 0:
   print("The factorial of 0 is 1")
else:
   for i in range(1,num + 1):
       factorial = factorial*i
   print("The factorial of",num,"is",factorial)

# ----------