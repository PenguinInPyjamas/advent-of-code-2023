import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Node = namedtuple("Node", ["node_type", "connections"])
NORTH = Point(0, -1)
EAST = Point(1, 0)
SOUTH = Point(0, 1)
WEST = Point(-1, 0)


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    nodes, start_point = parse_nodes("".join(open(args.input_file_path)))
    return nodes, start_point


def parse_nodes(input_string):
    nodes = {}
    start_point = None
    for y, column in enumerate(input_string.split("\n")):
        for x, char in enumerate(column):
            if char == "|":
                nodes[Point(x, y)] = Node(char, [Point(x, y - 1), Point(x, y + 1)])
            elif char == "-":
                nodes[Point(x, y)] = Node(char, [Point(x - 1, y), Point(x + 1, y)])
            elif char == "L":
                nodes[Point(x, y)] = Node(char, [Point(x, y - 1), Point(x + 1, y)])
            elif char == "J":
                nodes[Point(x, y)] = Node(char, [Point(x, y - 1), Point(x - 1, y)])
            elif char == "7":
                nodes[Point(x, y)] = Node(char, [Point(x, y + 1), Point(x - 1, y)])
            elif char == "F":
                nodes[Point(x, y)] = Node(char, [Point(x, y + 1), Point(x + 1, y)])
            elif char == "S":
                start_point = Point(x, y)
            elif char == ".":
                pass
            else:
                raise Exception(f"Cannot parse node at input ({x}, {y}): '{char}'")
    if start_point is not None:
        x, y = start_point
        connected_nodes = [p for p in nodes if start_point in nodes[p].connections]
        start_point_type = None
        if Point(x - 1, y) in connected_nodes:
            if Point(x + 1, y) in connected_nodes:
                start_point_type = "-"
            elif Point(x, y - 1) in connected_nodes:
                start_point_type = "J"
            elif Point(x, y + 1) in connected_nodes:
                start_point_type = "7"
        elif Point(x + 1, y) in connected_nodes:
            if Point(x, y - 1) in connected_nodes:
                start_point_type = "L"
            elif Point(x, y + 1) in connected_nodes:
                start_point_type = "F"
        elif Point(x, y - 1) in connected_nodes:
            if Point(x, y + 1) in connected_nodes:
                start_point_type = "|"
        nodes[start_point] = Node(start_point_type, connected_nodes)
    return nodes, start_point


def main():
    nodes, start_point = read_input()
    print(f"Part 1: {max(find_shortest_distances(nodes, start_point).values())}")
    print(f"Part 2: {find_main_loop_area(nodes, start_point)}")


def find_shortest_distances(nodes, start_point):
    distance = 0
    shortest_distances = {}
    end_points = {start_point}
    while len(end_points) > 0:
        new_end_points = set()
        for p in end_points:
            if p not in shortest_distances:
                shortest_distances[p] = distance
                new_end_points.update(nodes[p].connections)
        end_points = new_end_points
        distance += 1
    return shortest_distances


def find_main_loop_area(nodes, path_start_point):
    num_points_filled_by_loop = 0
    filled_points = set()
    loop_boundary = set(find_shortest_distances(nodes, path_start_point).keys())
    width = max(lx for lx, _ in loop_boundary) + 1
    height = max(ly for _, ly in loop_boundary) + 1
    for fill_start_x in range(width + 1):
        for fill_start_y in range(height + 1):
            fill_start_point = Point(fill_start_x, fill_start_y)
            if fill_start_point not in filled_points and fill_start_point not in loop_boundary:
                checked_points = {}
                edge_points = {fill_start_point}
                pipe_checked_points = set()
                pipe_edge_points = set()
                while len(edge_points) > 0 or len(pipe_edge_points) > 0:
                    new_edge_points = set()
                    new_pipe_edge_points = set()
                    for p in edge_points:
                        if p not in checked_points:
                            if 0 <= p.x <= width and 0 <= p.y <= height and p not in loop_boundary:
                                checked_points[p] = True

                                north_of_p = add_points(p, NORTH)
                                if north_of_p not in loop_boundary:
                                    new_edge_points.add(north_of_p)
                                elif nodes[north_of_p].node_type == "J":
                                    new_pipe_edge_points.add((north_of_p, SOUTH))
                                elif nodes[north_of_p].node_type == "L":
                                    new_pipe_edge_points.add((north_of_p, SOUTH))

                                east_of_p = add_points(p, EAST)
                                if east_of_p not in loop_boundary:
                                    new_edge_points.add(east_of_p)
                                elif nodes[east_of_p].node_type == "L":
                                    new_pipe_edge_points.add((east_of_p, WEST))
                                elif nodes[east_of_p].node_type == "F":
                                    new_pipe_edge_points.add((east_of_p, WEST))

                                south_of_p = add_points(p, SOUTH)
                                if south_of_p not in loop_boundary:
                                    new_edge_points.add(south_of_p)
                                elif nodes[south_of_p].node_type == "7":
                                    new_pipe_edge_points.add((south_of_p, NORTH))
                                elif nodes[south_of_p].node_type == "F":
                                    new_pipe_edge_points.add((south_of_p, NORTH))

                                west_of_p = add_points(p, WEST)
                                if west_of_p not in loop_boundary:
                                    new_edge_points.add(west_of_p)
                                elif nodes[west_of_p].node_type == "J":
                                    new_pipe_edge_points.add((west_of_p, EAST))
                                elif nodes[west_of_p].node_type == "7":
                                    new_pipe_edge_points.add((west_of_p, EAST))
                            else:
                                checked_points[p] = False
                    for p, d in pipe_edge_points:
                        if (p, d) not in pipe_checked_points and p in loop_boundary:
                            pipe_checked_points.add((p, d))
                            new_edge_points.add(add_points(p, d))
                            if nodes[p].node_type == "|":
                                new_pipe_edge_points.add((add_points(p, NORTH), d))
                                new_pipe_edge_points.add((add_points(p, SOUTH), d))
                            if nodes[p].node_type == "-":
                                new_pipe_edge_points.add((add_points(p, EAST), d))
                                new_pipe_edge_points.add((add_points(p, WEST), d))
                            if nodes[p].node_type == "L":
                                if d == NORTH:
                                    new_pipe_edge_points.add((p, EAST))
                                    new_pipe_edge_points.add((add_points(p, EAST), NORTH))
                                if d == EAST:
                                    new_pipe_edge_points.add((p, NORTH))
                                    new_pipe_edge_points.add((add_points(p, NORTH), EAST))
                                if d == SOUTH:
                                    new_pipe_edge_points.add((p, WEST))
                                    new_pipe_edge_points.add((add_points(p, EAST), SOUTH))
                                if d == WEST:
                                    new_pipe_edge_points.add((p, SOUTH))
                                    new_pipe_edge_points.add((add_points(p, NORTH), WEST))
                            if nodes[p].node_type == "J":
                                if d == NORTH:
                                    new_pipe_edge_points.add((p, WEST))
                                    new_pipe_edge_points.add((add_points(p, WEST), NORTH))
                                if d == EAST:
                                    new_pipe_edge_points.add((p, SOUTH))
                                    new_pipe_edge_points.add((add_points(p, NORTH), EAST))
                                if d == SOUTH:
                                    new_pipe_edge_points.add((p, EAST))
                                    new_pipe_edge_points.add((add_points(p, WEST), SOUTH))
                                if d == WEST:
                                    new_pipe_edge_points.add((p, NORTH))
                                    new_pipe_edge_points.add((add_points(p, NORTH), WEST))
                            if nodes[p].node_type == "7":
                                if d == NORTH:
                                    new_pipe_edge_points.add((p, EAST))
                                    new_pipe_edge_points.add((add_points(p, WEST), NORTH))
                                if d == EAST:
                                    new_pipe_edge_points.add((p, NORTH))
                                    new_pipe_edge_points.add((add_points(p, SOUTH), EAST))
                                if d == SOUTH:
                                    new_pipe_edge_points.add((p, WEST))
                                    new_pipe_edge_points.add((add_points(p, WEST), SOUTH))
                                if d == WEST:
                                    new_pipe_edge_points.add((p, SOUTH))
                                    new_pipe_edge_points.add((add_points(p, SOUTH), WEST))
                            if nodes[p].node_type == "F":
                                if d == NORTH:
                                    new_pipe_edge_points.add((p, WEST))
                                    new_pipe_edge_points.add((add_points(p, EAST), NORTH))
                                if d == EAST:
                                    new_pipe_edge_points.add((p, SOUTH))
                                    new_pipe_edge_points.add((add_points(p, EAST), SOUTH))
                                if d == SOUTH:
                                    new_pipe_edge_points.add((p, EAST))
                                    new_pipe_edge_points.add((add_points(p, SOUTH), EAST))
                                if d == WEST:
                                    new_pipe_edge_points.add((p, NORTH))
                                    new_pipe_edge_points.add((add_points(p, SOUTH), WEST))
                    edge_points = new_edge_points
                    pipe_edge_points = new_pipe_edge_points
                new_filled_area = [p for p in checked_points.keys() if checked_points[p] is True]
                inside_loop_boundary = True
                for p in new_filled_area:
                    if p.x == 0 or p.x == width or p.y == 0 or p.y == height:
                        inside_loop_boundary = False
                        break
                if inside_loop_boundary:
                    num_points_filled_by_loop += len(new_filled_area)
                filled_points.update(new_filled_area)
    return num_points_filled_by_loop


def add_points(a, b):
    return Point(a.x + b.x, a.y + b.y)


if __name__ == "__main__":
    main()
