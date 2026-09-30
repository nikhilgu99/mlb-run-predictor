import statsapi
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="mlb_db",
    user="mlb_admin",
    password="admin_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

def get_pitcher_whip(pitcher_name):
    """Fetches season WHIP for a pitcher by name; falls back to 1.25 (league average) if unannounced or not found."""
    if not pitcher_name or pitcher_name == "TBD":
        return 1.25
    
    try:
        results = statsapi.lookup_player(pitcher_name)
        if not results:
            return 1.25
        
        player_id = results[0]["id"]
        stats = statsapi.player_stat_data(player_id, group="pitching", type="season")
        pitching_stats = stats.get("stats", [{}])[0].get("stats", {})
        return float(pitching_stats.get("whip", 1.25))
    except Exception:
        return 1.25

def compute_yrfi_probability(away_whip, home_whip):
    """Calculates YRFI probability based on WHIP deviations from the league average (1.25)."""
    league_avg_whip = 1.25
    base_probability = 0.50
    weight = 0.15

    away_delta = (away_whip - league_avg_whip) / league_avg_whip
    home_delta = (home_whip - league_avg_whip) / league_avg_whip

    prob = base_probability + (weight * away_delta) + (weight * home_delta)
    return round(max(0.20, min(0.80, prob)) * 100, 2)

# Select games where probability is uncalculated or zero
cursor.execute("""
    SELECT game_pk, away_pitcher, home_pitcher 
    FROM daily_matchups 
    WHERE yrfi_probability = 0.00;
""")
games_to_process = cursor.fetchall()

print(f"Calculating probabilities for {len(games_to_process)} matchups...")

# Process and update db
for game_pk, away_pitcher, home_pitcher in games_to_process:
    away_whip = get_pitcher_whip(away_pitcher)
    home_whip = get_pitcher_whip(home_pitcher)
    
    yrfi_score = compute_yrfi_probability(away_whip, home_whip)

    cursor.execute("""
        UPDATE daily_matchups 
        SET yrfi_probability = %s 
        WHERE game_pk = %s;
    """, (yrfi_score, game_pk))

conn.commit()
cursor.close()
conn.close()

print("Calculation complete and database updated.")