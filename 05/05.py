from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("05a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("05a_puzzle_input.txt")

part2_input_list_test = part1_input_list_test
part2_input_list_puzzle = part1_input_list_puzzle


def parse_input_data(input_list: list[str]):
    # hack to handle end of file
    input_list = input_list + [""]
    # extract seed values into a list
    seed_values_str = input_list[0].split(": ")[1]
    seed_values_list = list(seed_values_str.split())
    # convert strings to ints
    seed_values_list = [int(val) for val in seed_values_list]

    mapping_dicts_dict = {}

    row_index = 2
    current_dict_key = None
    current_dict_values = []
    while row_index < len(input_list):
        # if first letter of row is not a digit, then the row has the key name
        if input_list[row_index] and input_list[row_index][0].isalpha():
            current_dict_key = input_list[row_index][:-1]
        # if first letter of row is a digit, then split the string and add to the values list
        elif input_list[row_index] and input_list[row_index][0].isdigit():
            current_value_str = input_list[row_index]
            current_value_list = list(current_value_str.split())
            current_value_list = [int(val) for val in current_value_list]
            current_dict_values.append(current_value_list)
        # otherwise, add the current map dictionary to the list
        # skip the row (empty line) and move on to next key or end of list
        else:
            mapping_dicts_dict[current_dict_key] = current_dict_values
            current_dict_key = None
            current_dict_values = []

        row_index += 1

    return seed_values_list, mapping_dicts_dict


def map_src_to_dst(source_list: list[int], map: list[list[int]]) -> list[int]:
    """
    for a list source integer value, determine its destination using a list of mapping ranges
    mapping range is list of [destination_start, source_start, range_length]
    """
    destination_list = []

    for source in source_list:
        # default case: if source not found in mapping ranges, then destination remains the same as source
        destination = source

        # check each range
        for map_range in map:
            destination_range_start, source_range_start, range_length = (
                map_range[0],
                map_range[1],
                map_range[2],
            )
            source_range_end = source_range_start + range_length
            if source_range_start <= source < source_range_end:
                offset = source - source_range_start
                destination = destination_range_start + offset
                # once the range is found, don't continue to look at other ranges
                break

        destination_list.append(destination)

    return destination_list


def run_part_1(input_list):
    input_data = parse_input_data(input_list)

    source_list, map_dict = input_data[0], input_data[1]
    # print(seed_list, map_src_to_dst(seed_list, map))

    map_list = [
        "seed-to-soil map",
        "soil-to-fertilizer map",
        "fertilizer-to-water map",
        "water-to-light map",
        "light-to-temperature map",
        "temperature-to-humidity map",
        "humidity-to-location map",
    ]

    # start with seed list
    destination_list = source_list
    # iterate through maps to get successive destinations
    for map in map_list:
        destination_list = map_src_to_dst(destination_list, map_dict[map])

    return min(destination_list)


def run_part_2(input_list):
    input_data = parse_input_data(input_list)

    map_list = [
        "seed-to-soil map",
        "soil-to-fertilizer map",
        "fertilizer-to-water map",
        "water-to-light map",
        "light-to-temperature map",
        "temperature-to-humidity map",
        "humidity-to-location map",
    ]

    source_list, map_dict = input_data[0], input_data[1]
    seed_ranges = []

    # create list of seed range tuples with seed start, end positions
    i = 0
    while i < len(source_list):
        range_start = source_list[i]
        range_length = source_list[i + 1]
        seed_ranges.append((range_start, range_start + range_length))
        i += 2

    # range with transformed values

    for map_key in map_list:
        # get current set of transformation ranges
        destination_ranges = map_dict[map_key]

        # iterate over seed range (start, end) tuples
        # each range is evaluated against each destination mapping range to determine any overlap
        # if there is an overlap, then create a new sub-range (start,end) and add it to list
        # once there are no overlaps, all positions have been fully transformed
        new_ranges = []
        while len(seed_ranges) > 0:
            # pop one range from list to evaluate
            seed_range_start, seed_range_end = seed_ranges.pop()

            # iterate through transformation mapping ranges to get successive destinations
            for destination_map in destination_ranges:
                destination_range_start, source_range_start, range_length = (
                    destination_map[0],
                    destination_map[1],
                    destination_map[2],
                )

                # test if current range has overlap with destination range
                overlap_start = max(seed_range_start, source_range_start)
                overlap_end = min(seed_range_end, source_range_start + range_length)

                if overlap_start < overlap_end:
                    # when ranges overlap, add the transformed sub-range to list of new ranges
                    # transformation offset of new start and end positions is the length of the overlap
                    new_ranges.append(
                        (
                            overlap_start
                            - source_range_start
                            + destination_range_start,
                            overlap_end - source_range_start + destination_range_start,
                        )
                    )
                    # handle non-overlapping subrange of current 'seed' range
                    if overlap_start > seed_range_start:
                        seed_ranges.append((overlap_start, seed_range_start))
                    if seed_range_end < overlap_end:
                        seed_ranges.append((overlap_end, seed_range_end))
                    break
                else:
                    # if there is no overlap, then add that range to the new 'seed' ranges to evaluate
                    new_ranges.append((seed_range_start, seed_range_end))

            seed_ranges = new_ranges

    return min(seed_ranges)[0]


print("Part 1:")
print(f"  Test input yields: {run_part_1(part1_input_list_test)}")
print(f"  Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")

print("\nPart 2:")
print(f"  Test input yields: {run_part_2(part2_input_list_test)}")
# print(f"  Puzzle input yields: {run_part_2(part2_input_list_puzzle)}")
