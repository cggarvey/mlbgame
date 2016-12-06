#!/usr/bin/env python

"""Module that controls getting stats and creating objects to hold that information."""

import mlbgame.data
import mlbgame.object


def process_players(data, role):
    home = list()
    away = list()
    for row in data:
        # checks if home team
        is_home = False
        if row.attrib['team_flag'] == "home":
            is_home = True
        # loops through players
        for x in row.findall(role):
            stats = {i: x.attrib[i] for i in x.attrib}
            # apply to correct list
            if is_home:
                home.append(stats)
            else:
                away.append(stats)
    return home, away


def player_stats(game_id):
    """Return dictionary of individual stats of a game with matching id."""
    # get data from data module
    data = mlbgame.data.get_box_score(game_id)

    # get pitching and batting info
    pitching = data.findall('pitching')
    batting = data.findall('batting')

    # loop through and process
    home_pitching, away_pitching = process_players(pitching, 'pitcher')
    home_batting, away_batting = process_players(batting, 'batter')

    # put lists in dictionary for output
    output = {'home_pitching': home_pitching,
              'away_pitching': away_pitching,
              'home_batting': home_batting,
              'away_batting': away_batting}
    return output


def process_teams(data, role):
    output = {}
    records = data.findall(role)
    home_key = 'home_{0}'.format(role)
    away_key = 'away_{0}'.format(role)

    for x in records:
        stats = {}
        # loop through stats and save
        for y in x.attrib:
            stats[y] = x.attrib[y]
        # apply to correct team
        if x.attrib['team_flag'] == 'home':
            output[home_key] = stats
        elif x.attrib['team_flag'] == 'away':
            output[away_key] = stats
    return output


def team_stats(game_id):
    """Return team stats of a game with matching id."""
    # get data from data module
    data = mlbgame.data.get_box_score(game_id)
    output = {}

    # get pitching and batting ingo
    pitching = process_teams(data, 'pitching')
    batting = process_teams(data, 'batting')
    # dictionary for output
    # loop through pitching info
    output.update(pitching)
    output.update(batting)

    return output


class PitcherStats(mlbgame.object.Object):
    """Holds stats information for a pitcher.

    Check out `statmap.py` for a full list of object properties.
    """

    def nice_output(self):
        """Prints basic pitcher stats in a nice way."""
        out = "{0} - {1} Earned Runs, {2} Strikouts, {3} Hits"
        return out.format(self.name_display_first_last, self.er, self.so, self.h)

    def __str__(self):
        return self.nice_output()


class BatterStats(mlbgame.object.Object):
    """Holds stats information for a batter.

    Check out `statmap.py` for a full list of object properties.
    """

    def nice_output(self):
        """Prints basic batter stats in a nice way."""
        if self.rbi > 0:
            if self.hr > 0:
                # display home runs if he has any
                out = "{0} - {1} for {2} with {3} RBI and {4} Home Runs"
            else:
                out = "{0} - {1} for {2} with {3} RBI"
            # display RBI if he has any but no HR
        # display basic game stats
        else:
            out = "{0} - {1} for {2}"

        return out % (self.name_display_first_last, self.h, self.ab, self.rbi, self.hr)

    def __str__(self):
        return self.nice_output()


class TeamStats(mlbgame.object.Object):
    """Holds total pitching or batting stats for a team"""
    # basically a copy of the object class with a different name for clarification
    pass
