import argparse
from collections import namedtuple

RockMap = namedtuple("RockMap", ["rocks", "length", "width"])
Point = namedtuple("Point", ["x", "y"])
ROUND_ROCK = 'O'
SQUARE_ROCK = '#'
SPACE = '.'


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    rock_map = parse_rock_map("".join(open(args.input_file_path)).strip())
    return rock_map


def parse_rock_map(input_string):
    input_lines = input_string.split("\n")
    rocks = {}
    for y, row_string in enumerate(input_lines):
        for x, char in enumerate(row_string):
            if char in {ROUND_ROCK, SQUARE_ROCK}:
                rocks[Point(x, y)] = char
            elif char == SPACE:
                continue
            else:
                raise Exception(f"Unknown item in input grid: '{char}'")
    return RockMap(rocks, len(input_lines), max(len(row) for row in input_lines))


def main():
    rock_map = read_input()
    print(f"Part 1: {calculate_load(full_tilt(rock_map))}")
    print(f"Part 2: {calculate_spin_cycle_load(rock_map, 1000000000)}")


def calculate_load(rock_map):
    return sum(rock_map.length - pos.y for pos in rock_map.rocks if rock_map.rocks[pos] == ROUND_ROCK)


def tilt_north(rock_map):
    old_rocks = rock_map.rocks
    new_rocks = {}
    for rock_pos in sorted(old_rocks.keys(), key=lambda r: r.y):
        target_pos = Point(rock_pos.x, rock_pos.y - 1)
        if rock_pos.y == 0 or old_rocks[rock_pos] == SQUARE_ROCK or target_pos in new_rocks:
            new_rocks[rock_pos] = old_rocks[rock_pos]
        else:
            new_rocks[target_pos] = old_rocks[rock_pos]
    return RockMap(new_rocks, rock_map.length, rock_map.width)


def full_tilt(original_rock_map, tilt_function=tilt_north):
    rock_map = original_rock_map
    new_rock_map = tilt_function(rock_map)
    while rock_map != new_rock_map:
        rock_map = new_rock_map
        new_rock_map = tilt_function(new_rock_map)
    return new_rock_map


def calculate_spin_cycle_load(original_rock_map, num_cycles):
    previous_results = []
    previous_input_to_result_index = {}
    new_rock_map = original_rock_map
    i = 0
    while f"{new_rock_map}" not in previous_input_to_result_index:
        previous_results.append(calculate_load(new_rock_map))
        previous_input_to_result_index[f"{new_rock_map}"] = i
        i += 1

        new_rock_map = full_tilt(new_rock_map, tilt_north)
        new_rock_map = full_tilt(new_rock_map, tilt_west)
        new_rock_map = full_tilt(new_rock_map, tilt_south)
        new_rock_map = full_tilt(new_rock_map, tilt_east)
        if i == num_cycles:
            return calculate_load(new_rock_map)
    load_cycle = previous_results[previous_input_to_result_index[f"{new_rock_map}"]:]
    return load_cycle[(num_cycles - i) % len(load_cycle)]


def tilt_east(rock_map):
    old_rocks = rock_map.rocks
    new_rocks = {}
    for rock_pos in sorted(old_rocks.keys(), key=lambda r: r.x, reverse=True):
        target_pos = Point(rock_pos.x + 1, rock_pos.y)
        if rock_pos.x == rock_map.width - 1 or old_rocks[rock_pos] == SQUARE_ROCK or target_pos in new_rocks:
            new_rocks[rock_pos] = old_rocks[rock_pos]
        else:
            new_rocks[target_pos] = old_rocks[rock_pos]
    return RockMap(new_rocks, rock_map.length, rock_map.width)


def tilt_south(rock_map):
    old_rocks = rock_map.rocks
    new_rocks = {}
    for rock_pos in sorted(old_rocks.keys(), key=lambda r: r.y, reverse=True):
        target_pos = Point(rock_pos.x, rock_pos.y + 1)
        if rock_pos.y == rock_map.length - 1 or old_rocks[rock_pos] == SQUARE_ROCK or target_pos in new_rocks:
            new_rocks[rock_pos] = old_rocks[rock_pos]
        else:
            new_rocks[target_pos] = old_rocks[rock_pos]
    return RockMap(new_rocks, rock_map.length, rock_map.width)


def tilt_west(rock_map):
    old_rocks = rock_map.rocks
    new_rocks = {}
    for rock_pos in sorted(old_rocks.keys(), key=lambda r: r.x):
        target_pos = Point(rock_pos.x - 1, rock_pos.y)
        if rock_pos.x == 0 or old_rocks[rock_pos] == SQUARE_ROCK or target_pos in new_rocks:
            new_rocks[rock_pos] = old_rocks[rock_pos]
        else:
            new_rocks[target_pos] = old_rocks[rock_pos]
    return RockMap(new_rocks, rock_map.length, rock_map.width)


if __name__ == "__main__":
    main()
