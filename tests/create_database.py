import pandas as pd
import sqlite3

def create_user_accounts(db_path, csv_path, table_name):
    df = pd.read_csv(csv_path)
    df["id"] = df["id"].astype(int)
    df["last_update"] = pd.to_datetime(df["last_update"])
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Drop the existing table if it exists
    conn.execute(f"DROP TABLE IF EXISTS {table_name};")
    
    # Create a new table with a primary key
    conn.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT, 
            auth TEXT,
            last_update DATETIME
        );
    """)

    # # Insert data from DataFrame into the new table
    df.to_sql(table_name, conn, if_exists='append', index=False)

    conn.close()

def save_csv_to_db(db_path, csv_path, table_name):
    # Read CSV data
    df = pd.read_csv(csv_path)
    df["id"] = df["id"].astype(int)
    df["last_update"] = pd.to_datetime(df["last_update"])

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Drop the existing table if it exists
    conn.execute(f"DROP TABLE IF EXISTS {table_name};")

    # Create a new table with a primary key
    conn.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,
            process_id TEXT,
            layer TEXT,
            tool TEXT,
            bin_lst TEXT,
            signature TEXT,
            type TEXT,
            name TEXT,
            user TEXT,
            desc TEXT,
            last_update DATETIME
        );
    """)

    # Insert data from DataFrame into the new table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.close()

def create_color_bin_table(db_path, csv_path, table_name):
    # Read CSV data
    df = pd.read_csv(csv_path)
    df["id"] = df["id"].astype(int)
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Drop the existing table if it exists
    conn.execute(f"DROP TABLE IF EXISTS {table_name};")

    # Create a new table with a primary key
    conn.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,
            process_id TEXT,
            bin TEXT,
            bin_group TEXT,
            color TEXT
        );
    """)

    # Insert data from DataFrame into the new table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.close()

def create_test_main_page_database(db_path, csv_path, table_name):
    # Read CSV data
    df = pd.read_csv(csv_path)
    df["id"] = df["id"].astype(int)
    df["wafer_id"] = df["wafer_id"].astype(str)
    df["yld"] = df["yld"].astype(str)
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Drop the existing table if it exists
    conn.execute(f"DROP TABLE IF EXISTS {table_name};")

    # Create a new table with a primary key
    conn.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,
            lot_id TEXT,
            wafer_id TEXT,
            yield TEXT,
            fail_bin TEXT,
            swly_mark TEXT,
            swly_label TEXT
        );
    """)

    # Insert data from DataFrame into the new table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.close()

if __name__ == "__main__":
    # csv_path = "/Users/JianQiu/Dropbox/pythonprojects/fastapi-aggrid/tests/test_signature.csv"
    # db_path = "/Users/JianQiu/Dropbox/pythonprojects/fastapi-aggrid/test.db"
    # account_csv_path = "/Users/JianQiu/Dropbox/pythonprojects/fastapi-aggrid/tests/test_account.csv"
    # save_csv_to_db(db_path=db_path, csv_path=csv_path, table_name="swly_name_table")
    # create_user_accounts(db_path=db_path, csv_path=account_csv_path, table_name="accounts")
    # csv_path = r"C:\Users\Jian Qiu\Dropbox\pythonprojects\fastapi-aggrid\tests\sample_color.csv"
    # db_path = r"C:\Users\Jian Qiu\Dropbox\pythonprojects\fastapi-aggrid\test.db"
    # create_color_bin_table(db_path=db_path, csv_path=csv_path, table_name="BIN_COLOR_TABLE")
    csv_path = r"C:\Users\Jian Qiu\Dropbox\pythonprojects\fastapi-aggrid\tests\Book1.csv"
    db_path = r"C:\Users\Jian Qiu\Dropbox\pythonprojects\fastapi-aggrid\test.db"
    create_test_main_page_database(db_path=db_path, csv_path=csv_path, table_name="low_yield_table")




