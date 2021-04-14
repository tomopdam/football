import csv
from io import StringIO

import psycopg2

from import_lib import import_from_csv

# db settings
host = 'db' # script is run on the web container, postgres is on db container
port = '5432'
dbname = 'postgres'
user = 'postgres'
password = 'postgres'



# settings for csv import of player list - see: import_lib.import_from_csv

csv_import_config = {
    'csv_filename' : 'data.csv',
    'csv_encoding' : 'utf-8',
    'csv_delim' : ',',
    'cols_to_import' : {
    	"ID" : "id_ext", 
    	"Name" : "name",
    	"Age" : "age", 
    	"Photo" : "photo", 
    	"Nationality" : "nationality", 
    	"Club" : "club", 
    	"Overall" : "overall", 
    	"Value" : "value", 
    	"Wage" : "wage", 
    	"Position" : "position", 
    	"Release Clause" : "release_clause"
    },
    'currency_string_cols' : [
        'wage', 
        'value', 
        'release_clause'
    ]
}

try:
    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
    
    # get player list to import
    
    players = import_from_csv(csv_import_config)
    
    # write to buffered csv for psycopg2's copy_from
    
    temp_csv_file = StringIO()
    headers = list(players[0].keys())
    writer = csv.DictWriter(temp_csv_file, delimiter=csv_import_config['csv_delim'], fieldnames=headers)

    writer.writerows(players)
    
    temp_csv_file.seek(0)
    
    # insert into players_temp
    cur = conn.cursor()

    cur.copy_from(temp_csv_file, 'players', sep=csv_import_config['csv_delim'])
    cur.close()
    conn.commit()
    temp_csv_file.close()
    
    
    
    print("Executed all queries.")	
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    

