import re


def find_version_number(filename: str) -> tuple[str, str]:
    version_pattern = r'v(?P<major>\d+)\.(?P<minor>\d+)'
    match_obj = re.search(version_pattern, filename)
    if match_obj is None:
        return None, None
    return match_obj['major'], match_obj['minor']