import math
from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("08a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("08a_puzzle_input.txt")

part2_input_list_test = deserialize_input_file("08b_test_input.txt")
part2_input_list_puzzle = part1_input_list_puzzle

MOVE_MAP = {"L": 0, "R": 1}


def build_node_map(input_list: list[str]) -> dict[str, tuple[str, str]]:
    node_map = {}
    node_string_list = input_list[2:]
    for node_string in node_string_list:
        node_string_parts = node_string.split(" = ")
        node_name, node_neighbor_strings = node_string_parts[0], node_string_parts[
            1
        ].replace("(", "").replace(")", "").split(", ")
        node_neighbors = (node_neighbor_strings[0], node_neighbor_strings[1])
        node_map[node_name] = node_neighbors

    return node_map


def run_part_1(input_list: list[str]) -> int:
    moves = input_list[0]
    node_map = build_node_map(input_list)

    start = "AAA"
    destination = None

    hop_count = 0
    move_index = 0
    direction = MOVE_MAP[moves[move_index]]

    while destination != "ZZZ":
        hop_count += 1
        destination = node_map[start][direction]
        # print(start, destination)
        start = destination
        move_index += 1
        # reset the index to the start if we reach the end of the moves list
        if move_index >= len(moves):
            move_index = 0
        direction = MOVE_MAP[moves[move_index]]

    return hop_count


# def get_desination_node(node_map, current_node, direction):
#     return node_map[current_node][direction]
def run_part_2(input_list: list[str]) -> int:
    moves = input_list[0]
    node_map = build_node_map(input_list)

    start_nodes = [node for node in node_map.keys() if node[2] == "A"]

    hop_counts = []

    for start_node in start_nodes:
        dest_node = "..."

        hop_count = 0
        move_index = 0
        direction = MOVE_MAP[moves[move_index]]

        while dest_node[2] != "Z":
            hop_count += 1
            dest_node = node_map[start_node][direction]
            # print(start, destination)
            start_node = dest_node
            move_index += 1
            # reset the index to the start if we reach the end of the moves list
            if move_index >= len(moves):
                move_index = 0
            direction = MOVE_MAP[moves[move_index]]

        hop_counts.append(hop_count)
    print(hop_counts)

    math.lcm(*hop_counts)

    return math.lcm(*hop_counts)


print("Part 1:")
print(f"  Test input yields: {run_part_1(part1_input_list_test)}")
print(f"  Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")

print("\nPart 2:")
print(f"  Test input yields: {run_part_2(part2_input_list_test)}")
print(f"  Puzzle input yields: {run_part_2(part2_input_list_puzzle)}")
