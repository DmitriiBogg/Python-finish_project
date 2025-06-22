import sqlite3

DB_PATH = "data/baseball.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Database connected. Enter SQL queries or 'exit' to quit.")

    while True:
        query = input("SQL> ")
        if query.lower() in ("exit", "quit"):
            break
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Exception as e:
            print(f"Error: {e}")

    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
