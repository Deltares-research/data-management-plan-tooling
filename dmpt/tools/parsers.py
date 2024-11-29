import re


def text_is_not_default(text: str, default_text: str = "Click here to enter text") -> bool:
    if default_text in text:
        return False
    return True


def parse_checkboxes(text) -> dict[str, bool]:
    """
    Parses a given text to determine the state of 'Yes' and 'No' checkboxes.
    
    The function looks for specific checkbox markers in the text:
    - "☒ Yes" indicates that the 'Yes' checkbox is checked.
    - "☐ Yes" indicates that the 'Yes' checkbox is unchecked.
    - "☒ No" indicates that the 'No' checkbox is checked.
    - "☐ No" indicates that the 'No' checkbox is unchecked.
    
    Args:
        text (str): The input text containing the checkbox markers.
    Returns:
        dict[str, bool]: A dictionary with keys 'Yes' and 'No', where the values are booleans
                         indicating whether the respective checkboxes are checked (True) or unchecked (False).
    """
    result = {"Yes": False, "No": False}

    # Normalize the text by removing invisible characters
    normalized_text = text.replace("\u200b", "").replace("\u2003", "").strip()

    # Check if 'Yes' or 'No' checkboxes are checked
    if "☒ Yes" in normalized_text:
        result["Yes"] = True
    elif "☐ Yes" in normalized_text:
        result["Yes"] = False

    if "☒ No" in normalized_text:
        result["No"] = True
    elif "☐ No" in normalized_text:
        result["No"] = False

    return result


def project_info(text:str) -> dict[str, str]:
    """
    Extracts project information from the given text.
    This function uses regular expressions to search for specific patterns
    in the input text and extracts the project leader and project number.
    
    Args:
        text (str): The input text containing project information.
    Returns:
        dict: A dictionary containing the extracted project information with keys:
            - 'Project leader': The name of the project leader.
            - 'Project number': The project number.
    """
    # Define the regex patterns
    leader_pattern = re.compile(r'Project lead:\s*(.*)')
    number_pattern = re.compile(r'Project number:\s*(\d+)')

    # Search for matches
    leader_match = leader_pattern.search(text)
    number_match = number_pattern.search(text)

    project_info = {}
    # Extract and store the matches in the dictionary
    if leader_match:
        project_info['Project leader'] = leader_match.group(1).strip()
    if number_match:
        project_info['Project number'] = number_match.group(1).strip()

    # Print the resulting dictionary
    return project_info