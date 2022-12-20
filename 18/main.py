INPUT_FILE = "./input.txt"


def neighbors(point):

    dimensions = 3

    ret = []
    for i in range(dimensions):

        for mutation in [-1, 1]:
            toAdd = [0] * dimensions

            toAdd[i] = mutation
            ret.append(toAdd)

    return list(map(lambda p: (p[0] + point[0], p[1] + point[1], p[2] + point[2]), ret))


with open(INPUT_FILE, "r") as f:

    # calculate where everything is

    pointSet = set()

    totalExposedSides = 0
    for line in f:
        point = tuple(map(lambda u: int(u), line.strip().split(",")))

        totalExposedSides += 6

        for n in neighbors(point):
            if n in pointSet:
                # adjacency removes two sides from consideration
                totalExposedSides -= 2

        pointSet.add(point)

    print(totalExposedSides)

    # incrementally cover the droplet in voxels
    maxValInPointSet = max([max(p) for p in pointSet]) + 1
    minValInPointSet = min([min(p) for p in pointSet]) - 1

    stack = [(0, 0, 0)]
    visited = set()

    # water flow can be approximated like a graph search
    while stack:

        p = stack.pop()

        visited.add(p)

        for n in neighbors(p):
            if (
                n not in pointSet
                and max(n) <= maxValInPointSet
                and min(n) >= minValInPointSet
                and n not in visited
            ):

                stack.append(n)

    negativeSet = set()
    negativeSurfaceArea = 0

    # for every valid node, adjust the surface area in the same way as part 1
    for point in visited:

        negativeSurfaceArea += 6

        for n in neighbors(point):
            if n in negativeSet:
                negativeSurfaceArea -= 2

        negativeSet.add(point)

    # the surface are of the covering water - the surface area on the outside of the cube is the answer
    print(negativeSurfaceArea - (6 * ((maxValInPointSet - minValInPointSet + 1) ** 2)))
