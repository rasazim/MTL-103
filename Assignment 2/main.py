import numpy as np
from fractions import Fraction as fr

def dual_simplex(A,B):
    m,n = A.size()
    while true:
        p_r=1
        p_c=1
        while A[p_r,0]>0:
            p_r=p_r+1
            if(p_r>=n):
                break
        if p_r>=n:
            break
        