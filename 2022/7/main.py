from typing import List
from collections import Counter

FILE_NAME = "./input.txt"


def problem():

    with open(FILE_NAME, "r") as f:

        # create a pretend root
        DISK = "C:"
        stack = [DISK]
        directorySizes = Counter()

        while stack:
            line = f.readline().strip()
            tokens: List[str] = line.strip().split(" ")

            if tokens[0] == "$" and tokens[1] == "cd":
                if tokens[2] != "..":
                    # a folder is defined by its current PWD
                    currPath = stack[-1] + "/" + tokens[2]
                    print("ENTERING", currPath)
                    stack.append(currPath)
                else:
                    # we're leaving this folder, so add the information I've accumulated
                    leaving = stack.pop()
                    directorySizes[stack[-1]] += directorySizes[leaving]
                    print(
                        f"LEAVING  {leaving} FOR {stack[-1]} AND ADDING {directorySizes[leaving]}"
                    )
            elif tokens[0].isnumeric():
                # we've found a file, so add the size to every path we've seen so far
                print("FILE", f"{stack[-1] + '/' +  tokens[1]}:{tokens[0]}")
                directorySizes[stack[-1]] += int(tokens[0])

            elif tokens[0] == "":
                # end of file remove "/"
                leaving = stack.pop()
                if stack:
                    # update the parent node if it exists
                    directorySizes[stack[-1]] += directorySizes[leaving]
                    print(
                        f"LEAVING  {leaving} FOR {stack[-1]} AND ADDING {directorySizes[leaving]}"
                    )

            else:
                # we are ignoring 'dir *' and 'ls *' since they do not contribute to our flow
                pass

        ROOT = f"{DISK}//"
        print()
        # problem 1
        print(f"CURR SIZE {directorySizes[ROOT]}")
        print(
            f"SPACE OF DIRS <= 100000 = {sum([value for _, value in directorySizes.items() if value <= 100000])}"
        )

        # problem 2
        TOTAL = 70000000
        spaceNeeded = 30000000 - (TOTAL - directorySizes[ROOT])
        print(f"SPACE NEEDED {spaceNeeded}")
        minimumDirectory = float("inf")
        minDirectoryName = ""
        for d, size in directorySizes.items():
            if size >= spaceNeeded and size <= minimumDirectory:
                minimumDirectory = size
                minDirectoryName = d

        print(f"FILE TO REMOVE {minDirectoryName} => {minimumDirectory}")


def main():
    problem()


main()
