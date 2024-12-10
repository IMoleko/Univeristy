# Import necessary libraries
import math
import random

# Demonstrate math.floor - returns the largest integer less than or equal to a given number
num1 = 7.8
print("math.floor({}) = {}".format(num1, math.floor(num1)))

# Demonstrate math.ceil - returns the smallest integer greater than or equal to a given number
num2 = 5.2
print("math.ceil({}) = {}".format(num2, math.ceil(num2)))

# Demonstrate max - returns the largest of its arguments
a, b, c = 12, 7, 15
print("max({}, {}, {}) = {}".format(a, b, c, max(a, b, c)))

# Demonstrate min - returns the smallest of its arguments
print("min({}, {}, {}) = {}".format(a, b, c, min(a, b, c)))

# Demonstrate random.randint - returns a random integer between given range
rand_int = random.randint(1, 10)
print("random.randint(1, 10) = {}".format(rand_int))

# Demonstrate random.random - returns a random float between 0 and 1
rand_float = random.random()
print("random.random() = {}".format(rand_float))

# Demonstrate random.shuffle - shuffles elements in a list in-place
sample_list = [1, 2, 3, 4, 5]
random.shuffle(sample_list)
print("random.shuffle([1, 2, 3, 4, 5]) = {}".format(sample_list))

# Demonstrate round - rounds a number to a given precision (default 0 decimal places)
num3 = 5.67
print("round({}, 1) = {}".format(num3, round(num3, 1)))

# Demonstrate math.sqrt - returns the square root of a given number
num4 = 16
print("math.sqrt({}) = {}".format(num4, math.sqrt(num4)))
