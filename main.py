import os
from dotenv import load_dotenv

from dmpt.get_fnc_data import call_dmp_api, process_api_data
from dmpt.score_dmp_files import create_dmp_dataframe

load_dotenv()

def main():

    # Get data from API
    projects = call_dmp_api()

    # Process the data
    df = process_api_data(projects)

    # Read and Scorethe DMPs
    dmps_table = create_dmp_dataframe(df)

    # make sure project numbers are integer type
    df.ProjectNumber = df.ProjectNumber.astype(int)
    dmps_table.ProjectNumber = dmps_table.ProjectNumber.astype(int)

    # Combine scoring results with project data on project number
    df_total = df.merge(
        dmps_table,
        left_on="ProjectNumber",
        right_on="ProjectNumber",
        how="outer",
        indicator=True,
    )

    output_folder = os.getenv("PATH_TO_DATA", "data")
    output_filename = os.getenv("OUTPUT_FILENAME ", "output.csv")
    df_total.to_csv(os.path.join(output_folder, output_filename), index=False, mode="w")


if __name__ == "__main__":
    main()
