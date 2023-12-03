import argparse
from collections import namedtuple, defaultdict
from functools import reduce


GameInfo = namedtuple("GameInfo", ["gameId", "rounds"])
Cube = namedtuple("Cube", ["colour", "count"])

PART_1_MAX_CUBES = [Cube("red", 12), Cube("green", 13), Cube("blue", 14)]


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    games = [read_game_info(line) for line in open(args.input_file_path)]
    return games


def read_game_info(s):
    id_string, game_string = s.split(":")
    game_id = int(id_string[5:])
    rounds = [[Cube(cube_string.split(" ")[1], int(cube_string.split(" ")[0]))
              for cube_string in round_string.split(", ")]
              for round_string in game_string.strip().split("; ")]
    return GameInfo(game_id, rounds)


def main():
    games = read_input()
    print(f"Part 1: {sum(g.gameId if verify_max_cubes(g.rounds, PART_1_MAX_CUBES) else 0 for g in games)}")
    print(f"Part 2: {sum(reduce(lambda x, y: x * y, find_game_requirements(g).values()) for g in games)}")


def verify_max_cubes(rounds, max_cubes):
    for game_round in rounds:
        for r_cube in game_round:
            for m_cube in max_cubes:
                if r_cube.colour == m_cube.colour:
                    if r_cube.count > m_cube.count:
                        return False
                    else:
                        continue
    return True


def find_game_requirements(game):
    minimum_requirements = defaultdict(lambda: 0)
    for game_round in game.rounds:
        for cube in game_round:
            minimum_requirements[cube.colour] = max(minimum_requirements[cube.colour], cube.count)
    return minimum_requirements


if __name__ == "__main__":
    main()
