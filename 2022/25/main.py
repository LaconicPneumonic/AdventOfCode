import math

INPUT_FILE = "./input.txt"


def snafuToDecimal(s: str) -> int:

    ret = 0

    charMapping = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    snafuDigits = len(s) - 1

    for i, c in enumerate(s):
        ret += charMapping[c] * 5 ** (snafuDigits - i)

    return ret


def convertToBaseFive(n):

    if n == 0:
        return "0"

    ret = []

    while n:
        ret.append(n % 5)

        n //= 5

    ret.reverse()

    return ret


# converted from the alg for balanced ternary here: https://www.geeksforgeeks.org/balanced-ternary-number-system/
def decimalToSnafu(num: int) -> str:

    baseFive = [0] + convertToBaseFive(num)

    for i in reversed(range(1, len(baseFive))):
        if baseFive[i] > 2:
            baseFive[i - 1] += 1
            baseFive[i] += 2

    ret = ""

    for i in range(len(baseFive)):

        if i == 0 and baseFive[i] == 0:
            continue
        elif baseFive[i] == 5:
            ret += "="
        elif baseFive[i] == 6:
            ret += "-"

        elif baseFive[i] == 7:
            ret += "0"
        else:
            ret += str(baseFive[i])

    return ret


with open(INPUT_FILE, "r") as f:

    decimalSum = 0

    for line in f:

        line = line.strip()

        decimalRep = snafuToDecimal(line)

        decimalSum += decimalRep

    print(decimalToSnafu(decimalSum))
