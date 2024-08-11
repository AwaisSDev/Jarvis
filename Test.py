# Project Description: Prints Factorial of 10
# Write code only

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(10))