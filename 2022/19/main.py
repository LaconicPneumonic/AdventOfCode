from collections import defaultdict
from enum import IntEnum
import re
from typing import Dict, Tuple
import time

INPUT_FILE = "./input.txt"


class Material(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3
    INVEST = 4


def getMemoKey(robots, wallet, time):

    return robots + wallet + tuple([time])


def getWalletPotential(robots, wallet, time):

    geodeRobots = robots[Material.GEODE]
    existingGeodes = wallet[Material.GEODE]

    # current geode robots vs buying one every time step
    # time - 1 + time - 2 .. etc = (time - 1)(time -2)
    return existingGeodes + (geodeRobots * (time - 1)) + ((time - 1) * (time) / 2)


MAX_PRUNE = -1
CALLS = 0


def maximize(
    robots: Tuple[int, int, int, int],
    costs: Dict[Material, Dict[Material, int]],
    wallet: Tuple[int, int, int, int],
    time: int,
    maxRobotsNeeded,
    memo=dict(),
) -> Tuple[Tuple[int, int, int, int], Tuple[int, int, int, int]]:

    global MAX_PRUNE
    global CALLS

    CALLS += 1

    print(robots, wallet, time)

    memoKey = getMemoKey(robots, wallet, time)
    if memoKey in memo:

        return memo[memoKey]

    # maximize = for every possible decision in a timestep, chose the maximum
    #            if time step == 0 return
    # runtime is exponential for sure. Is there overlap? likely, so might be able to reduce it

    if time == 0:
        return robots, wallet

    profit = defaultdict(lambda: 0)

    for robot, amt in enumerate(robots):
        profit[robot] = amt

    maxSoFar = tuple([-1 * float("inf")] * 5), tuple([0] * 4)

    explored = None

    for robot, cost in [
        (i, costs[i])
        for i in [
            Material.ORE,
            Material.CLAY,
            Material.OBSIDIAN,
            Material.GEODE,
            Material.INVEST,
        ]
    ]:

        spent = dict(
            [(material, wallet[material] - amount) for material, amount in cost.items()]
        )

        # only invest if I haven't bought already

        print(
            wallet,
            robots,
            robot,
            explored,
            time,
            spent,
        )
        if all([postSpend >= 0 for _, postSpend in spent.items()]) and not (
            robot == Material.INVEST and explored != None
        ):

            robotOrder = [
                Material.ORE,
                Material.CLAY,
                Material.OBSIDIAN,
                Material.GEODE,
            ]

            newWallet = tuple(
                [wallet[r] if r not in spent else spent[r] for r in robotOrder]
            )

            newRobot = tuple(
                [robots[r] if r != robot else robots[r] + 1 for r in robotOrder] + [0]
            )

            # skip if wallet potential is bad
            # No clue why this isn't working
            # if getWalletPotential(
            #     maxSoFar[0], maxSoFar[1], time - 1
            # ) > getWalletPotential(newRobot, newWallet, time - 1):

            #     if time > MAX_PRUNE:
            #         print("POT PRUNE", time)
            #         MAX_PRUNE = time
            #     continue

            if newRobot[robot] > maxRobotsNeeded[robot]:
                if time > MAX_PRUNE:
                    print("ROBOT PRUNE", time, end="\r")
                    MAX_PRUNE = time
                continue

            # skip if we produce more material than is required to buy downstream robots

            potRobot, potWallet = maximize(
                newRobot,
                costs,
                tuple([amount + profit[val] for val, amount in enumerate(newWallet)]),
                time - 1,
                maxRobotsNeeded,
                memo,
            )

            explored = robot

            if maxSoFar[1][Material.GEODE] < potWallet[Material.GEODE]:

                maxSoFar = (potRobot, potWallet)

    memo[memoKey] = maxSoFar

    return maxSoFar


with open(INPUT_FILE, "r") as f:

    bpProduct = 1
    bpSum = 0

    for i, line in enumerate(f.readlines()[:1]):
        bots = re.split(r"[:\.]\s", line.strip())[1:]

        oreRobotCost = re.findall("\d+", bots[0])
        clayRobotCost = re.findall("\d+", bots[1])
        obsidianRobotCost = re.findall("\d+", bots[2])
        geodeRobotCost = re.findall("\d+", bots[3])

        costs = {
            Material.ORE: {Material.ORE: int(oreRobotCost[0])},
            Material.CLAY: {
                Material.ORE: int(clayRobotCost[0]),
            },
            Material.OBSIDIAN: {
                Material.ORE: int(obsidianRobotCost[0]),
                Material.CLAY: int(obsidianRobotCost[1]),
            },
            Material.GEODE: {
                Material.ORE: int(geodeRobotCost[0]),
                Material.OBSIDIAN: int(geodeRobotCost[1]),
            },
            Material.INVEST: {},
        }

        TIME = 24
        totalMemo = dict()
        CALLS = 0
        MAX_PRUNE = -1

        print(line.strip())

        maxRobotsNeeded = dict()
        maxRobotsNeeded[Material.GEODE] = float("inf")
        maxRobotsNeeded[Material.INVEST] = float("inf")

        for cost in costs.values():
            for item, amt in cost.items():
                if item not in maxRobotsNeeded or maxRobotsNeeded[item] < amt:
                    maxRobotsNeeded[item] = amt

        tic = time.perf_counter()
        robot, wallet = maximize(
            tuple([1, 0, 0, 0, 0]),
            costs,
            tuple([0, 0, 0, 0]),
            TIME,
            maxRobotsNeeded,
            totalMemo,
        )
        toc = time.perf_counter()

        print()
        print("TIME", toc - tic, "CALLS", CALLS)
        print(robot, wallet)

        bpSum += (i + 1) * wallet[Material.GEODE]

        if i < -1:
            TIME = 32
            totalMemo = dict()
            CALLS = 0
            MAX_PRUNE = -1

            maxRobotsNeeded = dict()
            maxRobotsNeeded[Material.GEODE] = float("inf")
            maxRobotsNeeded[Material.INVEST] = float("inf")

            for cost in costs.values():
                for item, amt in cost.items():
                    if item not in maxRobotsNeeded or maxRobotsNeeded[item] < amt:
                        maxRobotsNeeded[item] = amt

            tic = time.perf_counter()
            robot, wallet = maximize(
                tuple([1, 0, 0, 0, 0]),
                costs,
                tuple([0, 0, 0, 0]),
                TIME,
                maxRobotsNeeded,
                totalMemo,
            )
            toc = time.perf_counter()

            print()
            print("TIME", toc - tic, "CALLS", CALLS)
            print(wallet[Material.GEODE.GEODE])

            bpProduct *= wallet[Material.GEODE]

        print()
    print(bpSum, bpProduct)
