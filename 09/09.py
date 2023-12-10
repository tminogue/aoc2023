from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("09a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("09a_puzzle_input.txt")

part2_input_list_test = part1_input_list_test
part2_input_list_puzzle = part1_input_list_puzzle


def get_series_lists(input_list: list[str]) -> list[list[int]]:
    series_list = []
    for row in input_list:
        series_list.append([int(n) for n in row.split()])

    return series_list

def get_series_diffs(series: list[int]) -> list[int]:
    diffs = []
    for i in range(1, len(series)):
        diffs.append(series[i] - series[i-1])
    return diffs

def run_part_1(input_list: list[str]) -> int:

    series_list = get_series_lists(input_list)
    # print(series_list); exit()

    series_next_values = []

    for series in series_list:
        print("---"*5)
        series_diffs = [series]

        diffs = series
        while sum(diffs) != 0:
            diffs = get_series_diffs(diffs)
            series_diffs.append(diffs)
            print(diffs)

        previous_series_diff = 0
        while len(series_diffs) > 0:
            current_series = series_diffs.pop()
            current_series.append(current_series[-1] + previous_series_diff)
            previous_series_diff = current_series[-1]

        series_next_value = previous_series_diff
        print(series_next_value)
        series_next_values.append(series_next_value)

    return sum(series_next_values)


def run_part_2(input_list: list[str]) -> int:

    series_list = get_series_lists(input_list)
    # print(series_list); exit()

    series_next_values = []

    for series in series_list:
        print("---"*5)
        series_diffs = [series]

        diffs = series
        while sum(diffs) != 0:
            diffs = get_series_diffs(diffs)
            series_diffs.append(diffs)
            # print(diffs)

        previous_series_diff = 0
        while len(series_diffs) > 0:
            current_series = series_diffs.pop()
            current_series = [current_series[0] - previous_series_diff] + current_series
            previous_series_diff = current_series[0]

        series_next_value = previous_series_diff
        print(series_next_value)
        series_next_values.append(series_next_value)

    return sum(series_next_values)





print("Part 1:")
print(f"  Test input yields: {run_part_1(part1_input_list_test)}")
# print(f"  Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")
#
# print("\nPart 2:")
print(f"  Test input yields: {run_part_2(part2_input_list_test)}")
print(f"  Puzzle input yields: {run_part_2(part2_input_list_puzzle)}")