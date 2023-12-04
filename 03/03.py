import argparse
from collections import defaultdict
from functools import reduce


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    input_lines = [line.strip() for line in open(args.input_file_path)]
    return input_lines


def main():
    part_numbers, gear_ratios = get_schematic_details(read_input())
    print(f"Part 1: {sum(part_numbers)}")
    print(f"Part 2: {sum(gear_ratios)}")


def get_schematic_details(schematic_lines):
    part_numbers = []
    gears = defaultdict(lambda: [])

    for line_num, line_string in enumerate(schematic_lines):
        col = 0
        while col < len(line_string):
            if '0' <= line_string[col] <= '9':
                part_number = 0
                part_number_length = 0
                while col + part_number_length < len(line_string)\
                        and '0' <= line_string[col + part_number_length] <= '9':
                    part_number = part_number * 10 + int(line_string[col + part_number_length])
                    part_number_length += 1

                is_valid_part_number = False
                for y in range(max(0, line_num - 1), min(line_num + 2, len(schematic_lines))):
                    for x in range(max(0, col - 1), min(col + part_number_length + 1, len(schematic_lines[y]))):
                        if (schematic_lines[y][x] < '0' or schematic_lines[y][x] > '9')\
                                and schematic_lines[y][x] is not '.':
                            is_valid_part_number = True
                            if schematic_lines[y][x] is '*':
                                gears[(x, y)].append(part_number)

                if is_valid_part_number:
                    part_numbers.append(part_number)
                col += part_number_length
            else:
                col += 1

    gear_ratios = [reduce(lambda a, b: a * b, part_number_list)
                   for part_number_list in gears.values() if len(part_number_list) > 1]
    return part_numbers, gear_ratios


if __name__ == "__main__":
    main()
