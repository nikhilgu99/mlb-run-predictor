import statsapi
import psycopg2
from datetime import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="mlb_db",
    user="mlb_admin",
    password="admin_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Define the Schema
cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_matchups (
    game_pk INT PRIMARY KEY,
    game_date DATE NOT NULL,
    away_team VARCHAR(50) NOT NULL,
    home_team VARCHAR(50) NOT NULL,
    away_pitcher VARCHAR(100),
    home_pitcher VARCHAR(100),
    yrfi_probability DECIMAL(5,2) DEFAULT 0.00
);
""")
conn.commit()

# Fetch MLB Schedule and Probable Pitchers
today = datetime.today().strftime('%Y-%m-%d')
# The hydrate parameter ensures we receive the starting pitcher data with the schedule
schedule = statsapi.get("schedule", {"sportId": 1, "date": today, "hydrate": "probablePitcher(note)"})

games = schedule.get("dates", [])[0].get("games", []) if schedule.get("dates") else []

# 4. Parse and Insert Data
for game in games:
    game_pk = game["gamePk"]
    game_date = game["officialDate"]
    
    teams = game["teams"]
    away_team = teams["away"]["team"]["name"]
    home_team = teams["home"]["team"]["name"]
    
    # Extract probable pitchers if they have been announced
    away_pitcher = teams["away"].get("probablePitcher", {}).get("fullName", "TBD")
    home_pitcher = teams["home"].get("probablePitcher", {}).get("fullName", "TBD")
    
    # Insert or update the database record
    cursor.execute("""
        INSERT INTO daily_matchups (game_pk, game_date, away_team, home_team, away_pitcher, home_pitcher)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (game_pk) DO UPDATE 
        SET away_pitcher = EXCLUDED.away_pitcher,
            home_pitcher = EXCLUDED.home_pitcher;
    """, (game_pk, game_date, away_team, home_team, away_pitcher, home_pitcher))

conn.commit()
cursor.close()
conn.close()

print(f"Successfully processed {len(games)} games for {today}.")