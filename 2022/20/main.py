INPUT_FILE = "./input.txt"


class ListNode:
    def __init__(self, val, prev=None) -> None:
        self.val = val
        self.next = None
        self.prev = prev


# old methods
def rotate(start, destination, array):

    if start == destination:
        return array

    if destination > start:
        for i in range(start + 1, destination + 1):

            temp = array[i - 1]
            array[i - 1] = array[i]
            array[i] = temp

    else:
        for i in range(start - 1, destination - 1, -1):
            temp = array[i + 1]
            array[i + 1] = array[i]
            array[i] = temp

    return array


def mix(originalOrder):
    for node in originalOrder:
        swaps = node.val

        curr = node

        if swaps == 0:
            pass

        elif swaps > 0:
            # probably not the most efficient swap, but it took me way too long to get this right
            for _ in range(swaps):
                nextVal = curr.next
                after = curr.next.next
                prev = curr.prev

                curr.next = after
                curr.prev = nextVal
                nextVal.next = curr
                nextVal.prev = prev
                prev.next = nextVal
                after.prev = curr

        elif swaps < 0:
            for _ in range(abs(swaps)):
                prev = curr.prev
                prevPrev = curr.prev.prev
                nextVal = curr.next

                curr.prev = prevPrev
                curr.next = prev
                prev.next = nextVal
                prev.prev = curr
                nextVal.prev = prev
                prevPrev.next = curr


# new fast method
def mixTwo(originalOrder):
    for node in originalOrder:
        swaps = node.val

        swaps = swaps % (len(originalOrder) - 1)

        curr = node

        if swaps == 0:
            pass

        # probably not minima
        elif swaps > 0:
            for _ in range(swaps):
                nextVal = curr.next
                after = curr.next.next
                prev = curr.prev

                curr.next = after
                curr.prev = nextVal
                nextVal.next = curr
                nextVal.prev = prev
                prev.next = nextVal
                after.prev = curr

        elif swaps < 0:
            for _ in range(abs(swaps)):
                prev = curr.prev
                prevPrev = curr.prev.prev
                nextVal = curr.next

                curr.prev = prevPrev
                curr.next = prev
                prev.next = nextVal
                prev.prev = curr
                nextVal.prev = prev
                prevPrev.next = curr


# helper
def toArray(node, l):

    curr = node

    ret = []

    for _ in range(l):

        ret.append(curr.val)
        curr = curr.next

    return ret


def p1():
    with open(INPUT_FILE, "r") as f:

        code = [int(i.strip()) for i in f]

        root = ListNode(code[0])
        curr = root
        originalOrder = [root]

        nodeForZero = None

        for i in code[1:]:

            curr.next = ListNode(i, curr)

            if i == 0:
                nodeForZero = curr.next

            originalOrder.append(curr.next)
            curr = curr.next

        curr.next = root
        root.prev = curr

        mixTwo(originalOrder)

        tempCurr = nodeForZero

        total = 0
        for i in range(4000):

            if i in {1000, 2000, 3000}:

                total += tempCurr.val

            tempCurr = tempCurr.next

        print(total)


def p2():
    with open(INPUT_FILE, "r") as f:

        code = [811589153 * int(i.strip()) for i in f]

        root = ListNode(code[0])
        curr = root
        originalOrder = [root]

        nodeForZero = None

        for i in code[1:]:

            curr.next = ListNode(i, curr)

            if i == 0:
                nodeForZero = curr.next

            originalOrder.append(curr.next)
            curr = curr.next

        curr.next = root
        root.prev = curr

        for i in range(10):
            mixTwo(originalOrder)

        tempCurr = nodeForZero

        total = 0
        for i in range(4000):

            if i in {1000, 2000, 3000}:

                total += tempCurr.val

            tempCurr = tempCurr.next

        print(total)


p1()
p2()
