from common import deserialize_input_file
import collections

part1_input_list_test = deserialize_input_file("04a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("04a_puzzle_input.txt")

part2_input_list_test = part1_input_list_test
part2_input_list_puzzle = part1_input_list_puzzle

def extract_card_data(input_list: list[str]) -> dict[tuple[set[str],set[str]]]:

    card_data = {}
    for row in input_list:
        card_number, card_row_data =  row.split(": ")
        card_number_key = int(card_number.split()[1])
        winning_numbers_str, card_data_str = card_row_data.split(" | ")
        winning_numbers_set = set(winning_numbers_str.split())
        card_data_set = set(card_data_str.split(" "))
        card_data[card_number_key] = (winning_numbers_set, card_data_set)

    return card_data

def get_card_winner_counts(card_data: dict):
    card_winners_counts = {}
    for card, numbers in card_data.items():
        winning_numbers_set, card_numbers_set = numbers[0], numbers[1]
        card_match_count = len(winning_numbers_set.intersection(card_numbers_set))
        card_winners_counts[card] = card_match_count


    return card_winners_counts


def run_part_1(input_list: list) -> int:
    card_data = extract_card_data(input_list)
    card_winner_counts = get_card_winner_counts(card_data)
    card_winners_values = {}

    for card, count in card_winner_counts.items():
        if count > 0:
            card_match_value = 2 ** (count-1)
        else:
            card_match_value = 0
        card_winners_values[card] = card_match_value

    return sum([val for val in card_winners_values.values()])


def run_part_2(input_list: list) -> int:
    card_data = extract_card_data(input_list)
    card_winner_counts = get_card_winner_counts(card_data)
    # start with one copy of each card
    card_copies_values = {card: 1 for card in card_data.keys()}
    # card_copy_values = collections.Counter(card_data)
    for card, count in card_winner_counts.items():
        for i in range(1, count+1):
            if card + i <= max(card_winner_counts.keys()):
                next_card_count = card_copies_values[card + i]
                # each copy of current card earns a copy of the next cards
                card_copies_values[card+i] = next_card_count + card_copies_values[card]

    # print(card_copies_values)
    return (sum([val for val in card_copies_values.values()]))


print("Part 1:")
print(f"  Test input yields: {run_part_1(part1_input_list_test)}")
print(f"  Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")

print("\nPart 2:")
print(f"  Test input yields: {run_part_2(part2_input_list_test)}")
print(f"  Puzzle input yields: {run_part_2(part2_input_list_puzzle)}")

