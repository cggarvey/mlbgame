import pytest
import mlbgame


@pytest.fixture(scope='session')
def league_info():
    return mlbgame.info.league_info()


@pytest.fixture(scope='session')
def team_info():
    return mlbgame.info.team_info()


@pytest.fixture(scope='session')
def dbacks(team_info):
    for team_dict in team_info:
        if team_dict['club'] == 'ari':
            info_obj = mlbgame.info.Info(team_dict)
    return info_obj


def test_league_info(league_info):

    assert isinstance(league_info, dict)
    assert league_info['club'] == 'mlb'
    assert league_info['club_full_name'] == 'Major League Baseball'
    assert league_info['display_code'] == 'mlb'
    assert league_info['id'] == '35003'
    assert league_info['url_prod'] == 'www.mlb.com'


def test_team_info(team_info):
    assert isinstance(team_info, list)
    assert len(team_info) >= 30


def test_info_init_setattr(dbacks):

    assert dbacks.club == 'ari'
    assert dbacks.club_common_name == 'D-backs'
    assert dbacks.club_full_name == 'Arizona Diamondbacks'


def test_info_nice_output(dbacks):
    assert dbacks.nice_output() == 'Arizona Diamondbacks (ARI)'
    assert str(dbacks) == 'Arizona Diamondbacks (ARI)'


if __name__ == '__main__':
    pass
