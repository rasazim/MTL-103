import numpy as np
from fractions import Fraction as fr

obj=""
n=0
m=0

with open("input.txt","r") as f:
    inp = f.read()

inp=inp.split('\n')
obj = inp[1]
print(obj)
i = 4
A=[]
while True:
    row = inp[i]
    if(row==''):
        break
    i=i+1
    row = list(map(int,row.split(', ')))
    m=m+1
    A.append(row)
n=len(A[0])
# print(A,m,n)

i=i+2
b=[]
while True:
    bi = inp[i]
    if(bi==''):
        break
    i=i+1
    b.append(int(bi))
b= np.array([b]).T
print(b)

i=i+2
j=0
while True:
    con = inp[i]
    if(con==''):
        break
    if(con=='<='):
        for l in A:
            l.append(0)
        A[j][n]=1
        n=n+1
    if(con=='>='):
        for l in A:
            l.append(0)
        A[j][n]=-1
        n=n+1
    i=i+1
    j=j+1
    # print(con)

i=i+2
c = list(map(int,inp[i].split(', ')))
while len(c)<n:
    c.append(0)
c = np.array([c]).T

    
print(c)

A = np.array(A)
print(A)

for i in range(m):
    if(b[i]<0):
        b[i]=-b[i]
        A[i]=-A[i]

A=np.c_[A,np.identity(m,dtype=fr)]
x = np.r_[np.zeros((n,1),dtype=fr),b]
B = list(range(n,n+m))
cd = np.c_[np.zeros((1,n),dtype=fr),np.ones((1,m),dtype=fr)]
ch = cd - np.matmul(np.ones((1,m),dtype=fr), A)
M = np.r_[np.c_[0,ch],np.c_[b,A]]
print(M)


