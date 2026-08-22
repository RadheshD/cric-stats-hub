import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore
import json
import pandas as pd
import os
from file_manager import read_json
from openpyxl.styles import Font, Alignment, Border, Side

# Beginner-friendly config values. 
# NOTE: Please change the password according to your local MySQL setup.
DB_CONFIG = {
    "host": "localhost",
    "user": "cricket_user",
    "password": "cricket123",
    "database": "cricket_stats_db"
}

def connect_db(use_db=True):
    """Connect to MySQL database."""
    try:
        config = DB_CONFIG.copy()
        if not use_db:
            config.pop('database', None) # Remove database for initial connection to create it
        
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
    except Error as e:
        pass # Return None silently as handled in main.py
    return None

def create_database_if_not_exists():
    """Create the cricket_stats_db if it does not already exist."""
    connection = connect_db(use_db=False)
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            print(f"Database '{DB_CONFIG['database']}' checked/created successfully.")
        except Error as e:
            print(f"Error creating database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def reset_database_tables():
    """Safely drop only the project tables if they exist to start fresh."""
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS bowling_stats")
            cursor.execute("DROP TABLE IF EXISTS batting_stats")
            cursor.execute("DROP TABLE IF EXISTS team_scores")
            cursor.execute("DROP TABLE IF EXISTS team_scores_db")
            cursor.execute("DROP TABLE IF EXISTS match_team_scores")
            cursor.execute("DROP TABLE IF EXISTS team_scores")
            cursor.execute("DROP TABLE IF EXISTS matches")
            connection.commit()
            print("Project tables dropped successfully for reset.")
        except Error as e:
            print(f"Error resetting tables: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def create_tables():
    """Create necessary tables if they do not exist."""
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            
            # matches
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    match_name VARCHAR(150),
                    tournament VARCHAR(150),
                    match_date VARCHAR(50),
                    venue VARCHAR(200),
                    toss VARCHAR(250),
                    result VARCHAR(250)
                )
            """)
            
            # team_scores_db
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS team_scores_db (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    team VARCHAR(100),
                    runs INT,
                    wickets INT,
                    overs VARCHAR(20),
                    status VARCHAR(50),
                    FOREIGN KEY(match_id) REFERENCES matches(id) ON DELETE CASCADE
                )
            """)

            # batting_stats
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS batting_stats (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    team VARCHAR(100),
                    player VARCHAR(150),
                    runs INT,
                    status VARCHAR(50),
                    FOREIGN KEY(match_id) REFERENCES matches(id) ON DELETE CASCADE
                )
            """)

            # bowling_stats
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bowling_stats (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    team VARCHAR(100),
                    bowler VARCHAR(150),
                    wickets INT,
                    FOREIGN KEY(match_id) REFERENCES matches(id) ON DELETE CASCADE
                )
            """)
            
            connection.commit()
            print("Tables 'matches', 'match_team_scores', 'batting_stats', 'bowling_stats' created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def insert_match(match_name, tournament, match_date, venue, toss, result):
    """Insert a single match into the database."""
    connection = connect_db()
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        sql = """INSERT INTO matches (match_name, tournament, match_date, venue, toss, result) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (match_name, tournament, match_date, venue, toss, result)
        cursor.execute(sql, values)
        connection.commit()
        match_id = cursor.lastrowid
        return match_id
    except Error as e:
        print(f"Error inserting match: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_match_data_from_json(json_file_path):
    """Read match data from JSON and insert it into MySQL database to avoid duplicates."""
    data = read_json(json_file_path)
    if not data:
        print("No data found in JSON to insert.")
        return None
        
    connection = connect_db()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        
        match_details = data.get('match_details', {})
        match_name = match_details.get('match', '')
        tournament = match_details.get('tournament', '')
        match_date = match_details.get('date', '')
        venue = match_details.get('venue', '')
        toss = match_details.get('toss', '')
        result = match_details.get('result', '')
        
        # Check if match already exists
        cursor.execute("""
            SELECT id FROM matches 
            WHERE match_name = %s AND match_date = %s AND venue = %s
        """, (match_name, match_date, venue))
        
        existing_match = cursor.fetchone()
        
        if existing_match:
            match_id = existing_match[0]
            print(f"Match already exists in database. Inserted/Existing Match ID: {match_id}")
            return match_id
            
        # Insert match
        cursor.execute("""
            INSERT INTO matches (match_name, tournament, match_date, venue, toss, result) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (match_name, tournament, match_date, venue, toss, result))
        match_id = cursor.lastrowid
            
        # Insert team scores
        team_scores = data.get('team_scores', {})
        for team, score in team_scores.items():
            runs = score.get('runs', 0)
            wickets = score.get('wickets', 0)
            overs = str(score.get('overs', 0.0))
            status = score.get('status', '')
            cursor.execute("""
                INSERT INTO team_scores_db (match_id, team, runs, wickets, overs, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (match_id, team, runs, wickets, overs, status))

        # Insert batting stats
        batting_stats = data.get('batting_stats', {})
        for team, players in batting_stats.items():
            for p in players:
                player = p.get('player', '')
                runs = p.get('runs', 0)
                status = p.get('status', '')
                cursor.execute("""
                    INSERT INTO batting_stats (match_id, team, player, runs, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (match_id, team, player, runs, status))
                
        # Insert bowling stats
        bowling_stats = data.get('bowling_stats', {})
        for team, bowlers in bowling_stats.items():
            for b in bowlers:
                bowler = b.get('bowler', '')
                wickets = b.get('wickets', 0)
                cursor.execute("""
                    INSERT INTO bowling_stats (match_id, team, bowler, wickets)
                    VALUES (%s, %s, %s, %s)
                """, (match_id, team, bowler, wickets))
                
        connection.commit()
        print(f"Successfully inserted match data from JSON. Inserted/Existing Match ID: {match_id}")
        return match_id
        
    except Error as e:
        print(f"Error inserting data from JSON: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_all_matches():
    """Retrieve all matches from the database."""
    connection = connect_db()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM matches")
        matches = cursor.fetchall()
        return matches
    except Error as e:
        print(f"Error fetching matches: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_team_scores(match_id=None):
    """Retrieve team scores, optionally filtered by match_id."""
    connection = connect_db()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        if match_id:
            cursor.execute("SELECT * FROM team_scores_db WHERE match_id = %s", (match_id,))
        else:
            cursor.execute("SELECT * FROM team_scores_db")
        stats = cursor.fetchall()
        return stats
    except Error as e:
        print(f"Error fetching team scores: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_batting_stats(match_id=None):
    """Retrieve batting stats, optionally filtered by match_id."""
    connection = connect_db()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        if match_id:
            cursor.execute("SELECT * FROM batting_stats WHERE match_id = %s", (match_id,))
        else:
            cursor.execute("SELECT * FROM batting_stats")
        stats = cursor.fetchall()
        return stats
    except Error as e:
        print(f"Error fetching batting stats: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_bowling_stats(match_id=None):
    """Retrieve bowling stats, optionally filtered by match_id."""
    connection = connect_db()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        if match_id:
            cursor.execute("SELECT * FROM bowling_stats WHERE match_id = %s", (match_id,))
        else:
            cursor.execute("SELECT * FROM bowling_stats")
        stats = cursor.fetchall()
        return stats
    except Error as e:
        print(f"Error fetching bowling stats: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_match_result(match_id, new_result):
    """Update the result of a specific match."""
    connection = connect_db()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE matches SET result = %s WHERE id = %s", (new_result, match_id))
        connection.commit()
        print(f"Match ID {match_id} result updated to: {new_result}")
        return True
    except Error as e:
        print(f"Error updating match result: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_match(match_id):
    """Delete a match from the database. (Also deletes related stats due to CASCADE)."""
    connection = connect_db()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM matches WHERE id = %s", (match_id,))
        connection.commit()
        print(f"Match ID {match_id} and related stats deleted successfully.")
        return True
    except Error as e:
        print(f"Error deleting match: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def export_db_to_json(output_file="output/db_export.json"):
    """Export all database data to a single JSON file."""
    matches = get_all_matches()
    team_scores = get_team_scores()
    batting = get_batting_stats()
    bowling = get_bowling_stats()
    
    if not matches:
        print("No database data to export to JSON.")
        return
        
    db_data = {
        "matches": matches,
        "team_scores": team_scores,
        "batting_stats": batting,
        "bowling_stats": bowling
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, indent=4, default=str)
        print(f"Database exported to JSON successfully at {output_file}")
    except Exception as e:
        print(f"Error exporting DB to JSON: {e}")

def export_db_to_excel(output_file="output/db_export.xlsx"):
    """Export database data to an Excel file with multiple sheets and formatting."""
    matches = get_all_matches()
    if not matches:
        print("No database data to export to Excel.")
        return
        
    team_scores = get_team_scores()
    batting = get_batting_stats()
    bowling = get_bowling_stats()
    
    matches_df = pd.DataFrame(matches)
    # Ensure dates are strings to prevent formatting issues in Excel
    if 'match_date' in matches_df.columns:
        matches_df['match_date'] = matches_df['match_date'].astype(str)
        
    team_scores_df = pd.DataFrame(team_scores)
    batting_df = pd.DataFrame(batting)
    bowling_df = pd.DataFrame(bowling)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            matches_df.to_excel(writer, sheet_name='Matches', index=False)
            if not team_scores_df.empty:
                team_scores_df.to_excel(writer, sheet_name='Team Scores', index=False)
            if not batting_df.empty:
                batting_df.to_excel(writer, sheet_name='Batting Stats', index=False)
            if not bowling_df.empty:
                bowling_df.to_excel(writer, sheet_name='Bowling Stats', index=False)
        
        # Add basic formatting
        from openpyxl import load_workbook
        wb = load_workbook(output_file)
        header_font = Font(bold=True)
        border_style = Side(style='thin')
        border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)
        alignment = Alignment(horizontal='center', vertical='center')

        for sheet in wb.sheetnames:
            ws = wb[sheet]
            for cell in ws[1]:
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center')
            
            for col in ws.columns:
                max_length = 0
                column_letter = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                    cell.border = border
                    if cell.row != 1:
                        cell.alignment = alignment
                
                ws.column_dimensions[column_letter].width = (max_length + 2)
                
        wb.save(output_file)
        print(f"Database exported to Excel successfully at {output_file}")
    except Exception as e:
        print(f"Error exporting DB to Excel: {e}")

def generate_html_table(output_file="output/db_table.html"):
    """Generate a clean HTML file showing database tables."""
    matches = get_all_matches()
    if not matches:
        print("No database data to export to HTML.")
        return
        
    team_scores = get_team_scores()
    batting = get_batting_stats()
    bowling = get_bowling_stats()
    
    matches_df = pd.DataFrame(matches)
    team_scores_df = pd.DataFrame(team_scores)
    batting_df = pd.DataFrame(batting)
    bowling_df = pd.DataFrame(bowling)
    
    html_template = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ text-align: center; color: #333; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #f2f2f2; color: #333; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Cricket Match Database Stats</h1>
        
        <h2>Matches</h2>
        {matches_df.to_html(index=False, classes='table')}
        
        <h2>Team Scores</h2>
        {team_scores_df.to_html(index=False, classes='table') if not team_scores_df.empty else '<p>No data</p>'}
        
        <h2>Batting Stats</h2>
        {batting_df.to_html(index=False, classes='table') if not batting_df.empty else '<p>No data</p>'}
        
        <h2>Bowling Stats</h2>
        {bowling_df.to_html(index=False, classes='table') if not bowling_df.empty else '<p>No data</p>'}
    </body>
    </html>
    """
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"Database HTML tables generated successfully at {output_file}")
    except Exception as e:
        print(f"Error exporting DB to HTML: {e}")
