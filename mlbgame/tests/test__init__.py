
import pytest
import mlbgame


def test_init_day():
    results = mlbgame.day(2016, 10, 2)
    assert isinstance(results, list)
    assert len(results) == 15
    assert all(map(lambda x: isinstance(x, mlbgame.game.GameScoreboard), results))


def test_init_impossible_day():
    # verify that a date that couldn't exist (e.g. October 32nd) returns [].
    results = mlbgame.day(2016, 10, 32)
    assert isinstance(results, list)
    assert len(results) == 0


def test_init_games():
    results = mlbgame.games(2016, 10, None, "Cubs", "Cubs")
    assert isinstance(results, list)
    assert all(map(lambda x: isinstance(x, list), results))
    assert len(results) == 17


def test_init_league():
    lg = mlbgame.league()

    assert lg.club == 'mlb'
    assert lg.club_full_name == 'Major League Baseball'
    assert lg.display_code == 'mlb'
    assert lg.url_prod == 'www.mlb.com'
