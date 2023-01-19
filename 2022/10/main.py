INPUT_FILE = "./input.txt"


with open(INPUT_FILE, "r") as f:
    # CPU
    X = 1
    cycle = 0
    buffer = 0
    carriedValue = 0

    ret = 0

    # CRT values
    ROWS, COLS = 6, 40

    while True:
        cycle += 1
        row, col = (cycle - 1) // COLS, (cycle - 1) % COLS

        print("#" if X - 1 <= col <= X + 1 else ".", end="")

        if col == COLS - 1:
            print()

        if (cycle - 20) % 40 == 0:
            ret += cycle * X

        if buffer != 0:
            buffer -= 1
            X += carriedValue
            carriedValue = 0
            continue

        command = f.readline().strip().split(" ")

        if command[0] == "noop":
            buffer = 0
            carriedValue = 0
        elif command[0] == "addx":
            buffer = 1
            carriedValue = int(command[1])

        elif buffer == 0:
            break

    print(ret)
