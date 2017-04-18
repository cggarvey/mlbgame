#!/usr/bin/env python

"""Module that is used for getting basic information about a game
such as the scoreboard and the box score.
"""

import mlbgame.data
import datetime


def process_scoreboard_game(game):
    o = {}  # output dictionary
    teams = game.findall('team')
    game_data = game.find('game')
    home_team_data = teams[0].find('gameteam')
    away_team_data = teams[1].find('gameteam')

    # generic processing for all games regardless of game status (tag)
    o['game_id'] = game_data.attrib['id']
    o['game_type'] = game.tag
    o['game_league'] = game_data.attrib['league']
    o['game_status'] = game_data.attrib['status']
    o['game_start_time'] = game_data.attrib['start_time']
    o['home_team'] = teams[0].attrib['name']
    o['home_team_runs'] = int(home_team_data.attrib['R'])
    o['home_team_hits'] = int(home_team_data.attrib['H'])
    o['home_team_errors'] = int(home_team_data.attrib['E'])
    o['away_team'] = teams[1].attrib['name']
    o['away_team_runs'] = int(away_team_data.attrib['R'])
    o['away_team_hits'] = int(away_team_data.attrib['H'])
    o['away_team_errors'] = int(away_team_data.attrib['E'])

    # specific processing based on the game's status
    if game.tag in ['ig_game', 'go_game']:
        o.update(process_scoreboard_game_win_loss(game))
    else:
        o.update(process_scoreboard_game_home_away(game))

    return o


def process_scoreboard_game_win_loss(game):
    # output dictionary. set up default values, then overwrite.
    o = {'w_pitcher': '',
         'w_pitcher_wins': 0,
         'w_pitcher_losses': 0,
         'l_pitcher': '',
         'l_pitcher_wins': 0,
         'l_pitcher_losses': 0,
         'sv_pitcher': '',
         'sv_pitcher_saves': 0}
    try:
        w_pitcher_data = game.find('w_pitcher')
        o['w_pitcher'] = w_pitcher_data.find('pitcher').attrib['name']
        o['w_pitcher_wins'] = int(w_pitcher_data.attrib['wins'])
        o['w_pitcher_losses'] = int(w_pitcher_data.attrib['losses'])
    except:
        pass
    try:
        l_pitcher_data = game.find('l_pitcher')
        o['l_pitcher'] = l_pitcher_data.find('pitcher').attrib['name']
        o['l_pitcher_wins'] = int(l_pitcher_data.attrib['wins'])
        o['l_pitcher_losses'] = int(l_pitcher_data.attrib['losses'])
    except:
        pass
    try:
        sv_pitcher_data = game.find('sv_pitcher')
        o['sv_pitcher'] = sv_pitcher_data.find('pitcher').attrib['name']
        o['sv_pitcher_saves'] = int(sv_pitcher_data.attrib['saves'])
    except:
        pass

    return o


def process_scoreboard_game_home_away(game):
    # output dictionary. set up default values, then overwrite.
    o = {'p_pitcher_home': '',
         'p_pitcher_home_wins': 0,
         'p_pitcher_home_losses': 0,
         'p_pitcher_away': '',
         'p_pitcher_away_wins': 0,
         'p_pitcher_away_losses': 0}
    try:
        p_pitcher_data = game.findall('p_pitcher')
        p_pitcher_home_data = p_pitcher_data[0]
        p_pitcher_away_data = p_pitcher_data[1]

        o['p_pitcher_home'] = p_pitcher_home_data.find('pitcher').attrib['name']
        o['p_pitcher_home_wins'] = int(p_pitcher_home_data.attrib['wins'])
        o['p_pitcher_home_losses'] = int(p_pitcher_home_data.attrib['losses'])

        o['p_pitcher_away'] = p_pitcher_away_data.find('pitcher').attrib['name']
        o['p_pitcher_away_wins'] = int(p_pitcher_away_data.attrib['wins'])
        o['p_pitcher_away_losses'] = int(p_pitcher_away_data.attrib['losses'])
    except:
        pass

    return o


def make_games_filter(teams):
    """Create closure function to filter scoreboard to relevant games."""
    def check_teams(x):

        if len(teams) == 0:  # no teams specified so we don't check the teams
            return True
        
        tms = x.findall('team')

        if len(tms) == 0:
            return False

        home = tms[0].attrib['name']
        away = tms[1].attrib['name']

        return len(set([home, away]).intersection(teams)) > 0

    return check_teams


def scoreboard(date, home=None, away=None):
    """Return the scoreboard information for games as a dictionary."""
    # get data
    data = mlbgame.data.get_scoreboard(date)
    teams = [x for x in [home, away] if x]
    games_filter = make_games_filter(teams)
    games_to_process = filter(games_filter, data)

    games = {}
    # loop through games
    for game in games_to_process:
        output = process_scoreboard_game(game)
        game_id = output['game_id']
        games[game_id] = output

    return games


class GameScoreboard(object):
    """Object to hold scoreboard information about a certain game."""

    def __init__(self, data):
        """Create a `GameScoreboard` object.

        data is expected to come from the `scoreboard()` function.
        """
        # loop through data
        for x in data:
            # set information as correct data type
            try:
                setattr(self, x, int(data[x]))
            except ValueError:
                try:
                    setattr(self, x, float(data[x]))
                except ValueError:
                    # string if not number
                    setattr(self, x, str(data[x]))
        # calculate the winning team
        if self.home_team_runs > self.away_team_runs:
            self.w_team = self.home_team
            self.l_team = self.away_team
        elif self.away_team_runs > self.home_team_runs:
            self.w_team = self.away_team
            self.l_team = self.home_team
        # create the datetime object for the game
        year, month, day, rest = self.game_id.split('_', 3)
        hour, other = self.game_start_time.split(':', 2)
        minute = other[:2]
        am_pm = other[2:]
        if am_pm == "PM":
            hour = int(hour) + 11
        self.date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))

    def nice_score(self):
        """Return a nicely formatted score of the game."""
        return '%s (%d) at %s (%d)' % (self.away_team, self.away_team_runs, self.home_team, self.home_team_runs)

    def __str__(self):
        return self.nice_score()

    def __repr__(self):
        return self.game_id


def box_score(game_id):
    """Get the box score information for the game with matching id."""
    # get data
    data = mlbgame.data.get_box_score(game_id)

    linescore = data.find('linescore')
    result = {}
    result['game_id'] = game_id
    # loop through innings and add them to output
    for x in linescore:
        inning = x.attrib['inning']
        home = x.attrib['home']
        away = x.attrib['away']
        result[int(inning)] = {'home': home, 'away': away}
    return result


class GameBoxScore(object):
    """Object to hold the box score of a certain game."""

    def __init__(self, data):
        """Create a `GameBoxScore` object.

        data is expected to come from the `box_score()` function.
        """
        self.data = data
        self.game_id = data['game_id']
        self.away = self.game_id[11:14]
        self.home = self.game_id[18:21]

        data.pop('game_id', None)
        # dictionary of innings
        self.innings = []
        # loops through the innings
        for x in sorted(data):
            try:
                result = {'inning': int(x),
                          'home': int(data[x]['home']),
                          'away': int(data[x]['away'])}
            # possible error when home team has 'x' becuase they did not bat
            except ValueError:
                result = {'inning': int(x),
                          'home': data[x]['home'],
                          'away': int(data[x]['away'])}
            self.innings.append(result)

    def __iter__(self):
        """Allow object to be iterated over."""
        for x in self.innings:
            yield x

    def print_scoreboard(self):
        """Print object as a scoreboard."""
        output = ''
        # parallel dictionaries with innings and scores
        innings = []
        away = []
        home = []
        for x in self:
            innings.append(x['inning'])
            away.append(x['away'])
            home.append(x['home'])
        # go through all the information and make a nice output
        # that looks like a scoreboard
        output += "Inning\t"
        for x in innings:
            output += str(x) + " "
        output += '\n'
        for x in innings:
            output += "---"
        output += "\nAway\t"
        for y, x in enumerate(away, start=1):
            if y >= 10:
                output += str(x) + "  "
            else:
                output += str(x) + " "
        output += "\nHome\t"
        for y, x in enumerate(home, start=1):
            if y >= 10:
                output += str(x) + "  "
            else:
                output += str(x) + " "
        return output


def overview(game_id):
    """Get the overview information for the game with matching id."""
    # get data
    data = mlbgame.data.get_overview(game_id)
    # parse data

    output = {}
    # get overview attributes
    for x in data.attrib:
        output[x] = data.attrib[x]
    return output


class Overview(object):
    """Object to hold an overview of game information.

    `elements` property is a set of all properties that an object contains.
    """

    def __init__(self, data):
        """Create an overview object that matches the corresponding info in `data`.

        `data` should be an dictionary of values.
        """
        element_list = []
        # loop through data
        for x in data:
            # set information as correct data type
            try:
                setattr(self, x, int(data[x]))
            except ValueError:
                try:
                    setattr(self, x, float(data[x]))
                except ValueError:
                    # string if not number
                    setattr(self, x, str(data[x]))
            element_list.append(x)
        self.elements = set(element_list)
