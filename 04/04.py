import argparse
from collections import namedtuple

Scratchcard = namedtuple("Scratchcard", ["card_id", "winning_numbers", "scratched_numbers"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    input_lines = [parse_scratchcard(line.strip()) for line in open(args.input_file_path)]
    return input_lines


def parse_scratchcard(input_line):
    card_id_string, winning_and_scratched_numbers_string = input_line.strip().split(":")
    winning_numbers_string, scratched_numbers_string = winning_and_scratched_numbers_string.split("|")
    card_id = int(card_id_string[4:].strip())
    return Scratchcard(card_id, {int(x) for x in winning_numbers_string.strip().split(' ') if len(x) > 0},
                                {int(x) for x in scratched_numbers_string.strip().split(' ') if len(x) > 0})


def main():
    scratchcards = read_input()

    part_1_score = 0
    for sc in scratchcards:
        num_matches = count_scratchcard_matches(sc)
        if num_matches > 0:
            part_1_score += pow(2, num_matches - 1)
    print(f"Part 1: {part_1_score}")
    print(f"Part 2: {get_scratchcard_scores(scratchcards)}")


def count_scratchcard_matches(sc):
    return sum(1 if sw == sx else 0 for sw in sc.scratched_numbers for sx in sc.winning_numbers)


# This is really computationally expensive. A more efficient method would be to count the number of each pending card...
# instead of physically copying each card many times and calculating them individually
def get_scratchcard_scores(scratchcards):
    used_scratchcard_count = 0
    scratchcard_pile = scratchcards.copy()
    while len(scratchcard_pile) > 0:
        used_scratchcard_count += len(scratchcard_pile)
        new_scratchcards = []
        for sc in scratchcard_pile:
            for i in range(sc.card_id, sc.card_id + count_scratchcard_matches(sc)):
                new_scratchcards.append(scratchcards[i])
        scratchcard_pile = new_scratchcards
    return used_scratchcard_count


if __name__ == "__main__":
    main()
