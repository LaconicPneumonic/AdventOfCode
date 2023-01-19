from collections import defaultdict
from functools import cache
from typing import Dict, Set, Tuple
import re

INPUT_FILE = "./input.txt"


def findHighestFlow(source, neighbors, flowAtNode, timeLeft):
    queue = [(source, 0, source)]
    visited = set()

    maxFlow = 0
    maxNode = (None, None, None, None)

    while queue:

        curr, dist, path = queue.pop()
        visited.add(curr)

        remainingTimeIfOpened = timeLeft - (dist + 1)
        flowIfOpened = flowAtNode[curr] * remainingTimeIfOpened

        if flowIfOpened > maxFlow:

            maxNode = (curr, remainingTimeIfOpened, flowIfOpened, path)
            maxFlow = flowIfOpened

        for n in neighbors[curr]:
            if n not in visited:
                queue.append((n, dist + 1, path + " " + n))

    return maxNode


def getNeighbors(
    curr: Tuple[str, int],
    neighbors: Dict[str, Set[str]],
    flowAtNode: Dict[str, int],
    activated,
):

    remainingTime = curr[1] - 1
    ret = []

    if flowAtNode[curr[0]] != 0 and curr[0] not in activated:
        ret.append(
            (
                (
                    curr[0],
                    remainingTime,
                ),
                -1 * flowAtNode[curr[0]] * remainingTime,
            )
        )

    for n in neighbors[curr[0]]:
        ret.append(((n, remainingTime), 0))
        # ret.append(((n, remainingTime - 1), -1 * flowAtNode[n] * (remainingTime - 1)))

    return ret


# what if we have a graph where the state is the current location and the time we have left
# the edges are the total flow contribution of this decision i.e. move, open
# there no loops since time always progresses forward, the graph weights are dynamic.

# essentially we're constructing a 2d graph here that is acyclic, with positive weights.
# we want to find the longest path which is equal to the shortest path in the negative graph
# source = ("AA", 30), target = (Any, 0)
# We'll use djikstra's!
def djikstras(neighbors, flowAtNode):

    queue = []
    queue.append((0, ("AA", 30)))

    dist: Dict[str, int] = dict()
    dist[("AA", 30)] = 0

    prev: Dict[str, str] = dict()

    activated = set()
    totalFLow = 0

    while queue:

        queue = sorted(queue, key=lambda q: q[0])
        _, curr = queue.pop()

        print(curr, activated)

        if curr[1] < 0:
            print("FOUND THE END", curr)

            break

        for neighbor, weight in getNeighbors(curr, neighbors, flowAtNode, activated):

            print(neighbor, weight)

            alt = dist[curr] + weight

            if neighbor not in dist or alt < dist[neighbor]:

                if neighbor in prev and prev[neighbor[0]] in activated:
                    activated.remove(curr)

                activated.add(neighbor[0])
                dist[neighbor] = alt
                prev[neighbor] = curr
                queue.append((alt, neighbor))

    print(prev)


def greedy(neighbors, flowAtNode):
    curr = "AA"
    remainingTimeIfOpened = 30
    finalFlow = 0

    i = 0
    while curr != None and i < 1000:
        curr, remainingTimeIfOpened, flowIfOpened, path = findHighestFlow(
            curr, neighbors, flowAtNode, remainingTimeIfOpened
        )

        if curr == None:
            break

        flowAtNode[curr] = 0
        finalFlow += flowIfOpened

        print(path, "=>", curr, remainingTimeIfOpened, flowIfOpened)
        i += 1

    print(finalFlow)


# kept old solutions before finding the correct one with hints from reddit
with open(INPUT_FILE, "r") as f:

    neighbors = defaultdict(set)
    flowAtNode: Dict[str, int] = dict()

    for line in f:

        print(line.strip())
        m = re.search(
            "Valve ([A-Z]{1,2}) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)$",
            line,
        )

        valve, flow, tunnels = m.groups()

        neighbors[valve].update(tunnels.split(", "))
        flowAtNode[valve] = int(flow)

    dist = defaultdict(lambda: float("inf"))

    for edge in [
        (source, target) for source, targets in neighbors.items() for target in targets
    ]:
        dist[edge] = 1

    for node in neighbors:
        dist[(node, node)] = 0

    for k in neighbors:
        for i in neighbors:
            for j in neighbors:
                if dist[(i, j)] > dist[(i, k)] + dist[(k, j)]:
                    dist[(i, j)] = dist[(i, k)] + dist[(k, j)]

    nodesWithFlow = frozenset([key for key, value in flowAtNode.items() if value != 0])

    @cache
    def backtracking(node, time, openValves: frozenset[str]):

        if len(openValves) == 0:
            return 0

        return max(
            [
                flowAtNode[o] * (time - dist[(node, o)] - 1)
                + backtracking(
                    o,
                    time - dist[(node, o)] - 1,
                    openValves.difference([o]),
                )
                for o in openValves
                if time - dist[(node, o)] >= 0
            ]
            + [0]
        )

    def backtrackingTwo(node, time, openValves: frozenset[str]):

        if len(openValves) == 0:
            return 0

        return max(
            [
                flowAtNode[o1] * (time - dist[(node, o1)] - 1)
                + backtrackingTwo(
                    o1,
                    time - dist[(node, o1)] - 1,
                    openValves.difference([o1]),
                )
                for o1 in openValves
                if time - dist[(node, o1)] - 1 >= 0
            ]
            # for which set of valves that the elf captures does the elephant capturing the rest
            # maximize the end amount of flow released. The elephant needs the max amount of time to find its
            # solution so we start with 26 as the time remaining.
            + [backtracking("AA", 26, openValves)]
        )

    print(backtracking("AA", 30, nodesWithFlow))
    print(backtrackingTwo("AA", 26, nodesWithFlow))
