import sys
import itertools
import functools
import copy
from typing import Iterable
import subprocess
from collections import Counter
from collections import defaultdict
from collections import namedtuple
import re
import aoc
import numpy as np
import networkx as nx
import operator
import time

vecadd = lambda *v: tuple(sum(x) for x in zip(*v))

sys.setrecursionlimit(10000)

#GET INPUT
day='22'
p = subprocess.run("bash -c './p_data.sh "+day+" true' ",shell=True)

input = open('./input_d_'+day+'.txt').read()

#PARSE INPUT

pattern = r'.*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?'
#parsed = [(int(bid),int(ore),int(clay),int(obo),int(obc),int(geo),int(geob)) for bid,ore,clay,obo,obc,geo,geob in re.findall(pattern,input)]

lines=[e for e in input.split('\n')]
col_length=len(lines)-2
row_length=max([len(lines[c]) for c in range(0,col_length)])

matrix=[[list(lines[y])[x] if len(list(lines[y]))>x else " " for x in range(0,row_length)] for y in range(0,col_length)]
new_matrix=[[matrix[y-1][x-1] if x!=0 and x!=row_length+1 and y!=0 and y!=col_length+1 else " " for x in range(0,row_length+2)] for y in range(0,col_length+2)]
matrix=new_matrix
#
# r_jumps=copy.deepcopy(matrix)
# for curr_y in range(col_length+2):
#     for curr_x in range(row_length+2):
#         target=None
#         if curr_x==151 and 1<=curr_y<=50:
#             target= (151-curr_y,100,2) #OK
#         elif curr_x==101 and 51<=curr_y<=100:
#             target= (50,50+curr_y,3) #OK
#         elif curr_x==101 and 101<=curr_y<=150:
#             target = (151-curr_y,150,2)
#         elif curr_x==51 and 151<=curr_y<=200:
#             target = (150,curr_y-100,3)
#         if
#         r_jumps[curr_y][curr_x]=target

curr_y=1
curr_x=51
curr_f=0

curr_i=""
instructions=[]
for i in range(0,len(lines[len(lines)-1])):
    curr_i+=lines[len(lines)-1][i]
    if curr_i.isnumeric() and i+1<len(lines[len(lines)-1]) and lines[len(lines)-1][i+1].isnumeric():
        continue
    else:
        if curr_i.isnumeric():
            instructions.append(int(curr_i))
        else:
            instructions.append(curr_i)
        curr_i=""

print(instructions)

def lookup(curr_y,curr_x,curr_f):

    #RIGHT
    if curr_f==0:
        if curr_x==151 and 1<=curr_y<=50:
            return (151-curr_y,100,2) #OK
        elif curr_x==101 and 51<=curr_y<=100:
            return (50,50+curr_y,3) #OK
        elif curr_x==101 and 101<=curr_y<=150:
            return (151-curr_y,150,2)
        elif curr_x==51 and 151<=curr_y<=200:
            return (150,curr_y-100,3)
    elif curr_f==1:
    #DOWN
        if curr_y==51 and 101<=curr_x<=150:
            return (curr_x-50,100,2)
        elif curr_y==151 and 51<=curr_x<=100:
            return (curr_x+100,50,2)
        elif curr_y==201 and 1<=curr_x<=50:
            return (1,curr_x+100,1)
    #LEFT
    elif curr_f==2:
        if curr_x==50 and 1<=curr_y<=50:
            return (151-curr_y,1,0)
        elif curr_x==50 and 51<=curr_y<=100:
            return (101,curr_y-50,1)
        elif curr_x==0 and 101<=curr_y<=150:
            return (151-curr_y,51,0)
        elif curr_x==0 and 151<=curr_y<=200:
            return (1,curr_y-100,1)
    elif curr_f==3:
        #UP
        if curr_y==0 and 101<=curr_x<=150:
            return (200,curr_x-100,3)
        elif curr_y==0 and 51<=curr_x<=100:
            return (curr_x+100,1,0)
        elif curr_y==100 and 1<=curr_x<=50:
            return (curr_x+50,51,0)


dirs={
    0:(0,1),
    1:(1,0),
    2:(0,-1),
    3:(-1,0)
}

for i in instructions:
    if type(i)==int:
        for k in range(0,i):
            (next_y,next_x) = vecadd(dirs[curr_f],(curr_y,curr_x))
            if matrix[next_y][next_x]==".":
                curr_y,curr_x=(next_y,next_x)
            elif matrix[next_y][next_x]=="#":
                break
            elif matrix[next_y][next_x]==" ":
                next=lookup(next_y,next_x,curr_f)
                if matrix[next[0]][next[1]]==".":
                    curr_y,curr_x,curr_f=next
                    continue
                else:
                    break
    else:
        if i=="R":
            curr_f=(curr_f+1)%4
        if i=="L":
            curr_f=(curr_f+3)%4
    #print(i,curr_y,curr_x,curr_f)
    #visualize(matrix,curr_x,curr_y,curr_f)

print(1000*curr_y+4*curr_x+curr_f)