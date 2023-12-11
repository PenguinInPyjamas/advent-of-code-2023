import argparse
from itertools import takewhile, cycle
from functools import reduce
from math import gcd


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    lines = [line.strip() for line in open(args.input_file_path)]
    return lines[0], dict((line[0:3], (line[7:10], line[12:15])) for line in lines[2:])


def main():
    instructions, nodes = read_input()
    if "AAA" in nodes:
        print(f"Part 1: {len(list(takewhile(lambda x: x != 'ZZZ', follow_instructions(instructions, nodes)))) + 1}")
    else:
        print("Part 1 not valid for this input")
    print(f"Part 2: {get_ghost_steps(instructions, nodes)}")


def follow_instructions(instructions, nodes, start_node="AAA"):
    current_node = start_node
    for i in cycle(instructions):
        if i == 'L':
            current_node = nodes[current_node][0]
        elif i == 'R':
            current_node = nodes[current_node][1]
        else:
            raise Exception(f"Instruction '{i}' is not valid")
        yield current_node


# This relies on the assumption that each ghost is on their own path,
# and that there are no nodes that aren't part of their ghost's endless looping path
def get_ghost_steps(instructions, nodes):
    loop_lengths = {len(list(takewhile(lambda x: x[2] != 'Z', follow_instructions(instructions, nodes, n)))) + 1
                    for n in nodes.keys() if n[2] == 'A'}
    return reduce(lambda x, y: int(x * y / gcd(x, y)), loop_lengths)


if __name__ == "__main__":
    main()
