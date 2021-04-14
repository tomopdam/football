import csv
from decimal import Decimal

# currency_string e.g. €110.5M, €525.5K, €100K, €0, ''
def currency_string_to_integer(currency_string):
    multiples = { 'M' : 1000000, 'K' : 1000 }
    output = 0
    
    if currency_string in ['€0', '']:
        return output

    # strip currency symbol
    if currency_string[:1] == '€':
        base = currency_string[1:] # e.g. €525.5K -> 525.5K -> 525500000
    # ends in K or M?
    if base[-1:] in multiples.keys():
        output = int(Decimal(base[:-1]) * multiples[base[-1:]])
    else:
        output = int(base)

    return output
    
# convert position to group for faster/cleaner group checking later
def position_to_group(position):
    # note: spec def and website ref were missing some entries:
    # RF, ST, LW, LF, RS, LS, RW, '', all of which I assigned to FP
    # as FP also includes midfielders.. I hope the '' players like to run
    
    # goalkeeper
    if position in ['GK']:
        return 'GK'
    # fullback
    if position in ['LB', 'RB', 'LWB', 'RWB']:
      return 'FB'
    # halfback
    if position in ['CB', 'LCB', 'RCB', 'CDM', 'LDM', 'RDM', 'CM', 'LCM', 'RCM', 'LM', 'RM']:
      return 'HB'
    # forward playing
    if position in ['CAM', 'LAM', 'RAM', 'LWF', 'RWF', 'CF', 'LCF', 'RCF', 'RF', 'ST', 'LW', 'LF', 'RS', 'LS', 'RW', '']:
      return 'FP'
    # by default, push to forward playing
    return 'FP'

# imports full playerset from csv, formats values e.g. wage and position, returns list of dicts
def import_from_csv(config):
    required_keys = ['csv_filename', 'csv_encoding', 'csv_delim', 'cols_to_import', 'currency_string_cols']
    if not all(key in config.keys() for key in required_keys):
        raise KeyError("import_from_csv config is missing required key(s).")
    
    try:
        players = []
        with open(config['csv_filename'], 'r', encoding=config['csv_encoding']) as csv_file:
            # map columns
            reader = csv.DictReader(csv_file, delimiter=config['csv_delim'])
            for row in reader:
                player = {}
                for old_key, new_key in config['cols_to_import'].items():
                    player[new_key] = row[old_key]
                    # format values
                    if new_key in config['currency_string_cols']:
                        # convert currency string into simple integer
                        player[new_key] = currency_string_to_integer(player[new_key])
                # group players according to position
                player['group'] = position_to_group(player['position'])
                players.append(player)
            return players
    except:
        raise Exception("Could not import from csv")
       
