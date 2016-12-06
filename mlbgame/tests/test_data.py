
import os
import lxml
import pytest
import datetime
import mlbgame.data


date = datetime.date(2016, 11, 2)


def test_valid_rootdir():
    assert os.path.exists(mlbgame.data.ROOT_DIR)


def test_access_error():
    path = '/bogus/path/to/something'
    with pytest.raises(IOError):
        mlbgame.data.access_error(path)


def test_unpack_ymd_ints():
    y, m, d = mlbgame.data.unpack_ymd(date)
    assert y == 2016
    assert m == 11
    assert d == 2


def test_unpack_ymd_str():
    y, m, d = mlbgame.data.unpack_ymd(date, string=True)
    assert y == '2016'
    assert m == '11'
    assert d == '02'


def test_date_from_gameid():
    gid = '2016_11_02_chnmlb_clemlb_1'
    date = mlbgame.data.date_from_gameid(gid)
    assert date.year == 2016
    assert date.month == 11
    assert date.day == 2


def test__get_url():
    url = mlbgame.data._get_url(date, 'scoreboard.xml')
    assert url == 'http://gd2.mlb.com/components/game/mlb/year_2016/month_11/day_02/scoreboard.xml'


def test__get_path():
    path = mlbgame.data._get_path(date, 'scoreboard.xml')
    assert path[-41:] == "/year_2016/month_11/day_02/scoreboard.xml"
    assert os.path.exists(os.path.dirname(path))


def test__get_dir():
    path = mlbgame.data._get_dir(date)
    assert path[-26:] == "/year_2016/month_11/day_02"
    assert os.path.exists(os.path.dirname(path))


def test_get_data_nocache():
    data = mlbgame.data.get_data(date, 'scoreboard.xml', gz=False, no_cache=True)
    assert isinstance(data, lxml.etree._Element)


def test_get_data_nocache_gz():
    data = mlbgame.data.get_data(date, 'scoreboard.xml', gz=True, no_cache=True)
    assert isinstance(data, lxml.etree._Element)


def test_get_data_cache():
    data = mlbgame.data.get_data(date, 'scoreboard.xml', gz=False)
    assert isinstance(data, lxml.etree._Element)


def test_get_data_cache_gz():
    data = mlbgame.data.get_data(date, 'scoreboard.xml', gz=True)
    assert isinstance(data, lxml.etree._Element)


