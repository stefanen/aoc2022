import copy
import functools
import math
import sys

vecadd = lambda *v: tuple(sum(x) for x in zip(*v))

##GET INPUT
day='24'
#p = subprocess.run("bash -c './p_data.sh "+day+" true' ",shell=True)

input = open('../input_d_'+day+'.txt').read()

##PARSE INPUT
lines=[e for e in input.split('\n')]


##PREPARE INITIAL STATE AND ALL FUTURE BLIZZARD STATES
col_length=len(lines)-1
row_length=max([len(lines[c]) for c in range(0,col_length)])

matrix_orig=[[list(lines[y])[x] if len(list(lines[y])) > x else " " for x in range(0, row_length)] for y in range(0, col_length)]
matrix_empty=[[list(lines[y])[x] if len(list(lines[y]))>x and list(lines[y])[x] not in ["^","v",">","<"] else "." for x in range(0,row_length)] for y in range(0,col_length)]

# def visualize2(matrix):
#     print("\n".join(["".join([matrix[y][x]  for x in range(0,len(matrix[0]))]) for y in range(0,col_length)]))

all_dirs=[(0,1),(1,0),(0,0),(-1,0),(0,-1)]

max_distinct_blizzard_state_count=math.lcm(row_length-2,col_length-2)
matrices = [matrix_orig]
for i in range(1,max_distinct_blizzard_state_count):
    next_matrix=copy.deepcopy(matrix_empty)
    for y in range(1,col_length-1):
        for x in range(1,row_length-1):
            if matrix_orig[y][x] in [".","#"]:
                continue
            new_y,new_x=(y,x)
            if matrix_orig[y][x]== "<":
                new_x=(x-i)%(row_length-2)
            elif matrix_orig[y][x]== ">":
                new_x=(x+i)%(row_length-2)
            elif matrix_orig[y][x]== "^":
                new_y=(y-i)%(col_length-2)
            elif matrix_orig[y][x]== "v":
                new_y=(y+i)%(col_length-2)

            if new_x==0:
                new_x=row_length-2
            if new_y==0:
                new_y=col_length-2
            next_matrix[new_y][new_x]="x"
    matrices.append(next_matrix)
    #visualize2(next_matrix)

def manh_d(v1,v2):
    return abs(v1[0]-v2[0])+abs(v1[1]-v2[1])

@functools.cache
def solve(curr, end, time):
    #print(curr,time)
    global best_length_seen

    if curr==end:
        #print(time)
        best_length_seen=min(best_length_seen, time)
        return time
    if time+manh_d(end,curr)>=best_length_seen:
        #TODO
        return best_length_seen
    cands = []
    next_time_modded=(time+1)%max_distinct_blizzard_state_count
    for dir in all_dirs:
        next_y,next_x=vecadd(curr,dir)
        if next_y>=len(matrices[next_time_modded]):
            continue
        if matrices[next_time_modded][next_y][next_x]==".":
            cands.append((next_y,next_x))
    if matrices[next_time_modded][curr[0]][curr[1]]==".":
        cands.append(curr)

    if len(cands)==0:
        return best_length_seen

    return min([solve(cand,end, time+1) for cand in cands])


def solve_wrapper(start,end,time_start,max_search_depth_solve):
    max_allowed_length=time_start+max_search_depth_solve
    #mutable by solve:
    global best_length_seen
    best_length_seen=max_allowed_length

    score=solve(start, end, time_start)
    if score>=max_allowed_length:
        print(f"Failed to find solution of length shorter than {max_search_depth_solve}")
        sys.exit(1)
    return score

##SOLVE
start=(0,1)
#end=(5,6)
end=(26,120)
max_search_depth_solve=400
sys.setrecursionlimit(max_search_depth_solve*5)
print("start p1")
best_time=solve_wrapper(start,end,0,max_search_depth_solve)
print(f"p1 result={best_time}")

best_time=solve_wrapper(end,start,best_time,max_search_depth_solve)
#print(f"p1.5 result={best_time}")

best_time=solve_wrapper(start,end,best_time,max_search_depth_solve)
print(f"p2 result={best_time}")