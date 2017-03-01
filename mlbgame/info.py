#!/usr/bin/env python

"""Module that is used for getting information
about the (MLB) league and the teams in it.
"""

import mlbgame.data
import mlbgame.object
from lxml import etree


def get_league_object():
    """Return the xml object corresponding to the league.

    Only designed for internal use"""
    league_xml = mlbgame.data.get_properties()
    data = etree.XML(league_xml.encode())

    # return league object
    return data.find("leagues").find("league")


def league_info():
    """Return a dictionary of league information."""
    league = get_league_object()
    output = {}
    for x in league.attrib:
        output[x] = league.attrib[x]
    return output


def team_info():
    """Return a list of team information dictionaries."""
    teams = get_league_object().find("teams").findall("team")
    output = []
    for team in teams:
        info = {}
        for x in team.attrib:
            info[x] = team.attrib[x]
        output.append(info)
    return output


class Info(mlbgame.object.Object):
    """Information about the league or teams.

    Properties:
    club
    club_common_name
    club_common_url
    club_full_name
    club_id
    club_spanish_name
    dc_site
    display_code
    division
    es_track_code
    esp_common_name
    esp_common_url
    facebook
    facebook_es
    fanphotos_url
    fb_app_id
    field
    google_tag_manager
    googleplus_id
    historical_team_code
    id
    instagram
    instagram_id
    league
    location
    medianet_id
    mobile_es_url
    mobile_short_code
    mobile_url
    mobile_url_base
    name_display_long
    name_display_short
    newsletter_category_id
    newsletter_group_id
    photostore_url
    pinterest
    pinterest_verification
    pressbox_title
    pressbox_url
    primary
    primary_link
    secondary
    snapchat
    snapchat_es
    team_code
    team_id
    tertiary
    timezone
    track_code
    track_filter
    tumblr
    twitter
    twitter_es
    url_cache
    url_esp
    url_prod
    vine
    """

    def nice_output(self):
        """Return a string for printing"""
        return '%s (%s)' % (self.club_full_name, self.club.upper())

    def __str__(self):
        return self.nice_output()
