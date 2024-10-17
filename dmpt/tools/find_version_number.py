import re


def find_version_number(filename: str) -> tuple[int, int]:
    """Find the version number of the filename. 
    The version number is expected to be in the format v{major}.{minor}.

    Args:
        filename (str): The name of the file

    Returns:
        tuple[int, int]: Tuple of major and minor version numbers
    """    
    version_pattern = r'v(?P<major>\d+)\.(?P<minor>\d+)'
    match_obj = re.search(version_pattern, filename)
    if match_obj is None:
        raise ValueError(f"No version number found in filename: {filename}")
    return int(match_obj['major']), int(match_obj['minor'])