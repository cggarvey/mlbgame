"""Unit tests of mlbgame.game module."""
import pytest
import mlbgame.game
import datetime
import lxml

date = datetime.date(2016, 11, 2)
game_id = '2016_11_02_chnmlb_clemlb_1'


@pytest.fixture(scope='session')
def xml_scoreboard():
    # returns a parsed xml document for 11/2/2016 -- World Series G7
    return mlbgame.data.get_scoreboard(date)


@pytest.fixture(scope='session')
def scoreboard():
    # return a dict of format game_id --> dict of game attributes
    return mlbgame.game.scoreboard(date)


@pytest.fixture(scope='session')
def xml_boxscore():
    # returns a parsed xml document for 11/2/2016 -- World Series G7
    return mlbgame.data.get_box_score(game_id)


@pytest.fixture(scope='session')
def boxscore():
    return mlbgame.game.box_score(game_id)


def test_make_games_filter_results(xml_scoreboard):
    assert len(xml_scoreboard) == 1
    teams = ['Cubs', 'Indians']
    games_filter = mlbgame.game.make_games_filter(teams)
    filtered = filter(games_filter, xml_scoreboard)
    assert len(list(filtered)) == 1


def test_make_games_filter_noresults(xml_scoreboard):
    assert len(xml_scoreboard) == 1
    teams = ['Reds', 'Blue Jays']
    games_filter = mlbgame.game.make_games_filter(teams)
    filtered = filter(games_filter, xml_scoreboard)
    assert len(list(filtered)) == 0


def test_scoreboard(scoreboard):
    sb = scoreboard['2016_11_02_chnmlb_clemlb_1']

    target = {'game_id': '2016_11_02_chnmlb_clemlb_1',
              'game_type': 'go_game',
              'game_league': 'NA',
              'game_status': 'FINAL',
              'game_start_time': '8:00PM',
              'home_team': 'Indians',
              'home_team_runs': 7,
              'home_team_hits': 11,
              'home_team_errors': 1,
              'away_team': 'Cubs',
              'away_team_runs': 8,
              'away_team_hits': 13,
              'away_team_errors': 3,
              'l_pitcher': 'B. Shaw',
              'l_pitcher_losses': 1,
              'l_pitcher_wins': 0,
              'sv_pitcher': 'M. Montgomery',
              'sv_pitcher_saves': 1,
              'w_pitcher': 'A. Chapman',
              'w_pitcher_losses': 0,
              'w_pitcher_wins': 1}
    assert target == sb


def test_process_scoreboard_game():
    pass


def test_xml_boxscore(xml_boxscore):
    assert isinstance(xml_boxscore, lxml.etree._Element)
    assert xml_boxscore.tag == 'boxscore'


def test_boxscore(boxscore):
    # verify that what we receive is exactly what we want to see
    target = {1: {'away': '1', 'home': '0'},
              2: {'away': '0', 'home': '0'},
              3: {'away': '0', 'home': '1'},
              4: {'away': '2', 'home': '0'},
              5: {'away': '2', 'home': '2'},
              6: {'away': '1', 'home': '0'},
              7: {'away': '0', 'home': '0'},
              8: {'away': '0', 'home': '3'},
              9: {'away': '0', 'home': '0'},
              10: {'away': '2', 'home': '1'},
              'game_id': '2016_11_02_chnmlb_clemlb_1'}
    assert boxscore == target

if __name__ == '__main__':
    pass