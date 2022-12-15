import itertools
import subprocess
import sys
from collections import defaultdict

scanners = defaultdict(int)
score=0
#GET INPUT
day='15'
#p = subprocess.run("bash -c './p_data.sh "+day+" true' ",shell=True)
input = open('./input_d_'+day+'.txt').read().strip()

#PARSE INPUT
lines=[e for e in input.split('\n')]

for line in lines:
    parts=line.split(',')
    sx=int(parts[0].split("=")[1])
    sy=int(parts[1].split(":")[0].split("=")[1])
    bx=int(parts[1].split(":")[1].split("=")[1])
    by=int(parts[2].split("=")[1])
    d=abs(sx-bx)+abs(sy-by)
    scanners[(sx, sy)]=d

plus_diags=set()
minus_diags=set()
for q in itertools.combinations(scanners.items(), 2):
    p1s1=q[0][0][0]+q[0][0][1]-(q[0][1]+1)
    p1s2=q[0][0][0]+q[0][0][1]+(q[0][1]+1)
    p1t1=q[0][0][0]-q[0][0][1]-(q[0][1]+1)
    p1t2=q[0][0][0]-q[0][0][1]+(q[0][1]+1)

    p2s1=q[1][0][0]+q[1][0][1]-(q[1][1]+1)
    p2s2=q[1][0][0]+q[1][0][1]+(q[1][1]+1)
    p2t1=q[1][0][0]-q[1][0][1]-(q[1][1]+1)
    p2t2=q[1][0][0]-q[1][0][1]+(q[1][1]+1)

    if p1t1==p2t2 or p1t1==p2t1:
        print("overlapping t-diag",q[0],q[1],p1t1)
        minus_diags.add(p1t1)
    if p1t2==p2t2 or p1t2==p2t1:
        print("overlapping t-diag",q[0],q[1],p1t2)
        minus_diags.add(p1t2)
    if p1s1==p2s2 or p1s1==p2s1:
        print("overlapping s-diag",q[0],q[1],p1s1)
        plus_diags.add(p1s1)
    if p1s2==p2s2 or p1s2==p2s1:
        print("overlapping s-diag",q[0],q[1],p1s2)
        plus_diags.add(p1s2)

print(plus_diags)
print(minus_diags)

print(f"candidate count= {len([x for x in itertools.product(plus_diags, minus_diags)])}")
#Case1 solution exists in interior of [0,4000000],[0,4000000]
for c in itertools.product(plus_diags, minus_diags):
    # x+y=c[0]
    # x-y=c[1]
    # =>
    x=(c[0]+c[1])//2
    y=(c[0]-c[1])//2
    if 0<x<4000000 and 0<y<4000000:
        candidate_ok=True
    else:
        candidate_ok=False
        continue
    for s,v in scanners.items():
        d=abs(s[0]-x)+abs(s[1]-y)
        if d<=v:
            candidate_ok=False
    if candidate_ok:
        break
if candidate_ok:
    print(f'Solution found in interior of grid {(x,y)}')
    print(x*4000000+y)
    sys.exit()

#case2 and 3
print("case2 and case3 not implemented, (no need yet)")
sys.exit()
#Case2 solution exists on corner boundary of [0,4000000],[0,4000000]

#Case3 solution exists on edge boundary of [0,4000000],[0,4000000]

#
# sys.exit()
#
# x=0
# counter=0
# while x<4000000:
#     y=0
#     if x%100000==0:
#         print(x,counter)
#     while y<4000000:
#         counter+=1
#         min_d=1
#         for s,v in scanners.items():
#             d=abs(s[0]-x)+abs(s[1]-y)
#             min_d=min(d-v,min_d)
#             #print(d-v)
#         if min_d<1:
#             y+=max(1,abs(min_d))
#         else:
#             print(x,y)
#             sys.exit()
#             x+=1
#
#
#     x+=1
#
# print(score)



