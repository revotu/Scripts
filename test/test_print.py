#from __future__ import print_function
import sys

A = 'A'
B = 'B'
C = 'C'

print A
sys.stdout.write(str(A) + '\n')

print A, B, C
sys.stdout.write(' '.join(map(str, [A, B, C])) + '\n')

print A,
sys.stdout.write(str(A))

f = open('file.txt', 'w')
print >> f, A, B, C,
f.close()
