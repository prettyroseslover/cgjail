import os

def children(pid):
    
    tids = os.listdir(f"/proc/{pid}/task")
    all_children = []

    for tid in tids:
        with open(f"/proc/{pid}/task/{tid}/children") as f:
            children = f.readline().strip(' ').split(' ')
        
        if children == ['']:
            continue

        all_children.extend(list(map(int, children)))

    return all_children

