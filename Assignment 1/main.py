import numpy

obj=""

with open("input.txt","r") as f:
    inp = f.readline()
    while(inp):
        if(inp == '[objective]\n'):
            obj = f.readline()
        if(inp == '[A]\n'):
            inp=f.readline()
            while(inp!='\n'):
                row = list(map(int,inp[:-1].split(", ")))
                
                inp=f.readline()
        inp = f.readline()
