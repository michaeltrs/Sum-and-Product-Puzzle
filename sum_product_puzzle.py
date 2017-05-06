# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 21:17:23 2017

@author: michael

Problem:
--------
X and Y are two different whole numbers greater than 1. Their sum is no greater 
than 100, and Y is greater than X. S and P are two mathematicians (and 
consequently perfect logicians); S knows the sum X + Y and P knows the 
product X * Y. Both S and P know all the information in this paragraph.

The following conversation occurs:

step1 - S says "P does not know X and Y."
step2 - P says "Now I know X and Y."
step3 - S says "Now I also know X and Y."

What are X and Y?

"""
from time import time
t0 = time()

import pandas as pd
import itertools

def flatten(l):
    return list(itertools.chain.from_iterable(l))
    
def termpairs(n):
    terms = []
    for i in range(2,n):
        if (((n-i)>1)
            &(all([i not in existingterms for existingterms in terms]))):
            terms.append([i,n-i])
    return terms
    
def factorpairs(n):
    factors = []
    for i in range(2,n):
        if n%i==0:
            if all([i not in existingfactors for existingfactors in factors]):
                factors.append([i,n/i])
    return factors
    
def listfactorpairs_num(l):
    return all([len(factorpairs(i))!=1 for i in l])
    
def listproduct(l):
    return [ i[0]*i[1] for i in l]

print('Making a table of all possible numbers')
numbers = [[[i,j]] for i in range(2,100) for j in range(2,100) 
              if (i+j<=100) & (i<j)]
numbers = pd.DataFrame(numbers, columns=['nums'])

numbers['S'] = numbers['nums'].apply(lambda n:n[0]+n[1])
numbers['P'] = numbers['nums'].apply(lambda n:n[0]*n[1])

numbers['terms'] = numbers['S'].apply(termpairs)

numbers['termsproduct'] = numbers['terms'].apply(listproduct)

numbers['num_termsproductfactors'] = numbers['termsproduct'].apply(listfactorpairs_num)

numbers = numbers[numbers['num_termsproductfactors']]

numbers['Pfreq'] = numbers.groupby('P')['P'].transform('count')

numbers = numbers[numbers['Pfreq']==1]

numbers['Sfreq'] = numbers.groupby('S')['S'].transform('count')

numbers = numbers[numbers['Sfreq']==1]

print(numbers['nums'].values)