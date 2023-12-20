import argparse
from collections import namedtuple

Lens = namedtuple("Lens", ["label", "power"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    init_sequence = [command for command in "".join(open(args.input_file_path)).strip().split(",")]
    return init_sequence


def main():
    init_sequence = read_input()
    print(f"Part 1: {sum(holiday_hash(command) for command in init_sequence)}")
    print(f"Part 2: {get_focusing_power(init_sequence)}")


def holiday_hash(s):
    hash_value = 0
    for char in s:
        hash_value = ((hash_value + ord(char)) * 17) % 256
    return hash_value


def get_focusing_power(seq):
    boxes = [[] for _ in range(256)]
    for step in seq:
        if step[-1] == "-":
            label = step[:-1]
            box_num = holiday_hash(label)
            new_box = []
            for lens in boxes[box_num]:
                if lens.label != label:
                    new_box.append(lens)
            boxes[box_num] = new_box
        elif "=" in step:
            label, lens_power_string = step.split("=")
            box_num = holiday_hash(label)
            new_lens = Lens(label, int(lens_power_string))
            lens_already_in_box = False
            new_box = []
            for lens in boxes[box_num]:
                if lens.label == label:
                    lens_already_in_box = True
                    new_box.append(new_lens)
                else:
                    new_box.append(lens)
            if not lens_already_in_box:
                new_box.append(new_lens)
            boxes[box_num] = new_box
    focusing_power = 0
    for box_num, box in enumerate(boxes):
        for lens_num, lens in enumerate(box):
            focusing_power += (box_num + 1) * (lens_num + 1) * lens.power
    return focusing_power


if __name__ == "__main__":
    main()
