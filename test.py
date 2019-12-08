import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

users = [
    (1, 'kunal', 'asdf'),
    (2, 'jose', 'qwer'),
    (3, 'seema', 'hjkl'),

]

insert_query = "INSERT INTO users values(?, ?, ?)"

cursor.executemany(insert_query, users)

select_query = "SELECT * FRoM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
