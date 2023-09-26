import psycopg2

conn = psycopg2.connect(dbname="postgres", host="192.168.1.23", user="meow", password="meowmeow")
cur = conn.cursor()
#cur.execute("CREATE TABLE user_counter (USER_ID serial PRIMARY KEY, counter integer, version integer);")
cur.execute("INSERT INTO user_counter (counter, version) VALUES (%s, %s)", (0, 0))

conn.commit()
cur.close()
conn.close()
