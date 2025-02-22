import sqlite3
import random


def create_tables():
    conn = sqlite3.connect("mafia_baku.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            chat_id INTEGER,
            role TEXT DEFAULT NULL
        )
    """)

    conn.commit()
    conn.close()


create_tables()


def add_player(user_id, username, chat_id):
    conn = sqlite3.connect("mafia_baku.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO players (user_id, username, chat_id, role) VALUES (?, ?, ?, ?)",
                   (user_id, username, chat_id, None))

    conn.commit()
    conn.close()


def get_players(chat_id):
    conn = sqlite3.connect("mafia_baku.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM players WHERE chat_id=?", (chat_id,))
    players = cursor.fetchall()
    conn.close()
    return players



def save_roles(assigned_roles):
    conn = sqlite3.connect("mafia_baku.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT OR REPLACE INTO roles (user_id, role) VALUES (?, ?)", assigned_roles)
    conn.commit()
    conn.close()



def get_role(user_id):
    conn = sqlite3.connect("mafia_baku.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM players WHERE user_id=?", (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else None
