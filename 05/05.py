import argparse
from collections import namedtuple

Almanac = namedtuple("Almanac", ["seeds", "maps"])
MapRange = namedtuple("MapRange", ["dest_start", "source_start", "length"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    almanac = parse_almanac("".join(open(args.input_file_path)).strip())
    return almanac


def parse_almanac(input_string):
    section_strings = input_string.split("\n\n")
    seeds = [int(s) for s in section_strings[0][7:].split(' ')]
    maps = [[MapRange(*(int(s) for s in map_range_string.split(" ")))
             for map_range_string in almanac_map.split("\n")[1:]]
            for almanac_map in section_strings[1:]]
    return Almanac(seeds, maps)


def main():
    almanac = read_input()
    print(f"Part 1: {min(get_seed_location_numbers_part_1(almanac))}")
    print(f"Part 2: {min(x[0] for x in get_seed_location_ranges_part_2(almanac))}")


def get_seed_location_numbers_part_1(almanac):
    location_numbers = []
    for seed in almanac.seeds:
        location = seed
        for almanac_map_ranges in almanac.maps:
            for dest_start, source_start, length in almanac_map_ranges:
                if source_start <= location < source_start + length:
                    location = dest_start + location - source_start
                    break
        location_numbers.append(location)
    return location_numbers


def get_seed_location_ranges_part_2(almanac):
    mapped_ranges = []
    for i in range(0, len(almanac.seeds), 2):
        mapped_ranges.append((almanac.seeds[i], almanac.seeds[i + 1]))
    mapped_ranges.sort()

    for almanac_map_ranges in almanac.maps:
        new_location_ranges = []
        for active_range_start, active_range_length in sorted(mapped_ranges, key=lambda r: r[0]):
            last_mapped_location = active_range_start - 1
            for map_destination, map_range_start, map_range_length in sorted(almanac_map_ranges, key=lambda mr: mr[1]):
                if map_range_start + map_range_length < active_range_start:
                    continue
                if map_range_start > active_range_start + active_range_length:
                    break

                overlap_start = max(active_range_start, map_range_start)
                overlap_end = min(active_range_start + active_range_length, map_range_start + map_range_length)
                overlap_length = overlap_end - overlap_start
                mapped_start = overlap_start + map_destination - map_range_start

                new_location_ranges.append((mapped_start, overlap_length))
                if overlap_start > last_mapped_location + 1:
                    new_location_ranges.append((last_mapped_location + 1, overlap_start - last_mapped_location))
                last_mapped_location = overlap_start + overlap_length - 1
            remaining_locations = active_range_start + active_range_length - 1 - last_mapped_location
            if remaining_locations > 0:
                new_location_ranges.append((last_mapped_location + 1, remaining_locations))
        mapped_ranges = sorted(new_location_ranges)

    return mapped_ranges


if __name__ == "__main__":
    main()
