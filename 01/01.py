from common import deserialize_input_file

part1_input_list = deserialize_input_file("01a_test_input.txt")
part2_input_list = deserialize_input_file("01b_test_input.txt")


def find_digit(input_str: str, direction: int = 1) -> int:
    """
    :param input_str:
    :param direction: must be -1 or 1 to determine indexing direction
    :return:
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
            return find_digit(input_str[direction:], direction=direction)
        elif direction == -1:
            # slice off last character and search from right to left
            return find_digit(input_str[:direction], direction=direction)
        else:
            raise ValueError(f"Couldn't find a damn digit in {input_str}")

def run_part_1(input_list: list[str]) -> int:

    total_rows_value: int = 0

    for row in input_list:
        first_digit = find_digit(row, direction=1)
        second_digit = find_digit(row, direction=-1)
        print(f"{first_digit}{second_digit}")

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


def run_part_2(input_list: list[str]) -> int:

    transformed_list = []
    # convert all words to numbers for each line in input_list
    for row in input_list:
        transformed_row = row
        for k in WORD_TO_NUMBER_MAP.keys():
            if k in row:
                # print(f"Found {k} in {row}")
                transformed_row = transformed_row.replace(k, str(WORD_TO_NUMBER_MAP[k]))
        print(row, transformed_row)
        transformed_list.append(transformed_row)

    # run the same logic as part 1 on transformed_list
    return run_part_1(transformed_list)