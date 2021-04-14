# coding=utf-8

"""
Simple script to check data types for building player table.
Checks:
- max string lengths
- max integer length for currency values (e.g. €110.5M -> 110500000)
"""

import csv
from decimal import Decimal

length_cols = [
  'ID',
  'Name',
  'Age',
  'Photo',
  'Nationality',
  'Club',
  'Overall',
  'Position'
]

decimal_cols = [
  'Value',
  'Wage',
  'Release Clause'
]

# note: if later we need to handle multiple currencies, \p{Sc} is available via regex (i.e. not basic re)
# but source file has everything standardised to Euros
# multiply base number by
multiples = { 'M' : 1000000, 'K' : 1000 }

tracked_lengths = {}
tracked_strings = {}

# not all positions are listed in the specs
list_of_positions = []

# track max values
for col in length_cols:
   tracked_lengths[col] = 0
   tracked_strings[col] = ""
max_currency_integer = 0

with open('data.csv', 'r', encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=',')
    for row in reader:
        if row['Position'] not in list_of_positions:
            list_of_positions.append(row['Position'])
        for col in length_cols:
            if len(row[col]) > tracked_lengths[col]:
                print(f"Updated {col}: new length {len(row[col])} -> {row[col]}")
                tracked_lengths[col] = len(row[col])
                tracked_strings[col] = row[col]
        for col in decimal_cols:
            # e.g. €110.5M, €525.5K, €100K, €0, ''
            final = 0
            if row[col] in ['€0', '']:
                continue
            raw = row[col][1:] # e.g. €525.5K -> 525.5K
            if raw[-1:] in multiples.keys():
                final = int(Decimal(raw[:-1]) * multiples[raw[-1:]])
            else:
                final = int(raw)
            # now check max length
            if final > max_currency_integer:
                print(f"New max currency value: {final}")
                max_currency_integer = final
            
                
print(f"\nResults:")
for col in length_cols:
    print(f"{col}: {tracked_lengths[col]} -> {tracked_strings[col]}")
print(f"Max currency: {max_currency_integer}")

print(list_of_positions)
    
