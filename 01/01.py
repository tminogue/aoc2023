from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("01a_test_input.txt")
part2_input_list_test = deserialize_input_file("01b_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("01a_puzzle_input.txt")
part2_input_list_puzzle = deserialize_input_file("01b_puzzle_input.txt")


def find_digit_part_1(input_str: str, direction: int = 1) -> int:
    """
    direction: must be -1 or 1 to determine indexing direction
    """
    # index is 0 if searching from left to right, -1 if searching from right to left
    search_index = direction * 0 if direction == 1 else direction

    if len(input_str) == 0:
        print("Nothing to search")
        return None
    else:
        if input_str[search_index].isdigit():
            return int(input_str[search_index])
        elif direction == 1:
            # slice off first character and search from left to right
            return find_digit_part_1(input_str[direction:], direction=direction)
        elif direction == -1:
            # slice off last character and search from right to left
            return find_digit_part_1(input_str[:direction], direction=direction)
        else:
            raise ValueError(f"Couldn't find a damn digit in {input_str}")


def run_part_1(input_list: list[str]) -> int:
    total_rows_value: int = 0

    for row in input_list:
        first_digit = find_digit_part_1(row, direction=1)
        second_digit = find_digit_part_1(row, direction=-1)
        # print(f"{first_digit}{second_digit}")

        # math and increment running total
        row_value = 10 * first_digit + second_digit
        total_rows_value += row_value

    return total_rows_value


WORD_TO_NUMBER_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def run_part_2_failed_attempt(input_list: list[str]) -> int:
    """
    This failed because it didn't handle the case of overlapping words like "eightwo"
    """
    transformed_list = []
    # convert all words to numbers for each line in input_list
    for row in input_list:
        transformed_row = row
        low_index = 0
        high_index = len(row) - 1
        for k in WORD_TO_NUMBER_MAP.keys():
            if k in row:
                # print(f"Found {k} in {row}")
                transformed_row = transformed_row.replace(k, str(WORD_TO_NUMBER_MAP[k]))
        print(row, transformed_row)
        transformed_list.append(transformed_row)

    # run the same logic as part 1 on transformed_list
    return run_part_1(transformed_list)


def find_digit_part_2(input_str: str, direction: int = 1) -> int:
    """
    direction: must be -1 or 1 to determine indexing direction
    """
    # index is 0 if searching from left to right, -1 if searching from right to left
    search_index = direction * 0 if direction == 1 else direction

    if len(input_str) == 0:
        print("Nothing to search")
        return None
    else:
        if input_str[search_index].isdigit():
            return int(input_str[search_index])
        elif direction == 1:
            # first check if the string starts with a number word and return that number
            for k in WORD_TO_NUMBER_MAP.keys():
                if input_str.startswith(k):
                    # print(f"Found {k} in {input_str}")
                    return WORD_TO_NUMBER_MAP[k]
            # otherwise, slice off first character and search from left to right
            return find_digit_part_2(input_str[direction:], direction=direction)
        elif direction == -1:
            # first check if the string ends with a number word and return that number
            for k in WORD_TO_NUMBER_MAP.keys():
                if input_str.endswith(k):
                    # print(f"Found {k} in {input_str}")
                    return WORD_TO_NUMBER_MAP[k]
            # otherwise, slice off last character and search from right to left
            return find_digit_part_2(input_str[:direction], direction=direction)
        else:
            raise ValueError(f"Couldn't find a damn digit in {input_str}")


def run_part_2(input_list: list[str]) -> int:
    total_rows_value: int = 0

    for row in input_list:
        first_digit = find_digit_part_2(row, direction=1)
        second_digit = find_digit_part_2(row, direction=-1)
        # print(f"{first_digit}{second_digit}")

        # math and increment running total
        row_value = 10 * first_digit + second_digit
        total_rows_value += row_value

    return total_rows_value


print("Part 1:")
# print(run_part_1(part1_input_list_test))
print(run_part_1(part1_input_list_puzzle))
print("\nPart 2:")
# print(run_part_2(part2_input_list_test))
print(run_part_2(part2_input_list_puzzle))
