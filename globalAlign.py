#!/usr/bin/python
# USAGE: 
# python globalAlign.py <string1> <string2> <match_val> <mismatch_val> <indel_val>

import sys

def align():
    opt_align = set([])
    dnaString = sys.argv[1]
    dnaString2 = sys.argv[2]
    match = int(sys.argv[3])
    mismatch = int(sys.argv[4])
    indel = int(sys.argv[5])
    score = [[0 for x in range(len(dnaString) + 1)] for x in 
                                                range(len(dnaString2)+1)] 
    for i in range(len(dnaString) + 1):
        if (i == 0):
            score[i][0] = 0
            print "Score 0,0: ", score[0][0]
        else:
            score[0][i] = -i
            print "Score First Row = ", score[0][i]
    for i in range(len(dnaString2) + 1):
        if (i == 0):
            print "Score 0,0: ", score[0][0]
        else:
            score[i][0] = -i
            print "Score First Col = ", score[i][0]
    
    for i in range(len(dnaString2)+1):
        if (i != 0):
            for j in range(len(dnaString)+1):
                if (j != 0):
                    if dnaString2[i-1] in dnaString[j-1]:
                        score[i][j] = max(score[i-1][j-1]+match, score[i-1][j] + 
                                          mismatch, score[i][j-1] + indel); 
                    else:
                        score[i][j] = max(score[i-1][j-1], score[i-1][j] + 
                                          mismatch, score[i][j-1] + indel);
    print "Optimal Alignment Score = ", score[len(dnaString2)][len(dnaString)]
    print score


align()
