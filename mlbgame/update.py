#!/usr/bin/env python

from __future__ import print_function

import mlbgame

from datetime import date, timedelta
import getopt
import gzip
import os
import shutil
import sys

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError


def date_usage():
    """Display usage of dates."""
    print("Something was wrong with your date(s): Dates must be correct and\
           in the format <MM-DD-YYYY>. End date cannot be before start date.")


def process_stats(games):
    # games is an mlbgame.day object
    i = 0
    for i, game in enumerate(games):
        mlbgame.data.get_box_score(game.game_id)
    return i


def process_events(games):
    # games is an mlbgame.day object
    i = 0
    for i, game in enumerate(games):
        mlbgame.data.get_game_events(game.game_id)
    return i


def process_overview(games):
    # games is an mlbgame.day object
    i = 0
    for i, game in enumerate(games):
        mlbgame.data.get_overview(game.game_id)
    return i


def run(hide=False, stats=False, events=False, overview=False, start=date(2012, 1, 12), end=None):
    """Update local game data."""
    # set end to be the day before today at maximum
    today = date.today()
    if end is None or end >= today:
        end = today - timedelta(days=1)

    # check if the dates are in correct chronological order
    if start > end:
        date_usage()
        sys.exit(2)

    # print a message because sometimes it seems like the program is not doing anything
    if not hide:
        print("Checking local data...")

    # get information for loop
    curr = start
    delta = timedelta(days=1)
    # calculate the days between the start and the end
    difference = float((end - start).days + .0)
    # loop through the dates
    while curr <= end:
        y, m, d = mlbgame.data.unpack_ymd(curr)

        day = mlbgame.day(y, m, d)

        # get stats if specified
        if stats:
            process_stats(day)

        # get events if specified
        if events:
            process_events(day)

        # get overview if specified
        if overview:
            process_overview(day)

        # loading message to show something is actually happening
        if not hide:
            pct = (1 - ((end - curr).days / difference)) * 100
            sys.stdout.write('Loading games (%00.2f%%) \r' % (pct))
            sys.stdout.flush()
        # increment the date counter
        curr += delta

    if not hide:
        # make sure loading ends at 100%
        sys.stdout.write('Loading games (100.00%).\n')
        sys.stdout.flush()
        # show finished message
        print("Complete.")


def clear():
    """Delete all cached data."""
    try:
        shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gameday-data/'))
    except OSError:
        access_error(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gameday-data/'))


def usage():
    """Display usage of command line arguments."""
    print("usage: " + sys.argv[0] + " <arguments>")
    print()
    print("Arguments:")
    print("--help (-h)\t\t\tdisplay this help menu")
    print("--clear\t\t\t\tdelete all cached data")
    print("--hide\t\t\t\thides output from update script")
    print("--stats\t\t\t\tsaves the box scores and individual game stats from every game")
    print("--events\t\t\tsaves the game events from every game")
    print("--overview\t\t\tsaves the game overview from every game")
    print("--start (-s) <MM-DD-YYYY>\tdate to start updating from (default: 01-01-2012)")
    print("--end (-e) <MM-DD-YYYY>\t\tdate to update until (default: current day)")


def start():
    """Start updating from a command and arguments."""
    try:
        data = getopt.getopt(sys.argv[1:], "hms:e:", ["help", "clear", "hide", "stats", "events", "overview", "start=", "end="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    hide = False
    more = False
    stats = False
    events = False
    overview = False
    start = "01-01-2012"
    today = date.today()
    end = "%i-%i-%i" % (today.month, today.day, today.year)
    # parse arguments
    for x in data[0]:
        if x[0] == "-h" or x[0] == "--help":
            return usage()
        elif x[0] == "--clear":
            return clear()
        elif x[0] == "--hide":
            hide = True
        elif x[0] == "--stats":
            stats = True
        elif x[0] == "--events":
            events = True
        elif x[0] == "--overview":
            overview = True
        elif x[0] == "-s" or x[0] == "--start":
            start = x[1]
        elif x[0] == "-e" or x[0] == "--end":
            end = x[1]
    # verify that dates are acceptable
    try:
        # split argument
        split_start = start.split("-")
        split_end = end.split("-")
        # create example dates
        date_start = date(int(split_start[2]), int(split_start[0]), int(split_start[1]))
        date_end = date(int(split_end[2]), int(split_end[0]), int(split_end[1]))
    except:
        date_usage()
        sys.exit(2)
    run(hide, stats, events, overview, date_start, date_end)


# start program when run from command line
if __name__ == "__main__":
    start()
