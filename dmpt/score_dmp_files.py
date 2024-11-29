import datetime
import os
import pandas as pd
import re

from dmp_v1 import read_and_score_dmp_v1
from dmp_v2 import read_and_score_dmp_v2

from tools.find_version_number import find_version_number


def find_matching_docx(folder_path: str) -> str|None:
    """
    Searches for a .docx file in the given folder that matches the pattern:
    {some_number}-{some_letters}_v{number}.{number}-data-management-plan.docx
    
    Args:
        folder_path (str): The path to the folder to search in.
    
    Returns:
        str: Full path to the file if found, or None if no matching file exists.
    """
    # Define the regex pattern
    pattern = re.compile(r"\d+-[a-zA-Z]+_v\d+\.\d+-data-management-plan\.docx$")
    
    # Walk through the directory
    for root, _, files in os.walk(folder_path):
        for file in files:
            if pattern.match(file):
                return os.path.join(root, file)
    
    return None


def create_dmp_dictionary(df: pd.DataFrame) -> dict[int, str]:
    """
    Creates a dictionary mapping project numbers to document paths.
    This function iterates over the project numbers in the given DataFrame,
    constructs a source folder path for each project, and attempts to find
    a matching .docx file in that folder. If a matching file is found, it is
    added to the dictionary with the project number as the key.

    Args:
        df (pd.DataFrame): A DataFrame containing a column 'ProjectNumber' with project numbers.
    Returns:
        dict[int, str]: A dictionary where the keys are project numbers and the values are paths to the matching .docx files.
    """

    suffix = "A. Contractual items"
    dmp = dict()
    for project_number in df.ProjectNumber:
        def round_down_to_500(number: int) -> int:
            return number - (number % 500)

        number = int(project_number)

        # Define the source directory you want to copy
        source_folder = f"n:\\Projects\\{round_down_to_500(number)}\\{number}\\{suffix}"
        # Define the destination directory where you want the folder to be copied

        temp = find_matching_docx(source_folder)
        if temp is not None:
            dmp[number] = temp
        return dmp
    

def date_modified(dmp: dict[int, str]) -> dict[int, datetime.datetime]:
    """
    Given a dictionary of project numbers and file paths, returns a dictionary
    where the keys are the project numbers and the values are the last modified
    dates of the corresponding files.

    Args:
        dmp (dict[int, str]): A dictionary where keys are project numbers and 
                              values are file paths.
    Returns:
        dict[int, datetime.datetime]: A dictionary where keys are project numbers
                                      and values are the last modified dates of 
                                      the corresponding files.
    """
    dmp_date_modified = {}
    for project_number, file_path in dmp.items():
        dmp_date_modified[project_number] = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    return dmp_date_modified


def read_and_score_dmps(dmp: dict[int, str]) -> dict[int, tuple[float, float, float]]:
    """
    Reads and scores Data Management Plans (DMPs) from given file paths.
    
    Args:
    dmp (dict[int, str]): A dictionary where keys are project numbers (int) and values are file paths (str) to the DMP files.

    Returns:
    pd.DataFrame: A DataFrame containing the project numbers, total scores, individual scores, and the date modified for each DMP.
    """
    
    dmp_scores = dict()
    for project_number, file_path in dmp.items():
        major, minor = find_version_number(file_path)
        match major:
            case(1):
                dmp_scores[project_number] = read_and_score_dmp_v1(file_path)
            case(2):
                dmp_scores[project_number] = read_and_score_dmp_v2(file_path)
    return dmp_scores

    

def create_dmp_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame containing DMP (Data Management Plan) scores and modification dates.
    This function processes the input DataFrame to generate a dictionary of DMPs, scores them,
    and retrieves their last modification dates. The results are then compiled into a new DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing DMP data.
    Returns:
        pd.DataFrame: A DataFrame with the following columns:
            - 'project_number': The project numbers.
            - 'total_score': The total scores for each project.
            - 'score1': The first individual score for each project.
            - 'score2': The second individual score for each project.
            - 'date_modified': The modification dates for each project.
    """

    dmp = create_dmp_dictionary(df)
    dmp_scores = read_and_score_dmps(dmp)
    dmp_date_modified = date_modified(dmp)

    # put the results in a dataframe
    # Create the dataframe
    data = {
        'ProjectNumber': list(dmp_scores.keys()),
        'total_score': [scores[0] for scores in dmp_scores.values()],
        'score1': [scores[1] for scores in dmp_scores.values()],
        'score2': [scores[2] for scores in dmp_scores.values()],
        'date_modified': [dt for dt in dmp_date_modified.values()]
    }

    return pd.DataFrame(data)

    