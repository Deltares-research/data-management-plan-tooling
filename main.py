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

    # Write to database
    write_projects_to_db(df)


if __name__ == "__main__":
    main()
