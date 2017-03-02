#!/usr/bin/env python

"""This module gets the XML data that other functions use.
It checks if the data is cached first, and if not,
gets the data from mlb.com.
"""

import os
import requests
import gzip
from lxml import etree
import datetime
import tempfile


ROOT_URL = "http://gd2.mlb.com/components/game/mlb"
ROOT_DIR = os.path.join(os.path.dirname(__file__), "gameday-data")
TEMP_DIR = tempfile.gettempdir()


def access_error(name):
    """Display error message when program cannot write to file."""
    print('I do not have write access to "%s".' % (name))
    print('Without write access, I cannot update the game database.')
    raise IOError


def unpack_ymd(date, string=False):
    """Calculate year, month, day components from datetime.date."""
    if not string:
        return date.year, date.month, date.day
    else:
        return str(date.year), str(date.month).zfill(2), str(date.day).zfill(2)


def date_from_gameid(game_id):
    """Calculate datetime.date from game_id."""
    y, m, d, _ = game_id.split('_', 3)
    year = int(y)
    month = int(m)
    day = int(d)

    return datetime.date(year, month, day)


def get_data(date, file, gid=None, gz=False, no_cache=False):
    """Get xml (cached file if possible), parse w/ lxml, and return result."""
    file_path = _get_path(date, file, gid, gz)

    if not os.path.isfile(file_path) or no_cache:
        success = download_xml(date, file, gid, gz)
        if not success:
            return False

    if gz:
        raw = read_xml_from_gzip(file_path)
    else:
        raw = read_xml_from_file(file_path)
    parsed = etree.XML(raw.encode())

    return parsed


def _get_url(date, file, gid=None):
    """Return a url for the required resource."""
    base = "{0}/year_{1}/month_{2}/day_{3}/{4}"
    y, m, d = unpack_ymd(date, string=True)

    if gid:
        end = "gid_{0}/{1}".format(gid, file)
    else:
        end = file

    return base.format(ROOT_URL, y, m, d, end)


def _get_path(date, file, gid=None, gz=False):
    """Find a local path for the required resource."""
    base_dir = _get_dir(date, gid)

    if gz:
        file = "{0}.gz".format(file)

    return os.path.join(base_dir, file)


def _get_dir(date, gid=None):
    """Find a local path for the required resource."""
    y, m, d = unpack_ymd(date, string=True)
    ymd = "year_{0}/month_{1}/day_{2}".format(y, m, d)

    date_dir = os.path.join(ROOT_DIR, ymd)

    if gid:
        path = os.path.join(date_dir, 'gid_{0}'.format(gid))
    else:
        path = os.path.join(date_dir)

    return mkdir(path)


def mkdir(dir_path):
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            access_error(dir_path)
            return False
    return dir_path


def download_xml(date, file, gid, gz):
    url = _get_url(date, file, gid)
    resp = requests.get(url)
    raw = resp.text
    if resp.status_code == requests.codes.ok:
        save_xml(raw, date, file, gid, gz)
        return True
    else:
        return False


def save_xml(xml, date, file, gid=None, gz=False):

    file_path = _get_path(date, file, gid, gz)
    try:
        if gz:
            write_xml_to_gzip(xml, file_path)
        else:
            write_xml_to_file(xml, file_path)
    except:
        print('error writing')
    return


def write_xml_to_file(xml, path):
    with open(path, "w") as f:
        f.write(xml)
    return True


def write_xml_to_gzip(xml, path):
    with gzip.open(path, "w") as f:
        try:
            f.write(xml)
        except TypeError:
            f.write(xml.encode())
    return True


def read_xml_from_file(path):
    with open(path, "r") as f:
        xml = f.read()
    return xml


def read_xml_from_gzip(path):
    with gzip.open(path, "r") as f:
        xml = f.read()
    xml = xml.decode()
    return xml


def get_xml_from_url(url):
    pass


def get_scoreboard(game_date, gz=True, no_cache=False):
    """Return the game file for a certain day matching certain criteria."""
    data = get_data(game_date, "scoreboard.xml", False, gz, no_cache)
    return data


def get_box_score(game_id, gz=False, no_cache=False):
    """Return the box score file of a game with matching id."""
    # get relevant information from game id
    game_date = date_from_gameid(game_id)
    data = get_data(game_date, "boxscore.xml", game_id, gz, no_cache)
    return data


def get_game_events(game_id, gz=False, no_cache=False):
    """Return the game events file of a game with matching id."""
    # get relevant information from game id
    game_date = date_from_gameid(game_id)
    data = get_data(game_date, "game_events.xml", game_id, gz, no_cache)
    return data


def get_overview(game_id, gz=False, no_cache=False):
    """Return the linescore file of a game with matching id."""
    # get relevant information from game id
    game_date = date_from_gameid(game_id)
    data = get_data(game_date, "linescore.xml", game_id, gz, no_cache)
    return data


def get_properties():
    """Return the current mlb properties file."""
    response = requests.get("http://mlb.mlb.com/properties/mlb_properties.xml")

    if response.status_code == requests.codes.ok:
        # if we get a 200 response, return the text.
        return response.text
    else:
        # in case mlb.com depricates this functionality
        raise ValueError("Could not find the properties file. mlb.com does not\
                          provide the file that mlbgame needs to perform this\
                          operation.")
