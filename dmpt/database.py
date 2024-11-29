import sqlite3
from pathlib import Path

import pandas as pd


def init_db(db_path: str = "data/dmp_data.db") -> None:
    """Initialize the SQLite database with the required tables."""
    # Ensure the data directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            project_description TEXT,
            closed BOOLEAN,
            unit TEXT,
            responsible_department TEXT,
            responsible_department_description TEXT,
            project_type TEXT,
            project_type_description TEXT,
            financier TEXT,
            business_area TEXT,
            business_area_description TEXT,
            project_leader_number TEXT,
            project_leader_name TEXT,
            project_administrator_number TEXT,
            project_administrator_name TEXT,
            date_created TIMESTAMP,
            date_modified TIMESTAMP,
            date_start TIMESTAMP,
            date_end TIMESTAMP,
            date_closed TIMESTAMP,
            status_api TEXT,
            quote_status TEXT,
            dmp_score INTEGER,
            dmp_score_part_1 INTEGER,
            dmp_score_part_2 INTEGER
        )
    """
    )

    conn.commit()
    conn.close()


def write_projects_to_db(df: pd.DataFrame, db_path: str = "data/dmp_data.db") -> None:
    """Write the projects DataFrame to the SQLite database."""
    conn = sqlite3.connect(db_path)

    # Write to database, replace if exists
    df.to_sql("projects", conn, if_exists="replace", index=False)

    conn.close()
