import os
from dotenv import load_dotenv
import pandas as pd

from dmpt.get_fnc_data import call_dmp_api, process_api_data
from dmpt.score_dmp_files import create_dmp_dataframe, create_dmp_dataframe_diff

load_dotenv()
OUTPUT_PROJECT_FILE = os.getenv("OUTPUT_PROJECT_FILE", "output.csv")
PATH_TO_DATA = os.getenv("PATH_FOLDER", "data")

def diff_run(df_total_old: pd.DataFrame) -> pd.DataFrame:
    # Get data from API
    projects = call_dmp_api()

    # Process the data
    df_api = process_api_data(projects)

    # Read and Scorethe DMPs
    df_scores = create_dmp_dataframe_diff(df_api, df_total_old)

    # make sure project numbers are integer type
    df_api.ProjectNumber = df_api.ProjectNumber.astype(int)
    df_scores.ProjectNumber = df_scores.ProjectNumber.astype(int)

    # Combine scoring results with project data on project number
    df_total = df_api.merge(
        df_scores,
        left_on="ProjectNumber",
        right_on="ProjectNumber",
        how="outer",
        indicator=True,
        )
    
    return df_total


def complete_run() -> pd.DataFrame: 
    # Get data from API
    projects = call_dmp_api()

    # Process the data
    df_api = process_api_data(projects)

    # Read and Scorethe DMPs
    df_scores = create_dmp_dataframe(df_api)

    # make sure project numbers are integer type
    df_api.ProjectNumber = df_api.ProjectNumber.astype(int)
    df_scores.ProjectNumber = df_scores.ProjectNumber.astype(int)

    # Combine scoring results with project data on project number
    df_total = df_api.merge(
        df_scores,
        left_on="ProjectNumber",
        right_on="ProjectNumber",
        how="outer",
        indicator=True,
        )
    
    return df_total


def run() -> None:
    if not os.path.exists(PATH_TO_DATA):
        os.makedirs(PATH_TO_DATA)  # Use makedirs for nested directories

    # read output file, if it exists
    if os.path.exists(os.path.join(PATH_TO_DATA, OUTPUT_PROJECT_FILE)):
        df_total_old = pd.read_csv(os.path.join("data", OUTPUT_PROJECT_FILE))
        df_total = diff_run(df_total_old)
    else:
        df_total = complete_run()

    df_total.to_csv(os.path.join("data", OUTPUT_PROJECT_FILE), index=False, mode="w")
    

