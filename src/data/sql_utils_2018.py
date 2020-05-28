import psycopg2
import pandas as pd
import os

DBNAME = "opportunity_youth"

#Retrieving postgres info for MEF
# from src.data import local
# PORT = local.port
# USER = local.user
# HOST = local.host
# PASSWORD = local.password


def create_tables():
    """
    Composite function that creates all relevant tables in the database
    This creates empty tables with the appropriate schema, then the data
    transfer is performed in the `copy_csv_files` function
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname=DBNAME, user="postgres", password="password")
#     conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, port=PORT, host=HOST)
    conn = psycopg2.connect(dbname=DBNAME)

    create_pums_2014_table(conn)
#     create_pums_2015_table(conn)
#     create_pums_2016_table(conn)
    create_pums_2018_table(conn)
    
    conn.close()


def create_pums_2014_table(conn):
    """
    Create a table for the 2014 5-year persons PUMS data
    """
    execute_sql_script(conn, "create_pums_2014_table.sql")
    
    
# def create_pums_2015_table(conn):
#     """
#     Create a table for the 2015 5-year persons PUMS data
#     """
#     execute_sql_script(conn, "create_pums_2015_table.sql")

    
# def create_pums_2016_table(conn):
#     """
#     Create a table for the 2016 5-year persons PUMS data
#     """
#     execute_sql_script(conn, "create_pums_2016_table.sql")
    
    
def create_pums_2018_table(conn):
    """
    Create a table for the 2018 5-year persons PUMS data
    """
    execute_sql_script(conn, "create_pums_2018_table.sql")


def copy_csv_files(data_files_dict):
    """
    Composite function that copies all CSV files into the database
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname=DBNAME, user="postgres", password="password")
#     conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, port=PORT, host=HOST)
    conn = psycopg2.connect(dbname=DBNAME)

    for name, files in data_files_dict.items():
        csv_file = files[0]
        # skip the header; this info is already in the table schema
        next(csv_file)
        if name == "pums_2014":
            copy_csv_to_pums_2014_table(conn, csv_file)
#         elif name == "pums_2015":
#             copy_csv_to_pums_2015_table(conn, csv_file)
#         elif name == "pums_2016":
#             copy_csv_to_pums_2016_table(conn, csv_file)
        if name == "pums_2018":
            copy_csv_to_pums_2018_table(conn, csv_file)
        print(f"""Successfully loaded CSV file into `{name}` table
        """)

    conn.close()


def copy_csv_to_pums_2014_table(conn, csv_file):
    """
    Copy the CSV contents of the 2014 5-year persons data into the table
    """
    COPY_PUMS_2014 = "copy_pums_2014_to_table.psql"
    copy_expert_psql_script(conn, COPY_PUMS_2014, csv_file)
    
# def copy_csv_to_pums_2015_table(conn, csv_file):
#     """
#     Copy the CSV contents of the 2015 5-year persons data into the table
#     """
#     COPY_PUMS_2015 = "copy_pums_2015_to_table.psql"
#     copy_expert_psql_script(conn, COPY_PUMS_2015, csv_file)
    
# def copy_csv_to_pums_2016_table(conn, csv_file):
#     """
#     Copy the CSV contents of the 2016 5-year persons data into the table
#     """
#     COPY_PUMS_2016 = "copy_pums_2016_to_table.psql"
#     copy_expert_psql_script(conn, COPY_PUMS_2016, csv_file)
    
def copy_csv_to_pums_2018_table(conn, csv_file):
    """
    Copy the CSV contents of the 2018 5-year persons data into the table
    """
    COPY_PUMS_2018 = "copy_pums_2018_to_table.psql"
    copy_expert_psql_script(conn, COPY_PUMS_2018, csv_file)
    

def execute_sql_script(conn, script_filename):
    """
    Given a DB connection and a file path to a SQL script, open up the SQL
    script and execute it
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.execute(file_contents)
    conn.commit()


def open_sql_script(script_filename):
    """
    Given a file path, open the file and return its contents
    We assume that the file path is always inside the sql directory
    """
    dir = os.path.dirname(__file__)
    relative_filename = os.path.join(dir, 'sql', script_filename)

    file_obj = open(relative_filename, 'r')
    file_contents = file_obj.read()
    file_obj.close()

    return file_contents


def copy_expert_psql_script(conn, script_filename, csv_file):
    """
    Given a DB connection and a file path to a PSQL script, open up the PSQL
    script and use it to run copy_expert
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.copy_expert(file_contents, csv_file)
    conn.commit()
