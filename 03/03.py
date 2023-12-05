from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("03a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("03a_puzzle_input.txt")

part2_input_list_test = part1_input_list_test
part2_input_list_puzzle = part1_input_list_puzzle


def is_symbol(char: str) -> bool:
    return not (char.isdigit() or char == ".")


def build_matrix(input_list: list):
    """
    returns a 2-d array with a tuple of:
        - the character at the coordinate
        - if that character is a digit
        - if that character is a symbol
        - if that character is a star (*)
    """
    num_rows = len(input_list)
    num_cols = len(input_list[0])
    matrix = [[None for i in range(num_cols)] for j in range(num_rows)]

    for y in range(num_rows):
        for x in range(num_cols):
            coordinate_value = input_list[y][x]
            matrix[y][x] = (
                coordinate_value,
                coordinate_value.isdigit(),
                is_symbol(coordinate_value),
                coordinate_value == "*"
            )

    return matrix


def get_valid_numbers_in_rows(matrix: list) -> list[dict]:
    """
    returns a list of dicts where each dict key is the row number and the value is a list of numbers found in that row
    """
    valid_numbers = []

    last_row_index = len(matrix) - 1
    last_col_index = len(matrix[0]) - 1

    y = 0
    while y <= last_row_index:
        x = 0
        all_row_numbers_list = []
        valid_row_numbers_list = []
        current_number_chars = []

        while x <= last_col_index:
            # check if value at current coordinate is a digit
            current_value = matrix[y][x]
            if current_value[1]:
                # if it is a digit, add it to current list of digits
                current_number_chars.append(current_value[0])
                # if the current column is the last column, add the concatenated number to current number list
                if x == last_col_index:
                    all_row_numbers_list.append("".join(current_number_chars))
                    # decrement search end index in this case since it is the last column
                    end_index = x
                    start_index = max(0, x - len(current_number_chars))
                    if has_adjacent_symbol(y, start_index, end_index, matrix):
                        valid_row_numbers_list.append("".join(current_number_chars))

                x += 1

            else:
                # if there are values in the current number list, add the concatenated number
                # to the row number list, and clear the current number list and increment column counter
                if current_number_chars:
                    all_row_numbers_list.append("".join(current_number_chars))
                    end_index = x
                    start_index = max(0, x - len(current_number_chars) - 1)
                    if has_adjacent_symbol(y, start_index, end_index, matrix):
                        valid_row_numbers_list.append("".join(current_number_chars))

                current_number_chars = []
                x += 1

        # add the list of numbers in row to overall list and increment row counter
        # print(f"Line {y}: Numbers = {all_row_numbers_list}, Valid = {valid_row_numbers_list}")
        valid_numbers.extend(valid_row_numbers_list)
        y += 1

    return valid_numbers


def has_adjacent_symbol(y_index, x_start_index, x_end_index, matrix: list) -> bool:
    last_row_index = len(matrix) - 1
    # x_start_index = min(0, x_start_index)
    # x_end_index = max(last_col_index, x_end_index)

    adjacency_checks = []
    # check adjacency
    #   check one position to either side
    #   don't check beyond left or right edges

    try:
        adjacency_checks.append(matrix[y_index][x_start_index][2])
    except:
        pass

    # try current rowone character to the right of end, unless the end index is right of the edge, bound to last column
    try:
        adjacency_checks.append(matrix[y_index][x_end_index][2])
    except:
        pass

    # check rows above and below
    if y_index > 0:
        # if not the first row, check row above
        row_above_coords = []
        for i in range(x_start_index, x_end_index + 1):
            try:
                row_above_coords.append(matrix[y_index - 1][i][2])
            except:
                continue

        adjacency_checks.extend(row_above_coords)

    if y_index < last_row_index:
        # if not the first row, check row above
        row_below_coords = []
        for i in range(x_start_index, x_end_index + 1):
            try:
                row_below_coords.append(matrix[y_index + 1][i][2])
            except:
                continue

        adjacency_checks.extend(row_below_coords)

    return any(adjacency_checks)


def get_all_number_digits(y: int, x_start:int, matrix:list) -> str:
    """
    traverse all characters in row and return the complete number string
    """
    last_col_index = len(matrix[0]) - 1

    # first add the first digit found to list of digits
    digits = [matrix[y][x_start][0]]

    # add all digits to the left to the start of the list
    x = x_start - 1
    while x >= 0:
        current_value = matrix[y][x]
        if current_value[1]:
            digits = [current_value[0]] + digits
            x -= 1
        else:
            break

    # add all digits to the right to the end of the list
    x = x_start + 1
    while x <= last_col_index:
        current_value = matrix[y][x]
        if current_value[1]:
            digits.append(current_value[0])
            x += 1
        else:
            break

    return "".join(digits)


def get_star_adjacent_numbers(matrix: list):
    last_row_index = len(matrix) - 1
    last_col_index = len(matrix[0]) - 1
    adjacent_numbers_list: list[list] = []

    # iterate over matrix to find stars, and test for adjacent numbers
    y = 0
    while y <= last_row_index:
        x = 0
        while x <= last_col_index:
            current_coordinates = matrix[y][x]
            # keep track of numbers found in a set, in order to not duplicate
            current_adjacent_numbers = set()
            # fourth [3] element of tuple is boolean for star char
            # second [1] element of tuple is boolean for digit char
            if current_coordinates[3]:
                # look left
                if x > 0:
                    left_pos = matrix[y][x-1]
                    if left_pos[1]:
                        # current_adjacent_numbers.append(left_pos)
                        number = get_all_number_digits(y, x-1, matrix)
                        current_adjacent_numbers.add(number)

                # look right
                if x < last_row_index:
                    right_pos = matrix[y][x+1]
                    if right_pos[1]:
                        number = get_all_number_digits(y, x+1, matrix)
                        current_adjacent_numbers.add(number)

                # look up-left, up, up-right
                if y > 0:
                    # up
                    up_pos = matrix[y-1][x]
                    if up_pos[1]:
                        number = get_all_number_digits(y-1,x,matrix)
                        current_adjacent_numbers.add(number)

                    # up-left
                    up_left_pos = matrix[y - 1][x - 1]
                    if x > 0:
                        if up_left_pos[1]:
                            number = get_all_number_digits(y - 1, x -1 , matrix)
                            current_adjacent_numbers.add(number)
                    # up-right
                    up_right_pos = matrix[y - 1][x + 1]
                    if x < last_row_index:
                        if up_right_pos[1]:
                            number = get_all_number_digits(y - 1, x + 1, matrix)
                            current_adjacent_numbers.add(number)

                # look down-left, down, down_right
                if y < last_row_index:
                    # down
                    down_pos = matrix[y + 1][x]
                    if down_pos[1]:
                        number = get_all_number_digits(y + 1, x, matrix)
                        current_adjacent_numbers.add(number)

                    # down-left
                    down_left_pos = matrix[y + 1][x - 1]
                    if x > 0:
                        if down_left_pos[1]:
                            number = get_all_number_digits(y + 1, x - 1, matrix)
                            current_adjacent_numbers.add(number)
                    # down-right
                    down_right_pos = matrix[y + 1][x + 1]
                    if x < last_row_index:
                        if down_right_pos[1]:
                            number = get_all_number_digits(y + 1, x + 1, matrix)
                            current_adjacent_numbers.add(number)

            if current_adjacent_numbers:
                # add each list of adjacent numbers to overall list
                # cast set to list to allow iteration on result
                adjacent_numbers_list.append(list(current_adjacent_numbers))

            x += 1
        y += 1

    return adjacent_numbers_list



def run_part_1(input_list: list[str]) -> int:
    matrix = build_matrix(input_list)
    valid_numbers = get_valid_numbers_in_rows(matrix)

    return sum([int(value) for value in valid_numbers])


def run_part_2(input_list: list[str]) -> int:
    gear_list = []

    matrix = build_matrix(input_list)
    gear_set_list = get_star_adjacent_numbers(matrix)

    for gear_set in gear_set_list:
        if len(gear_set) == 2:
            gear_ratio = int(gear_set[0]) * int(gear_set[1])
            gear_list.append(gear_ratio)

    return sum([ratio for ratio in gear_list])


    pass


print("Part 1:")
print(f"  Test input yields: {run_part_1(part1_input_list_test)}")
print(f"  Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")

print("\nPart 2:")
print(f"  Test input yields: {run_part_2(part2_input_list_test)}")
print(f"  Puzzle input yields: {run_part_2(part2_input_list_puzzle)}")