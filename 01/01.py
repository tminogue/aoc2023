from common import deserialize_input_file

input_list = deserialize_input_file("01a_test_input.txt")

def find_digit(input_str: str, direction: int = 1) -> int:
    """
    :param input_str:
    :param direction: must be -1 or 1 to determine indexing direction
    :return:
    """
    # index is 0 if searching from left to right, -1 if searching from right to left
    search_index = direction * 0 if direction == 1 else direction

    if len(input_str) == 0:
        return None
    else:
        if input_str[search_index].isdigit():
            return int(input_str[search_index])
        elif direction == 1:
            # slice off first character and search from left to right
            return find_digit(input_str[1*direction:], direction=direction)
        elif direction == -1:
            # slice off last character and search from right to left
            return find_digit(input_str[:direction], direction=direction)

def run_part_1(input_list: list[str]) -> int:

    total_rows_value: int = 0
    for row in input_list:

        first_digit = find_digit(row, direction=1)
        second_digit = find_digit(row, direction=-1)

        # print(f"{first_digit}{second_digit}")

        row_value = 10 * first_digit + second_digit
        total_rows_value += row_value

    return total_rows_value



