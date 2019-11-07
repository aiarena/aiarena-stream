import sqlite3

database_file = "data.db"
db = sqlite3.connect(database_file)


def create_db():
    cursor = db.cursor()
    cursor.execute('CREATE TABLE match_queue(match_id INTEGER)')
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
        queue_str += str(item[0]) + ' '
    return queue_str


def queue_pop_next_match():
    cursor = db.cursor()
    cursor.execute('select match_id from match_queue limit 1')
    row = cursor.fetchone()
    if row is None:  # there is no queued matches
        return None

    match_id = row[0]
    cursor.execute('delete from match_queue where match_id = ?', (match_id,))
    db.commit()
    return str(match_id)


if __name__ == "__main__":
    create_db()
