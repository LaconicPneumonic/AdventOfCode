from typing import List
from collections import Counter
FILE_NAME = './input.txt'

def problem():

    with open(FILE_NAME, 'r') as f:

        stack = ["/"]
        f.readline()

        directorySizes = Counter()

        while stack:
            line = f.readline().strip()
            tokens: List[str] = line.strip().split(" ")

            if tokens[0] == '$' and tokens[1] == 'cd':
                if tokens[2] != '..':
                    # a folder is defined by its current PWD
                    currPath = stack[-1] + "/" +  tokens[2]
                    print("ENTERING", currPath)
                    stack.append(currPath)
                else:
                    # we're leaving this folder maybe to return
                    leaving = stack.pop()
                    print("LEAVING", leaving)
            elif tokens[0].isnumeric():
                # we've found a file, so add the size to every path we've seen so far
                print("FILE", f"{stack[-1] + '/' +  tokens[1]}:{tokens[0]}")
                for directory in stack:
                    directorySizes[directory] += int(tokens[0])
            elif tokens[0] == '':
                # end of file remove "/"
                stack.pop()

            else:
                # we are ignoring 'dir *' and 'ls *' since they do not contribute to our flow
                pass
    

        print()
        # problem 1
        print(f"SPACE OF DIRS <= 100000 = {sum([value for _, value in directorySizes.items() if value <= 100000])}")
        
        # problem 2
        TOTAL = 70000000
        spaceNeeded = 30000000 - (TOTAL - directorySizes["/"])
        print(f"SPACE NEEDED {spaceNeeded}")
        minimumDirectory = float('inf')
        minDirectoryName = ""
        for d, size in directorySizes.items():
            if size >= spaceNeeded:
                minimumDirectory = min(minimumDirectory, size)
                minDirectoryName = d
        print(f"FILE TO REMOVE{minDirectoryName}:{minimumDirectory}")

def main():
   problem()

main()