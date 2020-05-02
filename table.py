import numpy as np
import re
import string
import math
import preparation

def countTrigrams(text):
    #inicialization, count starts with 2 starting symbols
    table = np.zeros((54,54,54))
    alphabet = preparation.makeAlphabet();
    temp1 = 42
    temp2 = 42
    letter = 0

    #count trigrams
    for a in text:
        if a in alphabet:
            letter = alphabet[a]
        else:
            letter = alphabet[' ']
        table[letter, temp1, temp2]+=1
        temp2 = temp1
        temp1 = letter
    return table




def smoothTable(table):
    result =  np.zeros((54,54,54))
    for j in range(54):
        for k in range(54):
            #performance optimalization v4.0
            d = countThemAll(table,j,k)
            t = d['T']
            z = d['Z']
            n = d['N']
            for i in range(54):
                c = table[i,j,k]
                #t = countT(table, j, k)
                #z = countZ(table, j, k)
                #n = countN(table, j, k)                
                if n == 0:
                        #if a history h has no counts, the MLE distribution PMLE(w | h) is not meaningful and should be ignored. source: http://www.ee.columbia.edu/~stanchen/e6884/labs/lab3/x207.html
                        # 1 will transform to 0 after logarithm conversion
                        p = 1
                elif c == 0:
                    p = t/(z*n+t)                  
                else:
                    p = c/(n+t)
                result[i,j,k] = p                
    return result

# count of triplets that appeared in the data
def countThemAll(table,temp1,temp2):
    countT = 0
    countZ = 0
    countN = 0
    d = dict()
    for i in range(54):
        countN += table[i,temp1,temp2]
        if table[i,temp1,temp2] != 0:
            countT += 1
        if table[i,temp1,temp2] == 0:
            countZ += 1
    d['T'] = countT
    d['Z'] = countZ
    d['N'] = countN
    return d

# count of triplets that appeared in the data
def countT(table,temp1,temp2):
    count = 0
    for i in range(54):
        for j in range(54):
            for k in range(54):
                if j == temp1:
                    if k == temp2:
                        if table[i,j,k] != 0:
                            count += 1
    return count

# count of triplets that didn't appear in the data
def countZ(table,temp1,temp2):
    count = 0
    for i in range(43):
        for j in range(43):
            for k in range(43):
                if j == temp1:
                    if k == temp2:
                        if table[i,j,k] == 0:
                            count += 1
    return count

# number of words that appeared in the text with specified predecessors
def countN(table,temp1,temp2):
    count = 0
    for i in range(43):
        for j in range(43):
            for k in range(43):
                if j == temp1:
                    if k == temp2:
                        count += table[i,j,k]
    return count


   
def calculateLM(text, table):
    result = 0
    temp1 = 42
    temp2 = 42
    letter = 0
    alphabet = preparation.makeAlphabet();

    for a in text:
        if a in alphabet:
            letter = alphabet[a]
        else:
            letter = alphabet[' ']       
        result += math.log10(table[letter, temp1, temp2])
        temp2 = temp1
        temp1 = letter
    #return math.pow(10,result)
    return result
