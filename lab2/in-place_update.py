import psycopg2
from threading import Thread
from time import perf_counter
import os

user_id = 2

DB_NAME = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')

# basic preparation
conn = psycopg2.connect(dbname=DB_NAME, host=HOST, user=USER, password=PASSWORD)
cur = conn.cursor()
cur.execute(f'update user_counter set counter = 0 where user_id = {user_id}')
conn.commit()
cur.close()


# in-place update
def change_counter():
    cur = conn.cursor()
    for t in range(0, 10000):
        cur.execute(f"update user_counter set counter = counter + 1 where user_id = {user_id}")
        conn.commit()
    cur.close()


threads = [Thread(target=change_counter)
           for t in range(0, 10)]

# start performance check
start_time = perf_counter()

# do our stuff
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end_time = perf_counter()

cur = conn.cursor()
cur.execute(f"SELECT counter FROM user_counter WHERE user_id = {user_id};")
print(f'Final counter value: {cur.fetchone()[0]}')
print(f'Final execution time: {end_time- start_time: 0.2f} seconds')

cur.close()
conn.close()
