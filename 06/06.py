import math
import re

from common import deserialize_input_file

part1_input_list_test = deserialize_input_file("06a_test_input.txt")
part1_input_list_puzzle = deserialize_input_file("06a_puzzle_input.txt")

part2_input_list_test = part1_input_list_test
part2_input_list_puzzle = part1_input_list_puzzle


race_times = [
    int(s) for s in re.split(" +", re.split(":", part1_input_list_test[0])[1]) if s
]
race_records = [
    int(s) for s in re.split(" +", re.split(":", part1_input_list_test[1])[1]) if s
]

races = [(race_times[i], race_records[i]) for i in range(len(race_times))]


def get_winning_count(race_time: int, race_record: int) -> int:
    """
    Distance traveled is speed * duration (running_time), and speed is fixed at the charging time (t)
    Race time is a constant (R)
    distance = speed * run_time = t * (R - t) = t*R - t**2
    Winning count will be the number of attempts less double the number of losers since the distance traveled
    is a symmetric parabolic function.

    """
    # number of attempts will be from 0 to race length
    num_attempts = race_time + 1
    losing_count = 0
    for t in range(0, num_attempts):
        distance = t * (race_time - t)
        # ties don't count as wins
        if distance <= race_record:
            losing_count += 1
        else:
            # exit loop as leftmost losers have been found
            break

    return num_attempts - (2 * losing_count)


def run_part_1(input_list):
    race_times = [int(s) for s in re.split(" +", re.split(":", input_list[0])[1]) if s]
    race_records = [
        int(s) for s in re.split(" +", re.split(":", input_list[1])[1]) if s
    ]

    races = [(race_times[i], race_records[i]) for i in range(len(race_times))]

    winning_race_counts = []
    for race in races:
        race_time, race_record = race[0], race[1]
        winning_race_counts.append(get_winning_count(race_time, race_record))
    # print(winning_race_counts)

    return math.prod(winning_race_counts)


def run_part_2(input_list):
    race_time = int(input_list[0].split(":")[1].replace(" ", ""))
    race_record = int(input_list[1].split(":")[1].replace(" ", ""))

    return get_winning_count(race_time, race_record)


print("Part 1:")
print(f"  Test input yields: {run_part_1(part1_input_list_test)}")
print(f"  Puzzle input yields: {run_part_1(part1_input_list_puzzle)}")

print("\nPart 2:")
print(f"  Test input yields: {run_part_2(part2_input_list_test)}")
print(f"  Puzzle input yields: {run_part_2(part2_input_list_puzzle)}")
