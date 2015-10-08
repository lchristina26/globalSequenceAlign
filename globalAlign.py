#!/usr/bin/python
# USAGE: 
# python globalAlign.py <string1> <string2> <match_val> <mismatch_val> <indel_val>

import math
import igraph
import random
import sys

upper = []
bottom = []
G = igraph.Graph()#[[]] 

def rand_string(length):
    sequence = []
    alphabet = ['a','c','g','t']
    for i in range(length):
        sequence.append(random.choice(alphabet))
    return sequence

def align(a, b, match, mismatch, indel):
    global G
    opt_align = set([])
    dnaString = a #rand_string(10)#sys.argv[1]
    dnaString2 = b #rand_string(10)#sys.argv[2]
    n = len(dnaString) + 1
    m = len(dnaString2) + 1
    score = [[0 for x in range(len(dnaString2) + 1)] for x in 
                                                range(len(dnaString)+1)] 
    for i in range(len(dnaString2) + 1):
        if (i == 0):
            score[i][0] = 0
#            print "Score 0,0: ", score[0][0]
        else:
            score[0][i] = -i
#            print "Score First Row = ", score[0][i]
    for i in range(len(dnaString) + 1):
        if (i == 0):
            pass #print "Score 0,0: ", score[0][0]
        else:
            score[i][0] = -i
#            print "Score First Col = ", score[i][0]
    G.add_vertices((n)*(m) + 1)
    for i in range(len(dnaString2)+1):
        print "IN LOOP ", i
#        if (i != 0):
        for j in range(len(dnaString)+1):
#         print "IN LOOP ", i,j
            home = j*n+i+1
            diag = (j-1)*n+i
            left = j*n + i
            top = (j-1)*n + i + 1
            r1 = score[i-1][j-1] + mismatch
            if dnaString2[i-1] in dnaString[j-1]:
                r1 = score[i-1][j-1] + match
            r2 = score[i-1][j] + indel
            r3 = score[i][j-1] + indel
            if j == 0 and i != 0:
                G.add_edges([(home, i)])
            if i == 0 and j != 0:
                G.add_edges([(home, top)])
            if (j != 0 and i != 0):
                if r1 == r2 and r2 == r3:
                    G.add_edges([(home, diag)]) #((i-1,j-1),(i,j))
                    G.add_edges([(home, left)])#((i-1, j), (i,j))
                    G.add_edges([(home, top)])  #((i,j-1), (i,j))
                    score[i][j] = r1
                elif r1 == r2 and r2 > r3:
                    G.add_edges([(home, diag)])    #(j-1,i-1), (i,j))
                    G.add_edges([(home, left)])   #((i-1, j), (i,j))
                    score[i][j] = r1
                elif r1 > r2 and r1 > r3:
                    G.add_edges([(home, diag)])    #(i-1,j-1))
                    score[i][j] = r1
                elif r3 > r2 and r3 > r1:
                    G.add_edges([(home, top)])   #(i, j-1), (i,j))
                    score[i][j] = r3
                elif r3 == r2 and r3 > r1:
                    G.add_edges([(home, top)])   #(i, j-1), (i,j))
                    G.add_edges([(home, left)])   #(i-1, j), (i,j))
                    score[i][j] = r3
                elif r2 > r1 and r2 > r3:
                    G.add_edges([(home, left)])   #(i-1,j), (i,j))
                    score[i][j] = r2
    print "Optimal Alignment Score = ", score[len(dnaString2)][len(dnaString)]
#    print score
#    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
#                      for row in score]))
def find_paths(graph, start, end, a, b):
    global upper
    global bottom
    paths = [[]]
    path = []
    n = len(a)
    paths =  graph.get_shortest_paths(start, end)#get_all_shortest_paths(start, end)
    for i in paths:
        path = i
    print "PATH + ", path
    for k in range(len(path)):
        if k != (len(path)-1):
            if path[k+1] == path[k] + n+2:
                if ((path[k+1]%(n+1)) == 0):
                    upper.append(a[k/(n+1)-1])
                    bottom.append(b[path[k+1]/(n+1) - 2])
                else:
                    upper.append(a[path[k+1]/(n+1)-1])
                    bottom.append(b[path[k+1]%(n+1) - 2])
            elif path[k+1] == path[k] + n + 1:
                upper.append(a[(k%n)])
                bottom.append("-")
            else:
                upper.append("-")
                bottom.append(b[k%n-1]);

match = int(sys.argv[1])
mismatch = int(sys.argv[2])
indel = int(sys.argv[3])
a = []
b = []
#a = ['H', 'A','P','P','E']
#b = ['A','P','P','L','E']
with open("a_sequences.txt", "rtU") as f:
  for line in f:
      for ch in line:
        a.append(ch)

with open("b_sequences.txt", "rtU") as f:
  for line in f:
      for ch in line:
        b.append(ch)
#a = rand_string(1000)#['H','A','P','G','X','E']#rand_string(10)
#print a
#b = rand_string(10)#['A','P','P','G','X','E']#rand_string(10)
print "Sequences to Align:"
print ' '.join(map(str, a))
print  ' '.join(map(str, b))
align(a, b, match, mismatch, indel)
#print G.get_all_shortest_paths(36, 1)
find_paths(G, 1, (len(a)+1)*(len(b)+1), a, b)
print "FINAL ALIGNMENT:"
#print upper
#print bottom
print ' '.join(map(str, upper))
print ' '.join(map(str, bottom))
#find_all_paths(G, 0, len(a))
