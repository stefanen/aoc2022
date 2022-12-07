from collections import defaultdict
import re

input = open('./input_d_7.txt').read().strip()
lines=[e for e in input.split('\n')]

#INIT STATE
workdir='/'
files = defaultdict(int)
recursive_folder_sizes=defaultdict(int)

#step1 list all files {absolute-file-path: size}
for line in lines:
    parts = line.split(' ')
    if parts[0]=='$':
        if parts[1]=='cd':
            z=parts[2]
            if z=='/':
                workdir='/'
            elif z=='..':
                workdir=re.sub(r"[^/]+/$", "", workdir)
            else:
                workdir=workdir+z+'/'
    elif re.match('[0-9]+',parts[0]):
        files[workdir+parts[1]]=int(parts[0])

#step2, calculate all total folder sizes
for path, size in files.items():
    parent=re.sub(r"[^/]+$", "", path)
    recursive_folder_sizes[parent]+=int(size)
    while parent != "/":
        parent=re.sub(r"[^/]+/$", "", parent)
        recursive_folder_sizes[parent]+=int(size)

#part1
print(sum([size for size in recursive_folder_sizes.values() if size<=100000]))

#part2
needed_space=30000000-(70000000 - recursive_folder_sizes["/"])
print([x for x in sorted(list(recursive_folder_sizes.values())) if x>=needed_space][0])


