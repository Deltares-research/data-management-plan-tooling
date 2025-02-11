from typing import Dict, List
from dotenv import load_dotenv
import os

import pandas as pd
import requests

load_dotenv()
API_URL = os.getenv("API_URL")
if API_URL is None:
    raise ValueError("API_URL environment variable is not set.")

def call_dmp_api(
    api_url: str = API_URL,
    since_date: str = "2023.11.01",
    verify_ssl: bool = False,
) -> List[Dict]:
    """
    Call the DMP API and return the project data.

    Args:
        api_url (str): The URL of the DMP API
        since_date (str): Date string to filter projects (will be converted to yyyy.mm.dd)
        verify_ssl (bool): Whether to verify SSL certificates. Default False for internal systems.

    Returns:
        List[Dict]: List of project dictionaries with the following fields:
            - ProjectNumber: Project identifier
            - ProjectDescription: Description of the project
            - Closed: Project closure status
            - Unit: Unit identifier
            - ResponsibleDepartment: Department code
            - ResponsibleDepartmentDescription: Department name
            - ProjectType: Type code
            - ProjectTypeDescription: Type description
            - Financier: Project financier
            - BusinessArea: Business area code
            - BusinessAreaDescription: Business area name
            - ProjectLeaderNumber: Project leader ID
            - ProjectLeaderName: Project leader name
            - ProjectAdministratorNumber: Administrator ID
            - ProjectAdministratorName: Administrator name
            - DateCreated: Creation timestamp
            - DateModified: Last modification timestamp
            - DateStart: Project start date
            - DateEnd: Project end date
            - DateClosed: Project closure date
            - Status: Project status
    """

    # Prepare query parameters
    params = {}
    params["since_date"] = since_date

    try:
        # Disable SSL verification warning if verify=False
        if not verify_ssl:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Make request with params
        response = requests.get(api_url, params=params, verify=verify_ssl, timeout=60)

        # Print the actual URL being called (helpful for debugging)
        print(f"Calling API URL: {response.url}")

        response.raise_for_status()
        data = response.json()

        if "projects" not in data:
            print(
                f"Warning: 'projects' key not found in response. Response structure: {list(data.keys())}"
            )
            return []

        return data["projects"]

    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
        print("Try setting verify_ssl=False if using self-signed certificates")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        print(f"Response status code: {getattr(e.response, 'status_code', 'N/A')}")
        print(f"Response content: {getattr(e.response, 'text', 'N/A')[:200]}...")
        return []
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response content: {response.text[:200]}...")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def process_api_data(projects: List[Dict]) -> pd.DataFrame:
    """
    Process the API response data into a DataFrame.

    Args:
        projects (List[Dict]): List of project dictionaries from the API

    Returns:
        pd.DataFrame: Processed DataFrame with project information
    """
    if not projects:
        return pd.DataFrame()

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(projects)

    # Convert date strings to datetime objects
    date_columns = ["DateCreated", "DateModified", "DateStart", "DateEnd", "DateClosed"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    df = df.rename(columns={"Status": "Status_API"})
    df["Quote_Status"] = df["Status_API"].apply(
        lambda x: (
            "Quote"
            if "Quote" in str(x)
            else "Order" if any(c.isdigit() for c in str(x)) else "Unknown"
        )
    )

    return df
