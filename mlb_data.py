import os
import json
import collections
import datetime
import statsapi
import numpy as np
from datetime import timedelta
import requests


def deep_update(source, overrides):
    """Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in list(overrides.items()):
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source

def get_file(path):
  dir = os.path.dirname(__file__)
  return os.path.join(dir, path)

def read_json(filename):
    j = {}
    path = get_file(filename)
    if os.path.isfile(path):
        j = json.load(open(path))
    return j

def get_config(base_filename):
    filename = "{}.json".format(base_filename)
    reference_filename = "{}.example".format(filename)
    reference_config = read_json(reference_filename)
    if not reference_filename:
        debug.error("Invalid {} reference config file. Make sure {} exists.".format(base_filename, base_filename))
        sys.exit(1)

    custom_config = read_json(filename)
    if custom_config:
        new_config = deep_update(reference_config, custom_config)
        return new_config
    return reference_config

def __filter_list_of_games(games, teams):
    return list(game for game in set(games) if set([game.away_team, game.home_team]).intersection(set(teams)))

def mlb_data_last_game(preferred_team):
    last_game_date = datetime.datetime.today()-timedelta(days=1)
    game_data_set = {}

    # Read scoreboard options from config.json if it exists
    #config = get_config("config")

    #teamData = statsapi.lookup_team(config['preferred']['teams'][0])
    for team in statsapi.lookup_team(preferred_team):

        last_game_date = last_game_date.strftime('%m/%d/%Y')
        last_gameData = statsapi.schedule(date=last_game_date, start_date=None, end_date=None, team=team['id'], opponent="", sportId=1, game_id=None)
        last_boxscore = statsapi.boxscore_data(last_gameData[0]['game_id'], timecode=None)

        game_data_set['home_id'] = last_gameData[0]['home_id']
        game_data_set['away_id'] = last_gameData[0]['away_id']
        game_data_set['status'] = last_gameData[0]['status']
        game_data_set['home_score'] = last_gameData[0]['home_score']
        game_data_set['home_hits'] = last_boxscore['home']['teamStats']['batting']['hits']
        game_data_set['away_score'] = last_gameData[0]['away_score']
        game_data_set['away_hits'] = last_boxscore['away']['teamStats']['batting']['hits']
        break

    return game_data_set

def mlb_data_current(preferred_team):
    now = datetime.datetime.now()
    game_data_set = {}

    # Read scoreboard options from config.json if it exists
    #config = get_config("config")

    #teamData = statsapi.lookup_team(config['preferred']['teams'][0])
    for team in statsapi.lookup_team(preferred_team):

        now = datetime.datetime.now().strftime('%m/%d/%Y')
        todays_gameData = statsapi.schedule(date=datetime.datetime.now().strftime('%m/%d/%Y'), start_date=None, end_date=None, team=team['id'], opponent="", sportId=1, game_id=None)
        #todays_boxscore = statsapi.boxscore_data(todays_gameData[0]['game_id'], timecode=None)
        response = requests.get('https://statsapi.mlb.com/api/v1.1/game/'+ str(todays_gameData[0]['game_id']) +'/feed/live')

        mlb_game_json_data = response.json() if response and response.status_code == 200 else None

        game_data_set['home_id'] = todays_gameData[0]['home_id']
        game_data_set['away_id'] = todays_gameData[0]['away_id']
        game_data_set['status'] = todays_gameData[0]['status']
        game_data_set['home_score'] = todays_gameData[0]['home_score']
        #game_data_set['home_hits'] = todays_boxscore['home']['teamStats']['batting']['hits'] #use live game data
        game_data_set['home_hits'] = mlb_game_json_data['liveData']['boxscore']['teams']['home']['teamStats']['batting']['hits']
        game_data_set['away_score'] = todays_gameData[0]['away_score']
        #game_data_set['away_hits'] = todays_boxscore['away']['teamStats']['batting']['hits'] #use live game data
        game_data_set['away_hits'] = mlb_game_json_data['liveData']['boxscore']['teams']['away']['teamStats']['batting']['hits']
        game_data_set['current_inning'] = todays_gameData[0]['current_inning']
        game_data_set['inning_state'] = todays_gameData[0]['inning_state']
        game_data_set['game_datetime'] = mlb_game_json_data['gameData']['datetime']['time'] + ' ' + mlb_game_json_data['gameData']['datetime']['ampm']
        game_data_set['outs_count'] = mlb_game_json_data['liveData']['linescore']['outs']
        break

    return game_data_set
