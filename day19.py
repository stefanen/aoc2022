import functools
import re
import sys
from collections import defaultdict

vecadd = lambda *v: tuple(sum(x) for x in zip(*v))

sys.setrecursionlimit(10000)

#GET INPUT
day='19'
input = open('../input_d_'+day+'.txt').read().strip()

#PARSE INPUT

pattern = r'.*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?([0-9-]+).*?'
parsed = [(int(bid),int(ore),int(clay),int(obo),int(obc),int(geo),int(geob)) for bid,ore,clay,obo,obc,geo,geob in re.findall(pattern,input)]

lines=[e for e in input.split('\n')]

def try_buy(new,res):
    if new=="OR":
        cost=(-b[1],0,0,0)
        new_robot=(1,0,0,0)
    if new=="CL":
        cost=(-b[2],0,0,0)
        new_robot=(0,1,0,0)
    if new=="OB":
        cost=(-b[3],-b[4],0,0)
        new_robot=(0,0,1,0)
    if new=="GE":
        cost=(-b[5],0,-b[6],0)
        new_robot=(0,0,0,1)
    new_res=vecadd(res,cost)
    if min(new_res)>=0:
        return (True,new_res,new_robot)
    return (False,res,None)

def get_cands(res,robots,time_left,b):
    #if we can immediately afford GE or OB get those and discard other options
    #(not 100% sure of this)
    if res[2]>=b[6] and res[0]>=b[5]:
        return ["GE"]
    if res[1]>=b[4] and res[0]>=b[3]:
        return ["OB"]

    cands=[]
    if robots[2]>0:
        #No sense waiting to build this if prerequisites missing
        cands+=["GE"]
    if robots[1]>0:
        #No sense waiting to build this if prerequisites missing
        cands+=["OB"]
    if robots[0]<max(b[1],b[2],b[3],b[5]):
        cands+=["OR"]
    if robots[1]<b[4]:
        cands+=["CL"]
    return cands

#@functools.cache
def solve(minerals, robots, next_robot_to_buy, time_left, bid, b):
    if time_left==0:
        best_seen[bid]=max(best_seen[bid], minerals[3])
        return minerals[3]

    if (minerals[3] + robots[3] * (time_left) + time_left * (time_left + 1) // 2)<=best_seen[bid]:
        return 0

    buy_sucess,updated_minerals,new_robot =try_buy(next_robot_to_buy, minerals)
    if buy_sucess:
        minerals=updated_minerals
        minerals=vecadd(minerals, robots)
        robots=vecadd(robots,new_robot)
        cands=get_cands(minerals, robots, time_left, b)
    else:
        minerals=vecadd(minerals, robots)
        cands=[next_robot_to_buy]

    #spawn child problems
    return max([solve(minerals, robots, cand, time_left - 1, bid, b) for cand in cands])


parsed=parsed[0:30]
best_seen=defaultdict(int)
best_length_seen=defaultdict(int)
for nextr in ["OR","CL"]:

    for b in parsed:
        res=(0,0,0,0)
        robots=(1,0,0,0)
        #print(b)
        best_score=solve(res, robots, nextr, 24, b[0], b)
        #print(best_score)
        best_length_seen[b[0]]=max(best_length_seen[b[0]], best_score * b[0])

print(best_length_seen)
s=0
for k,v in sorted(best_length_seen.items()):
    s+=v
print("part1")
print(s)

##part2

parsed=parsed[0:3]
best_seen=defaultdict(int)
best_length_seen=defaultdict(int)
for nextr in ["OR","CL"]:

    for b in parsed:
        res=(0,0,0,0)
        robots=(1,0,0,0)
        #print(b)
        best_score=solve(res, robots, nextr, 32, b[0], b)
        #print(best_score)
        best_length_seen[b[0]]=max(best_length_seen[b[0]], best_score)

print(best_length_seen)
product=1
for k,v in sorted(best_length_seen.items()):
    product*=v
print(product)
