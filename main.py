from dmpt.database import init_db, write_projects_to_db
from dmpt.get_fnc_data import call_dmp_api, process_api_data

from dmpt.score_dmp_files import create_dmp_table


def main():
    # Initialize database
    init_db()

    # Get data from API
    projects = call_dmp_api()

    # Process the data
    df = process_api_data(projects)

    # Read and Scorethe DMPs
    dmps_table = create_dmp_table(df)

    # Combine scoring results with project data
    df_total = df.merge(
        dmps_table,
        left_on="project_id",
        right_index=True,
        how="outer",
        indicator=True,
    )

    # Write to database
    write_projects_to_db(df_total)


if __name__ == "__main__":
    main()
