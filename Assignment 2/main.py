import numpy as np
from decimal import *
from decimal import Decimal as dc

def dual_simplex(A,B):
    m,n = A.shape
    m-=1
    n-=1
    status = True
    while True:
        p_r=-1
        p_c=-1
        for i in range(0,m):
            if(A[i+1,0]<0):
                if(p_r==-1):
                    p_r = i+1
                elif(B[p_r-1]>B[i]):
                    p_r = i+1
        if(p_r==-1):
            break
        for i in range(0,n):
            min=-1
            if(A[p_r,i+1]<0):
                if(min==-1 or -A[0,i+1]/A[p_r,i+1]<min):
                    min = -A[0,i+1]/A[p_r,i+1]
                    p_c = i+1
        if(p_c==-1):
            status = False
            break
        B[p_r-1] = p_c
        A[p_r] = A[p_r] / A[p_r,p_c]
        A[p_r,p_c]=dc(0)
        A = A - np.matmul(np.array([A[:,p_c]],dtype=dc).T,np.array([A[p_r]],dtype=dc))
        A[:,p_c] = dc(1) * np.zeros(m+1,dtype=dc)
        A[p_r,p_c]=dc(1)
    return (A,B,status)

A = np.array([list(map(dc,[-3,1,0,0,0,0])),list(map(dc,[1,1,1,0,0,0])),list(map(dc,[-1,-1,0,1,0,-1])),list(map(dc,[1,0,0,0,1,1]))])
B = [2,3,4]
print(A)
print(B)

A,B,stat = dual_simplex(A,B)
print(A)
print(B)