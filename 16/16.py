import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Beam = namedtuple("Beam", ["position", "direction"])
H_SPLITTER = "-"
V_SPLITTER = "|"
FWD_MIRROR = "/"
BKWD_MIRROR = "\\"
UP = "^"
DOWN = "V"
LEFT = "<"
RIGHT = ">"


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    cave_map = parse_cave_map("".join(open(args.input_file_path)).strip())
    return cave_map


def parse_cave_map(s):
    cave_map = {}
    for y, row in enumerate(s.split("\n")):
        for x, char in enumerate(row):
            if char in {H_SPLITTER, V_SPLITTER, FWD_MIRROR, BKWD_MIRROR}:
                cave_map[Point(x, y)] = char
    return cave_map


def main():
    cave_map = read_input()
    print(f"Part 1: {count_energized_tiles(cave_map)}")
    print(f"Part 2: {max(count_energized_tiles(cave_map, beam) for beam in get_all_edge_beams(cave_map))}")


def count_energized_tiles(cave_map, initial_beam=None):
    if initial_beam is None:
        initial_beam = Beam(Point(0, 0), RIGHT)
    beam_edges = {initial_beam}
    beam_history = set()
    max_x = max(p.x for p in cave_map)
    max_y = max(p.y for p in cave_map)
    while len(beam_edges) > 0:
        new_beam_edges = set()
        for position, direction in beam_edges:
            if (position, direction) in beam_history:
                continue

            if position not in cave_map:
                new_directions = [direction]
            else:
                if cave_map[position] == H_SPLITTER:
                    if direction in {UP, DOWN}:
                        new_directions = [LEFT, RIGHT]
                    else:
                        new_directions = [direction]
                elif cave_map[position] == V_SPLITTER:
                    if direction in {LEFT, RIGHT}:
                        new_directions = [UP, DOWN]
                    else:
                        new_directions = [direction]
                elif cave_map[position] == FWD_MIRROR:
                    if direction == UP:
                        new_directions = [RIGHT]
                    elif direction == DOWN:
                        new_directions = [LEFT]
                    elif direction == LEFT:
                        new_directions = [DOWN]
                    elif direction == RIGHT:
                        new_directions = [UP]
                    else:
                        raise Exception(f"Invalid direction for light beam: '{direction}'")
                elif cave_map[position] == BKWD_MIRROR:
                    if direction == UP:
                        new_directions = [LEFT]
                    elif direction == DOWN:
                        new_directions = [RIGHT]
                    elif direction == LEFT:
                        new_directions = [UP]
                    elif direction == RIGHT:
                        new_directions = [DOWN]
                    else:
                        raise Exception(f"Invalid direction for light beam: '{direction}'")
                else:
                    raise Exception(f"Invalid tile in cave map: '{cave_map[position]}'")
            for new_direction in new_directions:
                if new_direction == UP:
                    new_position = Point(position.x, position.y - 1)
                elif new_direction == DOWN:
                    new_position = Point(position.x, position.y + 1)
                elif new_direction == LEFT:
                    new_position = Point(position.x - 1, position.y)
                elif new_direction == RIGHT:
                    new_position = Point(position.x + 1, position.y)
                else:
                    raise Exception(f"Invalid direction for light beam: '{direction}'")
                if 0 <= new_position.x <= max_x and 0 <= new_position.y <= max_y:
                    new_beam_edges.add(Beam(Point(new_position.x, new_position.y), new_direction))

        beam_history.update(set(beam_edges))
        beam_edges = new_beam_edges
    return len({b.position for b in beam_history})


def get_all_edge_beams(cave_map):
    edge_beams = []
    max_x = max(p.x for p in cave_map)
    max_y = max(p.y for p in cave_map)
    for y in range(max_y + 1):
        edge_beams.append(Beam(Point(0, y), RIGHT))
        edge_beams.append(Beam(Point(max_x, y), LEFT))
    for x in range(max_x + 1):
        edge_beams.append(Beam(Point(x, 0), DOWN))
        edge_beams.append(Beam(Point(x, max_y), UP))
    return edge_beams


if __name__ == "__main__":
    main()
