import argparse
from collections import namedtuple, Counter

HandAndBet = namedtuple("HandAndBet", ["hand", "bet_value"])
Hand = namedtuple("Hand", ["hand_type", "hand_value"])

FiveOfaKind = 106
FourOfaKind = 105
FullHouse = 104
ThreeOfaKind = 103
TwoPair = 102
OnePair = 101
HighCard = 100

Ace = 14
King = 13
Queen = 12
Jack = 11
Ten = 10
Joker = 1


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    hands = [parse_input_line(line.strip()) for line in open(args.input_file_path)]
    return hands


def parse_input_line(line):
    hand_string, bet_string = line.split(" ")
    return HandAndBet(hand_string, int(bet_string))


def main():
    hands = read_input()

    part_1_winnings = sum((rank + 1) * hand.bet_value
                          for rank, hand in enumerate(sorted(hands, key=lambda hab: get_hand_value(hab.hand))))
    print(f"Part 1: {part_1_winnings}")

    part_2_winnings = sum((rank + 1) * hand.bet_value
                          for rank, hand in enumerate(sorted(hands, key=lambda hab: get_hand_value(hab.hand, True))))
    print(f"Part 2: {part_2_winnings}")


def get_hand_value(hand_string, joker_rule=False):
    card_values = [get_card_value(card, joker_rule) for card in hand_string]
    card_counts = Counter(card_values)
    num_pairs = sum(1 if c == 2 else 0 for _, c in card_counts.items())

    if any(c == 5 for _, c in card_counts.items()):
        return Hand(FiveOfaKind, card_values)
    if any(c == 4 for _, c in card_counts.items()):
        if card_counts[Joker] > 0:
            return Hand(FiveOfaKind, card_values)
        return Hand(FourOfaKind, card_values)
    if any(c == 3 for _, c in card_counts.items()):
        if num_pairs == 1:
            if card_counts[Joker] > 0:
                return Hand(FiveOfaKind, card_values)
            return Hand(FullHouse, card_values)
        else:
            if card_counts[Joker] > 0:
                return Hand(FourOfaKind, card_values)
            return Hand(ThreeOfaKind, card_values)
    if num_pairs == 2:
        if card_counts[Joker] == 1:
            return Hand(FullHouse, card_values)
        if card_counts[Joker] == 2:
            return Hand(FourOfaKind, card_values)
        return Hand(TwoPair, card_values)
    if num_pairs == 1:
        if card_counts[Joker] > 0:
            return Hand(ThreeOfaKind, card_values)
        return Hand(OnePair, card_values)
    if card_counts[Joker] == 1:
        return Hand(OnePair, card_values)
    return Hand(HighCard, card_values)


def get_card_value(card, joker_rule):
    if card == "A":
        return Ace
    if card == "K":
        return King
    if card == "Q":
        return Queen
    if card == "J":
        if joker_rule:
            return Joker
        else:
            return Jack
    if card == "T":
        return Ten
    return int(card)


if __name__ == "__main__":
    main()
