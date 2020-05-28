from io import BytesIO, TextIOWrapper, StringIO
from zipfile import ZipFile
from gzip import GzipFile
from csv import QUOTE_ALL

import pandas as pd
import requests

from src.data import sql_utils_2018

def download_data_and_load_into_sql():
    """
    This function dispatches everything.  It creates a PostgreSQL database with
    the appropriate name, sets up the table schema, downloads all of the files
    containing the data, and loads the data into the database
    """
    sql_utils_2018.create_tables()
    data_files_dict = collect_all_data_files()
    load_into_sql(data_files_dict)


def collect_all_data_files():
    """
    Create a dictionary with the in-memory file objects associated with all
    database tables
    """
    data_files_dict = {
        "pums_2014": collect_pums_2014_data(),
        "pums_2015": collect_pums_2015_data(),
        "pums_2016": collect_pums_2016_data(),
        "pums_2018": collect_pums_2018_data()
    }
    return data_files_dict


def load_into_sql(data_files_dict):
    """
    Given a dictionary of in-memory file objects, use sql_utils to copy them
    into the database.  Then close all of them.

    Each dictionary value is a tuple containing a CSV file object, then either
    None or some other file to be closed, e.g. a zip file
    """
    sql_utils_2018.copy_csv_files(data_files_dict)

    for csv_file, other_file in data_files_dict.values():
        csv_file.close()
        if other_file:
            other_file.close()


def collect_pums_2014_data():
    """
    Download the 2014 5-year ACS PUMS person-level records for the state of WA
    """
    PUMS_2014_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2014/5-Year/csv_pwa.zip"
    PUMS_2014_CSV_NAME = "ss14pwa.csv"
    return collect_zipfile_data(PUMS_2014_URL, PUMS_2014_CSV_NAME)


def collect_pums_2015_data():
    """
    Download the 2015 5-year ACS PUMS person-level records for the state of WA
    """
    PUMS_2015_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year/csv_pwa.zip"
    PUMS_2015_CSV_NAME = "ss15pwa.csv"
    return collect_zipfile_data(PUMS_2015_URL, PUMS_2015_CSV_NAME)


def collect_pums_2016_data():
    """
    Download the 2016 5-year ACS PUMS person-level records for the state of WA
    """
    PUMS_2016_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2016/5-Year/csv_pwa.zip"
    PUMS_2016_CSV_NAME = "ss16pwa.csv"
    return collect_zipfile_data(PUMS_2016_URL, PUMS_2016_CSV_NAME)


def collect_pums_2018_data():
    """
    Download the 2018 5-year ACS PUMS person-level records for the state of WA
    """
    PUMS_2018_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2018/5-Year/csv_pwa.zip"
    PUMS_2018_CSV_NAME = "psam_p53.csv"
    return collect_zipfile_data(PUMS_2018_URL, PUMS_2018_CSV_NAME)


def collect_zipfile_data(URL, csv_name):
    """
    Helper function used to collect CSV files contained in .zip archives
    """
    zip_file = download_zipfile(URL)
    csv_file = open_csv_from_zip(zip_file, csv_name)
    # return both so we can safely close them at the end
    return csv_file, zip_file


def download_zipfile(URL):
    """
    Given a URL for a .zip, download and unzip the .zip file
    """
    response = requests.get(URL)
    print(f"""Successfully downloaded ZIP file
    {URL}
    """)

    content_as_file = BytesIO(response.content)
    zip_file = ZipFile(content_as_file)
    return zip_file


def open_csv_from_zip(zip_file, csv_name):
    """
    Given an unzipped .zip file and the name of a CSV inside of it, 
    extract the CSV and return the relevant file
    """
    csv_file_bytes = zip_file.open(csv_name)
    # it seems we have to open the .zip as bytes, but CSV reader requires text
    csv_file_text = TextIOWrapper(csv_file_bytes, encoding="ISO-8859-1")
    return csv_file_text