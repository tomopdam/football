import psycopg2

host = 'db' # script is run on the web container, postgres is on db container
port = '5432'
dbname = 'postgres'
user = 'postgres'
password = 'postgres'

conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)

cur = conn.cursor()

# note we exclude players with cost == 0 as there's something weird going on there
cur.execute('SELECT players.id,players.overall,players.group,(players.wage+players.release_clause) AS cost from players WHERE (players.wage+players.release_clause) > 0 ORDER BY cost, overall DESC')


players = cur.fetchall()

cur.close()
conn.close()


class Team:
    def __init__(self, budget):
        self.budget = budget
        self.total_cost = 0
        self.total_overall = 0
        self.players = set({})
        self.groups = {
            'GK' : [TeamPlayer() for _ in range(1)],
            'FB' : [TeamPlayer() for _ in range(2)],
            'HB' : [TeamPlayer() for _ in range(3)],
            'FP' : [TeamPlayer() for _ in range(5)]
        }

    def add_player(self, player, sort_by):
        # get player group
        target_group = player.group
        # get last player- note it's always sorted by overall (i.e. score) DESC
        player_to_replace = self.groups[target_group][-1]
        # swap players
        self.groups[target_group][-1] = player
        # update totals
        self.total_cost = self.total_cost - player_to_replace.cost + player.cost
        self.total_overall = self.total_overall - player_to_replace.overall + player.overall
        # re-order that group
        if sort_by == 'overall':
            self.groups[target_group] = sorted(self.groups[target_group], key=lambda k: k.overall, reverse=True)
        elif sort_by == 'cost':
            self.groups[target_group] = sorted(self.groups[target_group], key=lambda k: k.cost, reverse=True)
        # update the set to ensure we don't add the same player multiple times
        if player_to_replace.id != 0:
            self.players.remove(player_to_replace.id)
        self.players.add(player.id)

    def output(self):
        for group, players in self.groups.items():
            for player in players:
                print(f"id {player.id}, group: {player.group}, cost: {player.cost}, overall: {player.overall}")
        print(self.players)
        print(f"Total cost: {self.total_cost}")
        print(f"Total score: {self.total_overall}")



class TeamPlayer:
    def __init__(self, player=None):
        # initial population of empty team
        if player is None:
            self.id = 0
            self.overall = 0
            self.group = '_'
            self.cost = 0
        else:
            # (0,1,2,3) -> id, overall, group, cost
            self.id = player[0]
            self.overall = player[1]
            self.group = player[2]
            self.cost = player[3]

def build_team(budget, players):
    team = Team(budget=budget)

    # first we pre-fill the team with the cheapest possible players
    # for each position, to ensure we always have a full roster

    # players is already sorted by cost ASC from DB query

    goalkeepers = [ x for x in players if x[2] == 'GK']
    for i in range(1):
        team.add_player(player=TeamPlayer(goalkeepers[i]), sort_by='overall')

    fullbacks = [ x for x in players if x[2] == 'FB']
    for i in range(2):
        team.add_player(player=TeamPlayer(fullbacks[i]), sort_by='overall')

    halfbacks = [ x for x in players if x[2] == 'HB']
    for i in range(3):
        team.add_player(player=TeamPlayer(halfbacks[i]), sort_by='overall')

    forwardplayers = [ x for x in players if x[2] == 'FP']
    for i in range(5):
        team.add_player(player=TeamPlayer(forwardplayers[i]), sort_by='overall')

    print(team.output())

    # now we have a base team of cheap players, optimise

    # iterate through players (by ascending score)
    # and add to team if within total budget
    players = sorted(players, key=lambda k: k[1])
    for player in players:
        new_player = TeamPlayer(player)
        if new_player.id in team.players:
            continue
        if (team.total_cost + new_player.cost - team.groups[new_player.group][-1].cost <= budget 
            and new_player.overall > team.groups[new_player.group][-1].overall):
            team.add_player(player=new_player, sort_by='overall')

    team.output()

    return team


final_team = build_team(100000, players)
