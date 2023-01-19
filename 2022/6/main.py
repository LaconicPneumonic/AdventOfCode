from collections import deque
FILE_NAME = './input.txt'


def indexOfUniqueLength(line, length):
    initial = length - 1
    s = deque([c for c in line[:initial]])
    for c in range(initial, len(line)):
        s.append(line[c])
        if len(set(s)) == length:
            return c + 1
        s.popleft()


def problemTwo(line):
    return indexOfUniqueLength(line, 14)


def problemOne(line):
    return indexOfUniqueLength(line, 4)


def main():

    with open(FILE_NAME, 'r') as f:
        line = f.readlines()[0]
        print(f"P1: {problemOne(line)}")
        print(f"P2: {problemTwo(line)}")


main()
