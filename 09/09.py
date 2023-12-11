import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    lines = [[int(x) for x in line.strip().split(' ')] for line in open(args.input_file_path)]
    return lines


def main():
    lines = read_input()
    print(f"Part 1: {sum(sum(x[-1] for x in get_history(l)) for l in lines)}")
    print(f"Part 2: {sum(get_history(l)[0][0] for l in lines)}")


def get_history(initial_history):
    history = [initial_history.copy()]
    while not all(x == 0 for x in history[-1]):
        history.append([])
        for i in range(len(history[-2]) - 1):
            history[-1].append(history[-2][i + 1] - history[-2][i])

    history[-1].append(0)
    for i in reversed(range(len(history) - 1)):
        history[i] = [history[i][0] - history[i + 1][0]] + history[i]
    return history


if __name__ == "__main__":
    main()
