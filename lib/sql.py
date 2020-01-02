import os
import sqlite3
import datetime

from lib.settings import (
    ISIE_DATABASE_FILE_PATH,
    ISIE_HOME
)


def initialize():
    """
    initialize the database
    """
    if not os.path.exists(ISIE_HOME):
        os.makedirs(ISIE_HOME)
    cursor = sqlite3.connect(ISIE_DATABASE_FILE_PATH)
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS "images" ('
        '`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
        '`base64_data` TEXT NOT NULL,'
        '`timestamp` TEXT NOT NULL,'
        '`watermark_used` TEXT NOT NULL,'
        '`sent_to` TEXT NOT NULL,'
        '`filetype` TEXT NOT NULL'
        ')'
    )
    conn = sqlite3.connect(ISIE_DATABASE_FILE_PATH, isolation_level=None, check_same_thread=False)
    return conn.cursor()


def fetch(cursor):
    """
    fetch all the data from the database
    """
    try:
        data = cursor.execute("SELECT * FROM images")
        results = data.fetchall()
    except Exception:
        results = []
    return results


def insert(cursor, base64_data, watermark_used, filetype, sent_to="N/A"):
    """
    insert that shit into the database
    """
    try:
        current_cache = fetch(cursor)
        id_number = len(current_cache) + 1
        timestamp = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
        cursor.execute(
            "INSERT INTO images (id,base64_data,timestamp,watermark_used,sent_to,filetype) VALUES (?,?,?,?,?,?)", (
                id_number,
                base64_data,
                timestamp,
                watermark_used,
                sent_to,
                filetype
            )
        )
    except Exception as e:
        print e
        return False
    return True
