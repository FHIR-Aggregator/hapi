import sqlite3

def get_ids_from_file(file_path):
    """
    Read IDs from the given file. Each line contains one ID.
    :param file_path: Path to the file containing IDs.
    :return: A list of IDs.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

def find_missing_ids(db_path, ids):
    """
    Find IDs that are not present in the SQLite database.
    :param db_path: Path to the SQLite database.
    :param ids: List of IDs to check in the database.
    :return: A list of IDs that are not found in the database.
    """
    missing_ids = []
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        for id in ids:
            cursor.execute("SELECT id FROM resources WHERE id = ?", (id,))
            if not cursor.fetchone():
                missing_ids.append(id)
    finally:
        connection.close()
    return missing_ids

if __name__ == "__main__":
    # Path to the input file and SQLite database
    file_path = "/tmp/group_ids.txt"
    db_path = "/tmp/fhir-graph.sqlite"

    # Read IDs from the file
    ids = get_ids_from_file(file_path)
    if not ids:
        print("No IDs to process.")
        exit(1)

    # Find missing IDs in the database
    missing_ids = find_missing_ids(db_path, ids)

    # Print missing IDs
    if missing_ids:
        print("The following IDs were not found in the database:")
        for missing_id in missing_ids:
            print(missing_id)
    else:
        print("All IDs were found in the database.")

