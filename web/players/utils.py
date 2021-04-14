# Utility file for player related code

# used by find_optimal_team() to track values
class Team:
    def __init__(self, budget):
        self.budget = budget
        self.total_cost = 0
        self.total_overall = 0
        self.players = set({})
        # pre-populate the group lists with empty players to avoid index issues
        self.groups = {
            'GK' : [TeamPlayer() for _ in range(1)],
            'FB' : [TeamPlayer() for _ in range(2)],
            'HB' : [TeamPlayer() for _ in range(3)],
            'FP' : [TeamPlayer() for _ in range(5)]
        }

    def find_player_to_replace_with(self, new_player):
        # returns a player that will be replaced by the new player

        # get player group
        target_group = new_player.group
        # get last player- note it's always sorted by overall (i.e. score) DESC
        player_to_replace = self.groups[target_group][-1]
        return player_to_replace

    def add_player(self, player, sort_by):
        if player.id in self.players:
            return ValueError(f"Cannot add the same player twice to the same team: {player.name}")

        # get player group
        target_group = player.group

        # get last player- note it's always sorted by overall (i.e. score) DESC
        player_to_replace = self.find_player_to_replace_with(player)

        # swap players
        self.groups[target_group][-1] = player

        # update totals
        self.total_cost = self.total_cost - player_to_replace.cost + player.cost
        self.total_overall = self.total_overall - player_to_replace.overall + player.overall

        # re-order that group in descending order
        if sort_by == 'overall':
            self.groups[target_group] = sorted(self.groups[target_group], key=lambda k: k.overall, reverse=True)
        elif sort_by == 'cost':
            self.groups[target_group] = sorted(self.groups[target_group], key=lambda k: k.cost, reverse=True)

        # update the set to ensure we don't add the same player multiple times
        if player_to_replace.id != 0:
            self.players.remove(player_to_replace.id)
        self.players.add(player.id)


# used by find_optimal_team()
class TeamPlayer:
    def __init__(self, player=None):
        # used for initial population of empty team
        if player is None:
            self.id = 0
            self.overall = 0
            self.group = '_'
            self.cost = 0
        else:
            self.id = player.id
            self.overall = player.overall
            self.group = player.group
            self.cost = player.cost

def find_optimal_team(budget, players):
    team = Team(budget=budget)

    # first we pre-fill the team with the cheapest possible players
    # for each position, to ensure we always have a full roster

    # players is already sorted by cost ASC from DB query

    times_to_fill = {
        'GK' : 1,
        'FB' : 2,
        'HB' : 3,
        'FP' : 5
    }

    for group, times in times_to_fill.items():
        # select the cheapest players from each position group
        initial_players = players.filter(group=group)[:times]
        for group_player in initial_players:
            team.add_player(player=TeamPlayer(group_player), sort_by='cost')
    
    # now we have a base team of cheap players, optimise

    # iterate through players and add to team if:
    # - would still be within total budget
    # - has a higher score than the player they're replacing
    # (player to replace= player with lowest score for that position group)
    for player in players:
        # can't add the same player twice
        if player.id in team.players:
            continue

        new_player = TeamPlayer(player)

        player_to_replace = team.find_player_to_replace_with(new_player)

        # if new team format is within budget and if overall score improves, add the player
        try: 
            if ((team.total_cost + new_player.cost - player_to_replace.cost) <= budget 
                and (new_player.overall > player_to_replace.overall)
                ):
                team.add_player(player=new_player, sort_by='overall')
        except ValueError:
            # skip player - no need for a hard error
            continue


    return team