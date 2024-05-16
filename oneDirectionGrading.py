#!/usr/bin/env python3
"""
File: oneDirectionGrading.py
Author: G. Vijaya Kumar
Date: 16th May 2024
Description: Geometric grading at one end of an edge for blockMesh
"""
import numpy as np

l = float(input("Enter the edge length: "))

# ratio of consecutive cells
r = float(input("Enter growth ratio (typically 1.1 or 1.2): "))

# first-cell height
a = float(input("Enter first cell height: "))

# maximum cell size in the edge
max_size = float(input("Enter the max cell size: "))

expansion_ratio = max_size/a

n = np.log(expansion_ratio)/np.log(r) + 1
n = int(round(n))

max_actual = a*pow(r,n-1)
max_actual = round(max_actual,4)

expansion_ratio = round(max_actual/a,4)

sum_n = a*(pow(r,n)-1)/(r-1)
sum_n = round(sum_n,4)

rem_length = l-sum_n
rem_length = round(rem_length,4)

norm_sum_n = int(sum_n*100/l)
norm_rem_length = 100-norm_sum_n

n_uniform = rem_length/max_actual

n_uniform = int(round(n_uniform))

print("First cell height = " + str(a))
print("stretching ratio = " + str(r))
print("specified max = "+str(max_size))
print("actual max = "+str(max_actual))
print("\nTotal cells = " + str(n+n_uniform))
print("\nGrading Forward")
print("("+str(norm_sum_n)+"\t"+str(n)+"\t"+str(expansion_ratio)+")")
print("("+str(norm_rem_length)+"\t"+str(n_uniform)+"\t"+str(1)+")")
print("\nIf Grading is Reverse, please use")
print("("+str(norm_rem_length)+"\t"+str(n_uniform)+"\t"+str(1)+")")
print("("+str(norm_sum_n)+"\t"+str(n)+"\t"+str(1.0/expansion_ratio)+")")
