from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("02a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("02a_puzzle_input.txt")

# part2_input_list_test = deserialize_input_file("02b_test_input.txt")
# part2_input_list_puzzle = deserialize_input_file("02b_puzzle_input.txt")

CUBE_COUNTS = {"red": 12, "green": 13, "blue": 14}

def build_game_sets(game_list: list[str]):
    """
    Build a list of sets of colors for each game

    Example: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    """
    game_sets_dict: dict[dict] = {}

    for row in game_list:
        game_sets = []
        game, game_sets_str = row.split(": ")
        # game ="Game 1"
        # game_sets_str = "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"]

        for game_set in game_sets_str.split("; "):
            # game_set = "3 blue, 4 red""
            game_set_color_counts = []
            for set_color_count_string in game_set.split(", "):
                # set_color_count_string = '3 blue'
                split_count_and_color_str = set_color_count_string.split(" ")
                color = split_count_and_color_str[1]
                count = int(split_count_and_color_str[0])
                game_set_color_counts.append({color: count})
            game_sets.append(game_set_color_counts)

        game_sets_dict[game] = game_sets

    return game_sets_dict


def is_valid_game_set(game_set_cube_color_counts: list) -> bool:
    """
    tests if a game set within a game is valid
    """

    for color_count in game_set_cube_color_counts:
        for color, count in color_count.items():
            if count > CUBE_COUNTS[color]:
                return False
    return True

def is_valid_game(game_list: list) -> bool:
    """
    tests if an entire game is valid: all game sets are valid
    """
    return all(
        [
            is_valid_game_set(game_set) for game_set in game_list
        ]
    )


def run_part_1(input_list: list[str]):

    valid_games = []

    game_sets_dict = build_game_sets(input_list)

    for game, game_list in game_sets_dict.items():
        if is_valid_game(game_list):
            # print(f"{game}: {game_list} is valid")
            game_int = int(game.split(" ")[1])
            valid_games.append(game_int)

    return sum(valid_games)


# if __name__ == "__main__":
print("Part 1:")
print(f"Test input yields: {run_part_1(part1_input_list_test)}")
print(f"Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")

print("\nPart 2:")
# print(run_part_2(part2_input_list_test))
# print(run_part_2(part2_input_list_puzzle))
#     pass