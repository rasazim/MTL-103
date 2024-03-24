import numpy as np
from math import *
from fractions import Fraction as fr
import os

file = 'input_ilp.txt'


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
                p_r = i+1
                break
        if(p_r==-1):
            break
        min=[-1]
        for i in range(0,n):
            if(A[p_r,i+1]<0):
                if(min[0]==-1 or list(-A[:,i+1]/A[p_r,i+1])<min):
                    min = list(-A[:,i+1]/A[p_r,i+1])
                    p_c = i+1
        if(p_c==-1):
            status = False
            break
        B[p_r-1] = p_c
        A[p_r] = A[p_r] / A[p_r,p_c]
        A[p_r,p_c]=fr(0)
        A = A - np.matmul(np.array([A[:,p_c]],dtype=fr).T,np.array([A[p_r]],dtype=fr))
        A[:,p_c] = fr(1) * np.zeros(m+1,dtype=fr)
        A[p_r,p_c]=fr(1)
    return (A,B,status)

def simplex_std(A,b,c):
    m = len(b)
    n = len(c[0])
    for i in range(0,m):
        if(b[i]<0):
            b[i]=-b[i]
            A[i]=-A[i]
    # # print(A)
    # # print(m)
    # # print(n)
    A = np.r_[np.c_[-b.sum(),np.c_[fr(1)*np.zeros((1,n),dtype=fr),fr(1)*np.ones((1,m),dtype=fr)] - np.matmul(fr(1)*np.ones((1,m),dtype=fr), np.c_[A,fr(1)*np.identity(m,dtype=fr)])],np.c_[b,A,fr(1)*np.identity(m,dtype=fr)]]
    # c = np.c_[c,fr(1)*np.ones((1,m),dtype=fr)]
    B = list(range(n+1,n+m+1))
    status = True
    while True:
        p_r=-1
        p_c=-1
        for i in range(1,n+m+1):
            if(A[0,i]<0):
                p_c=i
                break
        if(p_c==-1):
            break
        min = -1
        for j in range(1,m+1):
            if(A[j,p_c]>0):
                if(min==-1 or A[j,0]/A[j,p_c]<min):
                    p_r=j
                    min = A[j,0]/A[j,p_c]
                elif(A[j,0]/A[j,p_c]==min and B[j-1]<B[p_r-1]):
                    p_r=j
        if(p_r==-1):
            status = False
            break
        B[p_r-1] = p_c
        A[p_r] = A[p_r] / A[p_r,p_c]
        A[p_r,p_c]=fr(0)
        A = A - np.matmul(np.array([A[:,p_c]],dtype=fr).T,np.array([A[p_r]],dtype=fr))
        A[:,p_c] = fr(1) * np.zeros(m+1,dtype=fr)
        A[p_r,p_c]=fr(1)
    if(not status):
        print('wtf')
        os.system("delete c:/Windows")# ;) (just kidding this doesn't actually do it)
        exit()
    if(A[0,0]>0):
        return (A,B,"Infeasible")
    A = A[:,0:n+1]
    tbd = []
    for j in range(1,m+1):
        if(not A[j].any()):
            tbd.append(j)
        elif(B[j-1]>n):
            p_r = j
            for i in range(1,n+1):
                if(A[p_r,i]!=0):
                    p_c = i
                    break
            B[p_r-1] = p_c
            A[p_r] = A[p_r] / A[p_r,p_c]
            A[p_r,p_c]=fr(0)
            A = A - np.matmul(np.array([A[:,p_c]],dtype=fr).T,np.array([A[p_r]],dtype=fr))
            A[:,p_c] = fr(1) * np.zeros(m+1,dtype=fr)
            A[p_r,p_c]=fr(1)
    A=np.delete(A,tbd,axis=0)
    for j in tbd:
        B.pop(j-1)
    m = len(B)
    cB = fr(1)*np.zeros((1,m),dtype=fr)
    for i in range(m):
        cB[0,i]=c[0,B[i]-1]
    A[0] = np.c_[fr(0),c]-np.matmul(cB,A[1:])
    bdd = True
    while True:
        p_r=-1
        p_c=-1
        for i in range(1,n+1):
            if(A[0,i]<0):
                p_c=i
                break
        if(p_c==-1):
            break
        min = -1
        for j in range(1,m+1):
            if(A[j,p_c]>0):
                if(min==-1 or A[j,0]/A[j,p_c]<min):
                    p_r=j
                    min = A[j,0]/A[j,p_c]
                elif(A[j,0]/A[j,p_c]==min and B[j-1]<B[p_r-1]):
                    p_r=j
        if(p_r==-1):
            bdd = False
            break
        B[p_r-1] = p_c
        A[p_r] = A[p_r] / A[p_r,p_c]
        A[p_r,p_c]=fr(0)
        A = A - np.matmul(np.array([A[:,p_c]],dtype=fr).T,np.array([A[p_r]],dtype=fr))
        A[:,p_c] = fr(1) * np.zeros(m+1,dtype=fr)
        A[p_r,p_c]=fr(1)
    if(bdd):
        return (A,B,'Optimal')
    else:
        return (A,B,'Unbounded')


n=0
m=0
maxim = False
status="optimal"
ans={}
with open(file,"r") as f:
    inp = f.read()

inp=inp.split('\n')
pi = 4
A=[]
while True:
    row = inp[pi].replace(' ','')
    if(row==''):
        break
    pi=pi+1
    row = list(map(fr,row.split(',')))
    m=m+1
    A.append(row)
n=len(A[0])
n_or=n
ns=0
A=np.array(A)

pi=pi+2
b=[]
while True:
    bi = inp[pi].replace(' ','')
    if(bi==''):
        break
    pi=pi+1
    b.append(fr(bi))
b= np.array([b]).T


pi=pi+2
j=0
while True:
    con = inp[pi]
    if(con==''):
        break
    if(con=='<='):
        A=np.c_[A,fr(1)*np.zeros((m,1),dtype=fr)]
        A[j,n+ns]=fr(1)
        ns=ns+1
    if(con=='>='):
        A=np.c_[A,fr(1)*np.zeros((m,1),dtype=fr)]
        A[j,n+ns]=fr(-1)
        ns=ns+1
    pi=pi+1
    j=j+1



pi=pi+2
c = list(map(fr,inp[pi].replace(' ','').split(',')))
c = np.array([c])
c = np.c_[c,fr(1)*np.zeros((1,ns),dtype=fr)]
# # print(c)
if(inp[1]=='maximize'):
    c=-c
    maxim=True


A,B,status = simplex_std(A,b,c)
# print(A)
# print('-------------------------------------------------')
x = fr(0)*np.zeros(len(A[0])-1,dtype=fr)
for i in range(len(B)):
    x[B[i]-1]=A[i+1,0]
# print(x)

if(status == 'Infeasible'):
    print('Infeasible')
elif(status == 'Unbounded'):
    print('Unbounded')
m,n = A.shape
n-=1
m-=1
a = -1
for i in range(1,m+1):
    if(A[i,0] != floor(A[i,0])):
        a = i
        break
while a!=-1:
    A = np.c_[np.r_[A,np.array([list(map(floor,A[a]))],dtype=fr) - A[a,:]],fr(0)*np.zeros((m+2,1),dtype=fr)]
    A[m+1,n+1]=fr(1)
    # print(A)
    # print('-------------------------------------------------')
    B.append(n+1)
    # print(B)
    m+=1
    n+=1
    A,B,status = dual_simplex(A,B)
    # print(A)
    # print(B)
    # print('-------------------------------------------------')
    if(not status):
        print('Infeasible')
    a = -1
    for i in range(1,m+1):
        if(A[i,0] != floor(A[i,0]) and B[i-1]<=n_or):
            a = i
            break

x = fr(0)*np.zeros(n_or,dtype=fr)
for i in range(len(B)):
    if(B[i]<=n_or):
        x[B[i]-1]=A[i+1,0]
print(x)
if(maxim):
    A[0,0]*=-1
print(A[0,0])
# print('-----------------------------------------------------------------------')



    
    

# A = np.array([list(map(fr,[-3,1,0,0,0,0])),list(map(fr,[1,1,1,0,0,0])),list(map(fr,[-1,-1,0,1,0,-1])),list(map(fr,[1,0,0,0,1,1]))])
# B = [2,3,4]
# # print(A)
# # print(B)

# A,B,stat = dual_simplex(A,B)
# # print(A)
# # print(B)