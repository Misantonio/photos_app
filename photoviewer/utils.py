def read_file(file_path):
    """
    Read a file and return its content.
    """
    with open(file_path, "r") as file:
        content = file.read()
    return content