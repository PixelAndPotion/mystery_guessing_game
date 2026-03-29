import sqlite3

def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            avatar TEXT
        )
    ''')

    # Friends
    c.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            user_id INTEGER,
            friend_id INTEGER
        )
    ''')

    # Rooms
    c.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT,
            host_id INTEGER,
            is_private BOOLEAN
        )
    ''')

    # Rounds
    c.execute('''
        CREATE TABLE IF NOT EXISTS rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER,
            round_number INTEGER,
            puzzle_data TEXT,
            type TEXT
        )
    ''')

    # Guesses
    c.execute('''
        CREATE TABLE IF NOT EXISTS guesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_id INTEGER,
            user_id INTEGER,
            guess TEXT,
            correct BOOLEAN,
            time_taken REAL
        )
    ''')

    # Scores
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            user_id INTEGER PRIMARY KEY,
            total_points INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            achievements TEXT
        )
    ''')

    # Hints
    c.execute('''
        CREATE TABLE IF NOT EXISTS hints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_id INTEGER,
            user_id INTEGER,
            hint_type TEXT,
            points_spent INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()