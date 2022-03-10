import os

def absolute_from_rel_file_path(relative_path: str) -> str:
    """
    Given a path relative to this file,
    returns the absolute path.

    :param relative_path: The path relative to this file.
    :return: The absolute path.
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, relative_path)
