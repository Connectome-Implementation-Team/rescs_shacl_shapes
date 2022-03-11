import os

def absolute_from_rel_file_path(relative_path: str, file_location: str) -> str:
    """
    Given a path relative to file_location,
    returns the absolute path.

    :param relative_path: The path relative to the file_location param.
    :param file_location: The location of the file this method is called from.
    :return: The absolute path.
    """
    dirname = os.path.dirname(file_location)
    return os.path.join(dirname, relative_path)
