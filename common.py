def deserialize_input_file(log_file_path: str) -> list[str]:
    """
    Read in a file with rows of text and return a list strings for each row
    """
    input_file = open(log_file_path)
    return input_file.read().splitlines()
