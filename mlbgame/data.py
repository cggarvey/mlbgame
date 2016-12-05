#!/usr/bin/env python

"""This module gets the XML data that other functions use.
It checks if the data is cached first, and if not,
gets the data from mlb.com.
"""

import os
import requests
import gzip
import lxml
from lxml import etree
import datetime


ROOT_URL = "http://gd2.mlb.com/components/game/mlb"
ROOT_DIR = os.path.join(os.path.dirname(__file__), "gameday-data")


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

    if os.path.isfile(file_path) and not no_cache:
        try:
            parsed = etree.parse(file_path)
        except lxml.etree.XMLSyntaxError:
            print("xml syntax error: {0}".format(file_path))
            return False
    else:
        url = _get_url(date, file, gid)
        try:
            parsed = etree.parse(url)
            cache_xml(parsed, date, file, gid, gz)
        except OSError:
            print("unable to fetch: {0}".format(url))
            return False

    # root = parsed.getroot()
    # return root
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
        return os.path.join(date_dir, 'gid_{0}'.format(gid))
    else:
        return os.path.join(date_dir)


def cache_xml(lxml_etree, date, file, gid=None, gz=False):

    dir_path = _get_dir(date, gid)

    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            access_error(dir_path)

    file_path = _get_path(date, file, gid, gz)

    xml_string = etree.tostring(lxml_etree, encoding='utf-8', standalone='yes')
    write_to_file(xml_string, file_path, gz)
    return


def write_to_file(text, file_path, gz=False):
    if gz:
        with gzip.open(file_path, "w") as fi:
            fi.write(text)
    else:
        with open(file_path, "w") as fi:
            fi.write(str(text))
    return


def get_scoreboard(date):
    """Return the game file for a certain day matching certain criteria."""
    data = get_data(date, "scoreboard.xml", gz=True)
    return data


def get_box_score(game_id):
    """Return the box score file of a game with matching id."""
    # get relevant information from game id
    date = date_from_gameid(game_id)
    data = get_data(date, "boxscore.xml", game_id)
    return data


def get_game_events(game_id):
    """Return the game events file of a game with matching id."""
    # get relevant information from game id
    date = date_from_gameid(game_id)
    data = get_data(date, "game_events.xml")
    return data


def get_overview(game_id):
    """Return the linescore file of a game with matching id."""
    # get relevant information from game id
    date = date_from_gameid(game_id)
    data = get_data(date, "linescore.xml", game_id)
    return data


def get_properties():
    """Return the current mlb properties file."""
    try:
        return requests.get("http://mlb.mlb.com/properties/mlb_properties.xml")
    # in case mlb.com depricates this functionality
    except requests.HTTPError:
        raise ValueError("Could not find the properties file. mlb.com does not\
                          provide the file that mlbgame needs to perform this\
                          operation.")
