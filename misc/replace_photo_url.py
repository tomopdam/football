import requests
import psycopg2
import csv
from datetime import datetime

host = 'db' # script is run on the web container, postgres is on db container
port = '5432'
dbname = 'postgres'
user = 'postgres'
password = 'postgres'

conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)

new_photo_urls_csv = csv.DictReader(open("photo_check.csv", encoding="utf-8"))

new_photo_urls = []

for row in new_photo_urls_csv:
    new_photo_urls.append(row)

update_sql_exists = """UPDATE players
    SET photo = %s
    WHERE id_ext = %s"""

update_sql_doesnt_exist = """UPDATE players
    SET photo_exists = FALSE
    WHERE id_ext = %s"""

cur = conn.cursor()

for photo in new_photo_urls:
    if photo['exists'] == "True":
        continue
    #    cur.execute(update_sql, (photo['photo_url'],str(photo['id_ext'])))
    elif photo['exists'] == "False":
        cur.execute(update_sql_doesnt_exist, (str(photo['id_ext']), ))

conn.commit()

cur.close()
conn.close()

