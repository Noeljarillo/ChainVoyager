import requests
import sqlite3
import json
from datetime import datetime

def flatten_json(y, prefix=''):
    """Flatten nested JSON into a flat dictionary."""
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            full_key = f"{prefix}{k}" if prefix == '' else f"{prefix}_{k}"
            out.update(flatten_json(v, full_key))
    elif isinstance(y, list):
        for index, item in enumerate(y):
            full_key = f"{prefix}_{index}"
            out.update(flatten_json(item, full_key))
    else:
        out[prefix] = y
    return out

def fetch_and_save_pools_data(db_path):
    api_url = "https://yields.llama.fi/pools"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    
    data = response.json().get("data", [])
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    all_keys = set()
    flattened_data = []
    for pool in data:
        flat_pool = flatten_json(pool)
        flattened_data.append(flat_pool)
        all_keys.update(flat_pool.keys())

    all_keys = sorted(all_keys)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pools';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Initializing database...")
        columns = ',\n    '.join([f"'{key}' TEXT" for key in all_keys])
        create_table_sql = f"""
            CREATE TABLE pools (
                {columns},
                'created_at' TEXT
            )
        """
        cursor.execute(create_table_sql)
        print("Database initialized.")
    else:
        # Check if any new columns need to be added
        cursor.execute("PRAGMA table_info(pools);")
        existing_columns = [info[1] for info in cursor.fetchall()]
        new_columns = [key for key in all_keys if key not in existing_columns]
        for column in new_columns:
            cursor.execute(f"ALTER TABLE pools ADD COLUMN '{column}' TEXT;")
            print(f"Added new column '{column}' to the table.")

    for flat_pool in flattened_data:
        flat_pool['created_at'] = datetime.utcnow().isoformat()
        columns = ', '.join([f"'{key}'" for key in flat_pool.keys()])
        placeholders = ', '.join(['?' for _ in flat_pool.keys()])
        values = [str(flat_pool[key]) for key in flat_pool.keys()]
        insert_sql = f"INSERT INTO pools ({columns}) VALUES ({placeholders})"
        cursor.execute(insert_sql, values)

    conn.commit()
    conn.close()
    print(f"Data successfully saved to {db_path}")
