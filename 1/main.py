

def problemOne():
    fileName = "./input.txt"

    with open(fileName, 'r') as f:

        maxElf = 0
        totalSoFar = 0
        for line in f.readlines():
            line = line[:len(line) - 1]

            if len(line) == 0:
                totalSoFar = 0
            else:
                totalSoFar += int(line)
                maxElf = max(totalSoFar, maxElf)

        print(maxElf)


def problemTwo():
    fileName = "./input.txt"

    with open(fileName, 'r') as f:

        totalSoFar = 0
        topThree = [0, 0, 0]
        for line in f.readlines():
            line = line[:len(line) - 1]

            if len(line) == 0:
                totalSoFar = 0
            else:
                totalSoFar += int(line)
                topThree.append(totalSoFar)
                topThree = sorted(topThree, reverse=True)[:3]

        print(sum(topThree))


def main():
    problemOne()
    problemTwo()


main()
