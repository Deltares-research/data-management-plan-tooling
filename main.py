from dmpt.database import init_db, write_projects_to_db
from dmpt.get_fnc_data import call_dmp_api, process_api_data
from dmpt.read_dmp import read_tables
from dmpt.score_dmp import score_projects


def main():
    # Initialize database
    init_db()

    # Get data from API
    projects = call_dmp_api()

    # Process the data
    df = process_api_data(projects)

    # Read the DMPs
    dmp_tables = read_tables(df)

    # Score the data
    scored_projects = score_projects(dmp_tables)

    # Combine scoring results with project data
    df_total = df.merge(
        scored_projects,
        left_on="project_id",
        right_index=True,
        how="outer",
        indicator=True,
    )

    # Write to database
    write_projects_to_db(df)


if __name__ == "__main__":
    main()
