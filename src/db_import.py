import sqlite3
import pandas as pd

CSV_PATH = "data/player_stats_2000_2025.csv"
DB_PATH = "data/baseball.db"

def import_to_db():
    df = pd.read_csv(CSV_PATH)
    
    # clean the df
    df['Team'] = df['Team'].replace({
        'New York': 'New York Yankees',
        'Boston': 'Boston Red Sox',
        'Chicago': 'Chicago White Sox',
        'Cleveland': 'Cleveland Guardians',
        'Cleveland Indians': 'Cleveland Guardians',
        'Detroit': 'Detroit Tigers',
        'Houston': 'Houston Astros',
        'Kansas City': 'Kansas City Royals',
        'Los Angeles': 'Los Angeles Angels',
        'Anaheim': 'Los Angeles Angels',
        'Minnesota': 'Minnesota Twins',
        'Oakland': 'Oakland Athletics',
        'Seattle': 'Seattle Mariners',
        'Tampa Bay': 'Tampa Bay Rays',
        'Texas': 'Texas Rangers',
        'Toronto': 'Toronto Blue Jays',
        'Baltimore': 'Baltimore Orioles'
    })

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("player_stats", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Imported {len(df)} rows into 'player_stats' table.")

if __name__ == "__main__":
    import_to_db()
