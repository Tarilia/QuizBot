import os

import aiosqlite
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')


def db_connection(func):
    async def wrapper(*args, **kwargs):
        async with aiosqlite.connect(DB_NAME) as db:
            result = await func(db, *args, **kwargs)
            await db.commit()
            return result
    return wrapper


@db_connection
async def create_table(db):
    await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state
                     (user_id INTEGER PRIMARY KEY,
                      question_index INTEGER)''')
    await db.execute('''CREATE TABLE IF NOT EXISTS user_scores
                     (user_id INTEGER PRIMARY KEY, score INTEGER)''')


@db_connection
async def get_quiz_index(db, user_id):
    async with db.execute('SELECT question_index FROM quiz_state WHERE'
                          ' user_id = (?)', (user_id,)) as cursor:
        results = await cursor.fetchone()
        if results is not None:
            return results[0]
        else:
            return 0


@db_connection
async def update_quiz_index(db, user_id, index):
    await db.execute('INSERT OR REPLACE INTO quiz_state'
                     ' (user_id, question_index)'
                     ' VALUES (?, ?)', (user_id, index))


@db_connection
async def reset_user_score(db, user_id):
    await db.execute('INSERT OR REPLACE INTO user_scores'
                     ' (user_id, score) VALUES (?, 0)',
                     (user_id, ))


@db_connection
async def get_user_score(db, user_id):
    async with db.execute('SELECT score FROM user_scores'
                          ' WHERE user_id = ?',
                          (user_id,)) as cursor:
        result = await cursor.fetchone()
        return result[0] if result else None


@db_connection
async def update_user_score(db, user_id, is_correct):
    async with db.execute('SELECT score FROM user_scores'
                          ' WHERE user_id = ?',
                          (user_id, )) as cursor:
        result = await cursor.fetchone()
        score = result[0] if result else 0
        if is_correct:
            score = score + 1 if score else 1
        await db.execute('INSERT OR REPLACE INTO user_scores'
                         ' (user_id, score) VALUES (?, ?)',
                         (user_id, score))
