#!/usr/bin/python
# USAGE: 
# python globalAlign.py <string1> <string2> <match_val> <mismatch_val> <indel_val>

import math
import random
import sys

upper = []
lower = []
G = [[]]

def align(a, b, match, mismatch, indel):
    global upper
    global lower
    global G
    opt_align = set([])
    dnaString = a #rand_string(10)#sys.argv[1]
    dnaString2 = b #rand_string(10)#sys.argv[2]
    n = len(dnaString) + 1
    m = len(dnaString2) + 1
    score = [[0 for x in range(len(dnaString2) + 1)] for x in 
                                                range(len(dnaString)+1)] 
    for i in range(len(dnaString2)+1):
        if (i == 0):
            score[i][0] = 0
#            print "Score 0,0: ", score[0][0]
        else:
#            print i
            G.append([(0,i), (0, i-1), a[i-1], "-"])
            score[0][i] = -i
#            print "Score First Row = ", score[0][i]
    for i in range(len(dnaString) + 1):
        if (i == 0):
            pass #print "Score 0,0: ", score[0][0]
        else:
            G.append([(i,0), (i-1, 0), "-", b[i-1]])
            score[i][0] = -i
#            print "Score First Col = ", score[i][0]
    first = 0
    second = 0
    for i in range(len(dnaString2)+1):
        print i
        if (i != 0):
            for j in range(len(dnaString)+1):
                if (j != 0):
                    r1 = score[i-1][j-1] + mismatch
                    if dnaString2[i-1] in dnaString[j-1]:
                        r1 = score[i-1][j-1] + match
                    r2 = score[i-1][j] + indel
                    r3 = score[i][j-1] + indel
#                    print i, j
                    score[i][j] = max(r1, r2, r3)
                    if score[i][j] == r1:
#                        print a[j-1], b[i-1]
                        G.append([(i,j),(i-1,j-1), a[j-1],b[i-1]])
                    elif score[i][j] == r2:
#                        print "a", b[j-1]
                        G.append([(i,j),(i-1,j), "-",b[i-1]])
                    else:
#                        print a[i-1]
                        G.append([(i,j),(i,j-1), a[j-1],"-"])

    print "Optimal Alignment Score = ", score[len(dnaString2)-1][len(dnaString)-1]

def get_array(x):
    global G
    global upper
    global lower
    first = []
#    print G
    first = G[x-1]
#    print len(G)
    last = G[len(G)-1]
#    print last
    for i in reversed(G):
        print "FIRST",i
        if not i:
            break
        if i[0] == last[1]:
#            print "HELLO"
            upper.append(last[2])
            lower.append(last[3])
            last = i
            print "LAST" ,last
            
#    upper.append(first[2])
#    lower.append(first[3])
    upper.append(last[2])
    lower.append(last[3])

        
        

match = int(sys.argv[1])
mismatch = int(sys.argv[2])
indel = int(sys.argv[3])

a = []
b = []

with open("a_1.txt") as f:
    while True:
        c = f.read(1)
        if not c:
            print "End of file"
            break
        if c not in '\n':
            a.append(c)

with open("b_1.txt") as f:
    while True:
        c = f.read(1)
        if not c:
            print "End of file"
            break
        if c not in '\n':
            b.append(c)
print a
print b
    
#a = ['A', 'C','G','G','T']
#b = ['T','A','A','G','T']

align(a, b, match, mismatch, indel)
get_array((len(a))*(len(b)))
u2 = []
l2 = []
for i in reversed(upper):
    u2.append(i)
print u2
for i in reversed(lower):
    l2.append(i)
print l2


