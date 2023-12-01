import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    input_lines = [line for line in open(args.input_file_path)]
    return input_lines


def main():
    document = read_input()
    print(f"Part 1: {sum(get_calibration_value(line) for line in document)}")
    print(f"Part 2: {sum(get_calibration_value(fix_digits(line)) for line in document)}")


def get_calibration_value(document):
    first_digit = None
    last_digit = None

    for c in document:
        c_ord = ord(c)
        if ord('0') <= c_ord <= ord('9'):
            c_digit = c_ord - ord('0')
            if first_digit is None:
                first_digit = c_digit
            last_digit = c_digit
            
    # Handle part 1 method being used on lines intended for part 2 that only have spelled-out digits
    if first_digit is None:
        first_digit = last_digit = 0

    return first_digit * 10 + last_digit


def fix_digits(s):
    # Repetition is the easiest way to handle overlapping characters (e.g. "eightwothree")
    return s.replace("one", 'one1one').replace("two", 'two2two').replace("three", 'three3three')\
        .replace("four", 'four4four').replace("five", 'five5five').replace("six", 'six6six')\
        .replace("seven", 'seven7seven').replace("eight", 'eight8eight').replace("nine", 'nine9nine')


if __name__ == "__main__":
    main()
