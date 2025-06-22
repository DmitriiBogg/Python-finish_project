import sqlite3
import pandas as pd

CSV_PATH = "data/player_stats_2000_2026.csv"
DB_PATH = "data/baseball.db"

def import_to_db():
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("player_stats", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Imported {len(df)} rows into 'player_stats' table.")

if __name__ == "__main__":
    import_to_db()
