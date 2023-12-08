from collections import Counter

from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("07a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("07a_puzzle_input.txt")

part2_input_list_test = part1_input_list_test
part2_input_list_puzzle = part1_input_list_puzzle

CARD_RANKS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CARD_RANKS_JOKER = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

# hand value rank determined by counts of most common, second most common
HAND_VALUES = {
    (5, 0): 6,  # five of a kind
    (4, 1): 5,  # four of a kind
    (3, 2): 4,  # full_house
    (3, 1): 3,  # three of a kind
    (2, 2): 2,  # two pair
    (2, 1): 1,  # one pair
    (1, 1): 0,  # high card
}


def get_hand_value(hand: list, bid: int) -> tuple[int, list[int], int]:
    """
    # hand value rank determined by counts of most common, second most common
    # returns tuple of hand value rank, a list of sorted hand tuples, bid
    """
    hand_counter = Counter(hand)
    # sort the hand by count, then by card value and return a list of tuples, best cards first
    sorted_hand_tuples = sorted(
        hand_counter.items(), key=lambda x: (x[1], x[0]), reverse=True
    )

    # get the counts of the most common cards, only the top two counts are needed to rank the hands
    # per the HAND_VALUES dict above
    first_card_count = sorted_hand_tuples[0][1]
    second_card_count = 0
    if len(sorted_hand_tuples) > 1:
        second_card_count = sorted_hand_tuples[1][1]

    # tuple of the top two card counts will determine the hand rank from HAND_VALUES dict
    # first value returned below
    top_card_counts = (first_card_count, second_card_count)

    return HAND_VALUES[top_card_counts], hand, bid


def get_hand_value_with_joker(hand: list, bid: int) -> tuple[int, list[int], int]:
    """
    # hand value rank determined by counts of most common, second most common
    # returns tuple of hand value rank, a list of sorted hand tuples, bid
    """
    hand_counter = Counter(hand)
    # pop the joker from the counter so it doesn't figure in the hand value calculation
    # and grab its count to add to the count of the best card
    joker_card_count = hand_counter.pop(1, None)

    # if there are only jokers, return a five of a kind with all Joker values
    # since the jokers will be the lowest rank of 5 of a kind
    if joker_card_count == 5:
        return 6, [1, 1, 1, 1, 1], bid

    # sort the hand by count, then by card value and return a list of tuples, best cards first
    sorted_hand_tuples = sorted(
        hand_counter.items(), key=lambda x: (x[1], x[0]), reverse=True
    )

    # get the counts of the most common cards, only the top two counts are needed to rank the hands
    # per the HAND_VALUES dict above
    first_card_value, first_card_count = (
        sorted_hand_tuples[0][0],
        sorted_hand_tuples[0][1],
    )
    second_card_count = 0
    if len(sorted_hand_tuples) > 1:
        second_card_count = sorted_hand_tuples[1][1]

    # now update the hand counter after joker is popped
    # incrementing the best card count with the joker card count
    # and resort the hand tuples to determine
    if joker_card_count:
        hand_counter[first_card_value] += joker_card_count
        sorted_hand_tuples = sorted(
            hand_counter.items(), key=lambda x: (x[1], x[0]), reverse=True
        )
        first_card_count = sorted_hand_tuples[0][1]
        second_card_count = 0
        if len(sorted_hand_tuples) > 1:
            second_card_count = sorted_hand_tuples[1][1]

    # tuple of the top two card counts will determine the hand rank from HAND_VALUES dict
    # first value returned below
    top_card_counts = (first_card_count, second_card_count)

    return HAND_VALUES[top_card_counts], hand, bid


# determine individual hand values (counters)
# rank high hand value to low (order by max count)
# compare hands with same value, rank within same value, comparing card values


def run_part_1(input_list: list) -> int:
    """
    # hand value rank determined by counts of most common, second most common
    # returns tuple of hand value rank, a list of sorted hand tuples, bid
    """
    hands_list = []
    for row in input_list:
        hand_bid = [row_list for row_list in row.split()]
        hand_letters, bid = list(hand_bid[0]), int(hand_bid[1])
        hand_numbers = [CARD_RANKS[card] for card in hand_letters]
        hands_list.append(get_hand_value(hand_numbers, bid))

    # print(hands_list)

    # sort list in place by first element in tuple, then by second, then by third
    # hand value, card 1 value, card 2 value
    # break ties with first value of card in list
    ranked_hands = sorted(
        hands_list,
        key=lambda x: (x[0], x[1]),
        reverse=False,
    )

    total_value = 0
    for index, hand in enumerate(ranked_hands):
        # bid is last element in tuple, index is zero based
        # ranked hands is sorted lowest to highest
        total_value += hand[2] * (index + 1)

    return total_value


def run_part_2(input_list: list) -> int:
    """
    # hand value rank determined by counts of most common, second most common
    # returns tuple of hand value rank, a list of sorted hand tuples, bid
    """
    hands_list = []
    for row in input_list:
        hand_bid = [row_list for row_list in row.split()]
        hand_letters, bid = list(hand_bid[0]), int(hand_bid[1])
        hand_numbers = [CARD_RANKS_JOKER[card] for card in hand_letters]
        hands_list.append(get_hand_value_with_joker(hand_numbers, bid))

    # print(hands_list)

    # sort list in place by first element in tuple, then by second, then by third
    # hand value, card 1 value, card 2 value
    # break ties with first value of card in list
    ranked_hands = sorted(
        hands_list,
        key=lambda x: (x[0], x[1]),
        reverse=False,
    )

    total_value = 0
    for index, hand in enumerate(ranked_hands):
        # bid is last element in tuple, index is zero based
        # ranked hands is sorted lowest to highest
        total_value += hand[2] * (index + 1)

    return total_value


print("Part 1:")
print(f"  Test input yields: {run_part_1(part1_input_list_test)}")
print(f"  Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")

print("\nPart 2:")
print(f"  Test input yields: {run_part_2(part2_input_list_test)}")
print(f"  Puzzle input yields: {run_part_2(part2_input_list_puzzle)}")


# for i, h in enumerate(ranked_hands):
#     print(f"{i+1},{h[2]},{(i+1)*h[2]}, {h}")
# print(total_value)
