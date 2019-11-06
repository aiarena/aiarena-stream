import sqlite3

database_file = "data.db"
db = sqlite3.connect(database_file)


def create_db():
    cursor = db.cursor()
    cursor.execute('CREATE TABLE match_queue(match_id INTEGER PRIMARY KEY)')
    db.commit()


def queue_match_replay(match_id: int):
    cursor = db.cursor()
    cursor.execute('insert into match_queue values(?)', (match_id,))
    db.commit()


def get_queue():
    cursor = db.cursor()
    cursor.execute('select match_id from match_queue')
    queue_str = ''
    for item in cursor.fetchall():
        queue_str += str(item[0])
    return queue_str
