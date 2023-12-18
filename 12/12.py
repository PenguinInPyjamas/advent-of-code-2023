import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    parsed_lines = [parse_input_line(line) for line in open(args.input_file_path)]
    return parsed_lines


def parse_input_line(line):
    spring_string, damaged_spring_counts_string = line.strip().split(" ")
    return spring_string, [int(x) for x in damaged_spring_counts_string.split(",")]


def main():
    spring_rows = read_input()
    print(f"Part 1: {sum(count_valid_spring_combinations(row) for row in spring_rows)}")
    print(f"Part 2: {sum(count_valid_spring_combinations(unfold_row(row)) for row in spring_rows)}")


def unfold_row(spring_info):
    spring_string, invalid_spring_counts = spring_info
    return "?".join([spring_string] * 5), invalid_spring_counts * 5


def count_valid_spring_combinations(spring_info, invalid_spring_count=0, cache=None):
    spring_string, invalid_spring_groups = spring_info

    if cache is None:
        cache = {}
    cache_index = f"{spring_string}|{invalid_spring_groups}|{invalid_spring_count}"
    if cache_index in cache:
        return cache[cache_index]

    if sum(1 if (c == '#' or c == '?') else 0 for c in spring_string)\
            < sum(invalid_spring_groups) - invalid_spring_count:
        return 0

    for i, spring_char in enumerate(spring_string):
        if spring_char == '#':
            if len(invalid_spring_groups) > 0:
                invalid_spring_count += 1
            else:
                return 0
        elif spring_char == '.':
            if invalid_spring_count == 0:
                continue
            elif invalid_spring_count != invalid_spring_groups[0]:
                return 0
            else:
                invalid_spring_count = 0
                invalid_spring_groups = invalid_spring_groups[1:]
        elif spring_char == '?':
            out = count_valid_spring_combinations(("#" + spring_string[i + 1:], invalid_spring_groups),
                                                  invalid_spring_count, cache) \
                   + count_valid_spring_combinations(("." + spring_string[i + 1:], invalid_spring_groups),
                                                     invalid_spring_count, cache)
            cache[cache_index] = out
            return out
        else:
            raise Exception(f"Unexpected character when reading spring info: '{spring_char}'")

    if len(invalid_spring_groups) == 0 and invalid_spring_count == 0:
        return 1
    elif len(invalid_spring_groups) == 1 and invalid_spring_groups[0] == invalid_spring_count:
        return 1
    else:
        return 0


if __name__ == "__main__":
    main()
