import argparse
from collections import namedtuple
from functools import reduce
from math import floor

RaceInfo = namedtuple("RaceInfo", ["time", "record"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    races = parse_race_info("".join(open(args.input_file_path)))
    return races


def parse_race_info(input_string):
    time_string, distance_string = input_string.split("\n")[:2]
    times = [int(s) for s in time_string[9:].split(' ') if len(s) > 0]
    distances = [int(s) for s in distance_string[9:].split(' ') if len(s) > 0]
    return [RaceInfo(t, d) for t, d in zip(times, distances)]


def main():
    races = read_input()
    print(f"Part 1: {reduce(lambda x, y: x * y, (count_margin_basic(ri) for ri in races))}")

    real_time, real_distance = 0, 0
    for rt, rd in races:
        real_time = real_time * (10 ** len(str(rt))) + rt
        real_distance = real_distance * (10 ** len(str(rd))) + rd
    print(f"Part 2: {count_margin_advanced(RaceInfo(real_time, real_distance))}")


def count_margin_basic(race_info):
    return sum(1 if (race_info.time - hold_time) * hold_time > race_info.record else 0
               for hold_time in range(race_info.time))


def count_margin_advanced(race_info):
    lower_margin = find_margin_edge(race_info)
    upper_margin = find_margin_edge(race_info, True)
    return upper_margin - lower_margin + 1


def find_margin_edge(race_info, find_upper_edge=False):
    search_start = 0
    search_end = race_info.time
    while search_end - search_start > 2:
        middle_point = floor((search_start + search_end) / 2)
        middle_point_score = (race_info.time - middle_point) * middle_point
        if middle_point_score > race_info.record:
            if find_upper_edge:
                search_start = middle_point
            else:
                search_end = middle_point
        else:
            if find_upper_edge:
                search_end = middle_point - 1
            else:
                search_start = middle_point + 1

    if find_upper_edge:
        if (race_info.time - search_end) * search_end > race_info.record:
            return search_end
        else:
            return search_start
    else:
        if (race_info.time - search_start) * search_start > race_info.record:
            return search_start
        else:
            return search_end


if __name__ == "__main__":
    main()
