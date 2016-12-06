import pytest
import mlbgame.game
import datetime

date = datetime.date(2016, 11, 2)


@pytest.fixture(scope='session')
def xml_scoreboard():
    # returns a parsed xml document for 11/2/2016 -- World Series G7
    return mlbgame.data.get_scoreboard(date)


@pytest.fixture(scope='session')
def scoreboard():
    # return a dict of format game_id --> dict of game attributes
    return mlbgame.game.scoreboard(date)


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
    assert sb['game_id'] == '2016_11_02_chnmlb_clemlb_1'
    assert sb['game_type'] == 'go_game'
    assert sb['game_league'] == 'NA'
    assert sb['game_status'] == 'FINAL'
    assert sb['game_start_time'] == '8:00PM'
    assert sb['home_team'] == 'Indians'
    assert sb['home_team_runs'] == 7
    assert sb['home_team_hits'] == 11
    assert sb['home_team_errors'] == 1
    assert sb['away_team'] == 'Cubs'
    assert sb['away_team_runs'] == 8
    assert sb['away_team_hits'] == 13
    assert sb['away_team_errors'] == 3
    assert sb['l_pitcher'] == 'B. Shaw'
    assert sb['l_pitcher_losses'] == 1
    assert sb['l_pitcher_wins'] == 0
    assert sb['sv_pitcher'] == 'M. Montgomery'
    assert sb['sv_pitcher_saves'] == 1
    assert sb['w_pitcher'] == 'A. Chapman'
    assert sb['w_pitcher_losses'] == 0
    assert sb['w_pitcher_wins'] == 1


def test_process_scoreboard_game():
    pass

if __name__ == '__main__':
    pass