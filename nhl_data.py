import datetime
import time
import os
import requests
from lib import nhl
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import random
from PIL import Image
import sys
import numpy as np

def sleep(sleep_period):
    """ Function to sleep if not in season or no game.
    Inputs sleep period depending if it's off season or no game."""

    # Get current time
    now = datetime.datetime.now()
    # Set sleep time for no game today
    if "day" in sleep_period:
        delta = datetime.timedelta(hours=12)
    # Set sleep time for not in season
    elif "season" in sleep_period:
        # If in August, 31 days else 30
        if now.month is 8:
            delta = datetime.timedelta(days=31)
        else:
            delta = datetime.timedelta(days=30)
    next_day = datetime.datetime.today() + delta
    next_day = next_day.replace(hour=12, minute=10)
    sleep = next_day - now
    sleep = sleep.total_seconds()
    time.sleep(sleep)
    
def run_nhl(nhl_team_id):
    nhl_game_data = {}
    teams = {1 : "NJD", 2 : "NYI", 3 : "NYR", 4 : "PHI", 5 : "PIT", 6 : "BOS", 7 : "BUF", 8 : "MTL", 9 : "OTT", 10 : "TOR", 12 : "CAR", 13 : "FLA", 14 : "TBL", 15 : "WSH", 16 : "CHI", 17 : "DET", 18 : "NSH", 19 : "STL", 20 : "CGY", 21 : "COL", 22 : "EDM", 23 : "VAN", 24 : "ANA", 25 : "DAL", 26 : "LAK", 28 : "SJS", 29 : "CBJ", 30 : "MIN", 52 : "WPG", 53 : "ARI", 54 : "VGK"}
    #teams = {6 : "BOS"}
    
    home_score = 0
    home_team = 0
    away_score = 0
    away_team = 0
    current_period = 0
    home_sog = 0
    away_sog = 0
    home_powerplay = 0
    away_powerplay = 0
    time_remaining = 0
    gameday = False
    # check game
    gameday = nhl.check_if_game(nhl_team_id)

    if gameday == True:
        # check end of game
        game_end = nhl.check_game_end(nhl_team_id)

        # get score, teams, and live stats link
        home_score, home_team, away_score, away_team, live_stats_link = nhl.fetch_game(nhl_team_id)
        # get stats from the game
        current_period, home_sog, away_sog, home_powerplay, away_powerplay, time_remaining = nhl.fetch_live_stats(live_stats_link)

        if current_period > 0:
            nhl_game_data['home_score'] = home_score
            nhl_game_data['home_team'] = home_team
            nhl_game_data['away_score'] = away_score
            nhl_game_data['away_team'] = away_team
            nhl_game_data['current_period'] = current_period
            nhl_game_data['home_sog'] = home_sog
            nhl_game_data['away_sog'] = away_sog
            nhl_game_data['time_remaining'] = time_remaining
            nhl_game_data['gameday'] = gameday
            return nhl_game_data
            #return home_score, home_team, away_score, away_team, current_period, home_sog, away_sog, time_remaining, gameday

        if current_period == 0:
            #offscreen_canvas.Clear()
            game_start_time = nhl.fetch_game_start_time(live_stats_link)

            nhl_game_data['home_team'] = home_team
            nhl_game_data['away_team'] = away_team
            nhl_game_data['current_period'] = current_period
            nhl_game_data['game_start_time'] = game_start_time
            nhl_game_data['gameday'] = gameday

            return nhl_game_data
            #return home_score, home_team, away_score, away_team, current_period, home_sog, away_sog, game_start_time, gameday

    else:
        #print("No Game Today!")
        nhl_game_data['home_team'] = home_team
        nhl_game_data['gameday'] = gameday
        return nhl_game_data
        #return home_score, home_team, away_score, away_team, current_period, home_sog, away_sog, time_remaining, gameday


###########################################################
"""
if __name__ == "__main__":
    my_scoreboard = scoreboard()
    try:
        # Start loop
        print("Press CTRL-C to stop")
        my_scoreboard.run()
    except KeyboardInterrupt:
        print("Exiting\n")
        sys.exit(0)
"""