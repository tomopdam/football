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

cur = conn.cursor()

# get all player ids and photo urls
cur.execute('SELECT players.id_ext from players')

players = cur.fetchall()

cur.close()
conn.close()

def photo_exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def build_url(id_ext, attempt):
    id_ext = str(id_ext).zfill(6)
    if attempt==0:
      return 'https://cdn.sofifa.com/players/'+id_ext[:3]+'/'+id_ext[3:]+'/21_120.png'
    else:
      return 'https://cdn.sofifa.com/players/'+id_ext[:3]+'/'+id_ext[3:]+'/19_120.png'

def time_now():
    return str(datetime.now())

already_checked_csv = csv.DictReader(open("photo_check.csv", encoding="utf-8"))

results = []

players_to_skip = []

for player in already_checked_csv:
    results.append(player)
    players_to_skip.append(player['id_ext'])

print(f"Skipping {len(players_to_skip)} rows that are already OK.")


count = 0
print(time_now() + "-- started.")
# set limits on the array to do it manually in batches
# script won't lose existing data, or re-check
for player in players:
    id_ext = player[0]
    if str(id_ext) in players_to_skip:
      continue

    photo_url = build_url(id_ext=id_ext, attempt=0)
    exists = photo_exists(photo_url)
    if exists==False:
      # try alternative configuration
      photo_url = build_url(id_ext=id_ext, attempt=1)
      exists = photo_exists(photo_url)
      if (exists == False):
        photo_url = 'https://cdn.sofifa.com/players/notfound_0_120.png'
    results.append({
      'id_ext' : id_ext,
      'photo_url' : photo_url,
      'exists' : exists
    })
    count += 1
    if (count % 50 == 0):
      print(time_now() + "-- checked a batch of 50.")
print(time_now() + "-- finished.")

if results:
  with open('photo_check.csv', 'w', encoding='utf-8') as temp_csv_file:
      headers = list(results[0].keys())
      writer = csv.DictWriter(temp_csv_file, delimiter=',', fieldnames=headers)
      writer.writeheader()
      writer.writerows(results)