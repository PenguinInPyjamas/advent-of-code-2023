import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    patterns = [[line for line in pattern.strip().split("\n") if len(line.strip()) > 0]
                for pattern in "".join(open(args.input_file_path)).strip().split("\n\n")]
    return patterns


def main():
    patterns = read_input()
    print(f"Part 1: {sum(find_lines_of_symmetry(p)[0] for p in patterns)}")
    print(f"Part 2: {sum(find_line_of_symmetry_with_smudge(p) for p in patterns)}")


def find_lines_of_symmetry(pattern):
    symmetry_scores = []

    for y in range(1, len(pattern)):
        symmetry_inconsistency = False
        gap = 0
        while 0 <= y - 1 - gap and y + gap < len(pattern):
            if pattern[y + gap] != pattern[y - gap - 1]:
                symmetry_inconsistency = True
                break
            gap += 1
        if not symmetry_inconsistency:
            symmetry_scores.append(100 * y)

    for x in range(1, min(len(row) for row in pattern)):
        symmetry_inconsistency = False
        gap = 0
        while 0 <= x - 1 - gap and x + gap < min(len(row) for row in pattern):
            for row in pattern:
                if row[x + gap] != row[x - gap - 1]:
                    symmetry_inconsistency = True
                    break
            if symmetry_inconsistency:
                break
            gap += 1
        if not symmetry_inconsistency:
            symmetry_scores.append(x)

    return symmetry_scores


def find_line_of_symmetry_with_smudge(pattern):
    original_lines_of_symmetry = find_lines_of_symmetry(pattern)
    for y in range(len(pattern)):
        for x in range(min(len(row) for row in pattern)):
            if pattern[y][x] == ".":
                new_symbol = "#"
            elif pattern[y][x] == "#":
                new_symbol = "."
            else:
                raise Exception(f"Unknown symbol '{pattern[y][x]}' found in mirror pattern")
            new_lines_of_symmetry = find_lines_of_symmetry(pattern[:y]
                                                           + [pattern[y][:x] + new_symbol + pattern[y][x + 1:]]
                                                           + pattern[y + 1:])
            new_lines_of_symmetry = [x for x in new_lines_of_symmetry if x not in original_lines_of_symmetry]
            if len(new_lines_of_symmetry) == 1:
                return new_lines_of_symmetry[0]
    print("Error: No valid smudge could be found!")
    return 0


if __name__ == "__main__":
    main()
