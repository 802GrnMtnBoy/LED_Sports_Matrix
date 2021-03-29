import sys
import datetime
import time
import os
import argparse
import mlb_data
from nhl_data import run_nhl
from weather_data import runWeather
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageFont, ImageDraw
import numpy as np

def get_file(path):
    dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(dir, path)

def readOptions(filename):
    enabledArray = []
    nhl_team_id = 0
    nhldelay = 0
    weatherEnabled=False
    #weatherKey=""
    #weatherBaseurl=""
    #weatherZip=""
    #weatherModifiers=""
    weatherDelay = 0
    nhlEnabled=False
    mlbEnabled=False
    #mlbEnabled="f"
    #nflEnabled="f"
    options_list = {}
    enabledArray.append("clock")
    if os.path.isfile(filename):
        try:
            f = open(filename, 'r')
            #print ("Reading options file")
            for line in f:
                if len(line) > 2:
                    # split on the first '=' only
                    s = line[:len(line) - 1].split('=', 1)
                    value = s[1][:len(s[1])]
                    if s[0] == "weatherEnabled" and s[1] == "t":
                        #weatherEnabled = True
                        options_list['weatherEnabled'] = True
                        enabledArray.append("weather")
                    elif s[0] == "weatherDelay": #and options_list['weatherEnabled'] == True:
                        options_list['weatherDelay'] = int(value)
                        #weatherDelay = int(value)
                    elif s[0] == "nhlEnabled" and s[1] == "t":
                        options_list['nhlEnabled'] = True
                        #nhlEnabled = True
                        enabledArray.append("nhl")
                    #elif s[0] == 'nhlTeam' and nhlEnabled == True:
                    elif s[0] == 'nhlTeam': #and options_list['nhlEnabled'] == True:
                        #nhl_team_id = int(value)
                        options_list['nhl_team_id'] = int(value)
                    elif s[0] == 'nhlDelay': #and options_list['nhlEnabled'] == True:
                        #nhldelay = int(value)
                        options_list['nhlDelay'] = int(value)
                    elif s[0] == "mlbEnabled" and s[1] == "t":
                        options_list['mlbEnabled'] = True
                        enabledArray.append("mlb")
                    elif s[0] == 'mlbTeam' and options_list['mlbEnabled'] == True:
                        #nhl_team_id = int(value)
                        options_list['mlb_team_id'] = int(value)
                    elif s[0] == 'mlbDelay' and options_list['mlbEnabled'] == True:
                        #nhldelay = int(value)
                        options_list['mlbDelay'] = int(value)
        except IOError:
            print ("Failure reading options file")
        except IndexError:
            print ("Error in options.ini: " + line)
    else:
        print ("Unable to find options.ini file 1")
    #return weatherEnabled,weatherDelay,nhlEnabled,nhl_team_id, nhldelay, enabledArray
    return options_list, enabledArray
def displayLogo(currentBoard,logo_id, colout, w, h):

    if currentBoard == "nhl":
        image_file = "/home/pi/bowerLEDmatrix/nhl_logos/40x30/"+str(logo_id)+".png"
        #im = Image.open(image_file)
        #im = im.convert('RGBA')
    elif currentBoard == "weather":
        now = datetime.datetime.now()
        if int(now.strftime("%H")) < 18:
            #image_file = "/home/pi/47bowerLEDmatrix/weather/25x25/day/6.png"
            image_file = "/home/pi/bowerLEDmatrix/weather_logos/64x64/day/"+logo_id
        else:
            #image_file = "/home/pi/47bowerLEDmatrix/weather/25x25/night/335.png"
            image_file = "/home/pi/bowerLEDmatrix/weather_logos/64x64/night/"+str(logo_id)
    elif currentBoard == "mlb":
        image_file = "/home/pi/bowerLEDmatrix/mlb_logos/40x30/"+str(logo_id)+".png"
    
    im = Image.open(image_file)
    im = im.convert('RGBA')        
    
    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = colout # Transpose back needed

    image = Image.fromarray(data)
    #image.thumbnail((30, 20), Image.ANTIALIAS)
    image.thumbnail((w, h), Image.ANTIALIAS)

    #self.matrix.SetImage(image.convert('RGB'),posx,posy)
    return image.convert('RGB')

def get_board(enabledArray,arrayCnt):
    currentBoard = enabledArray[arrayCnt]
    return currentBoard

def run(matrix):

    isgameday = False
    #matrix colors
    colout = (100,100,100)
    icony = 0 
    iconsizx = 40 #size in pixels of the weather icons
    iconsizy = 30
    posx = 0
    posy = 0
    width = 64
    height = 32
    chkWeatherCnt = 0
    nhl_noGameCnt = 0
    arrayCnt = 0
    # setup canvas
    canvas = matrix.CreateFrameCanvas()
    
    # fill it with black
    canvas.Fill(0, 0, 0)
    
    #colors
    white = graphics.Color(255, 255, 255)
    gray = graphics.Color(127, 127, 127)
    green = graphics.Color(0, 150, 0)
    yellow = graphics.Color(127, 127, 0)
    red = graphics.Color(150, 0, 0)
    red2 = graphics.Color(255,0,0)
    blue = graphics.Color(0, 0, 150)
    orange = graphics.Color(255,153,51)
    magenta = graphics.Color(127, 0, 127)
    cyan = graphics.Color(0, 127, 127)
    dim = graphics.Color(10, 10, 10)
    # text will be yellow
    textColor = graphics.Color(255, 235, 59)
    textColor2 = graphics.Color(255,255,153)
 
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x7.bdf")
    time_font = graphics.Font()
    time_font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
    font_medium = graphics.Font()
    font_medium.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
    font_very_small = graphics.Font()
    font_very_small.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")
    font_small = graphics.Font()
    font_small.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
    font_big = graphics.Font() 
    font_big.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/9x15.bdf")

    #option ini file name
    filename = '/home/pi/bowerLEDmatrix/options.ini'

    # set initial switch values
    last_Time_chk = datetime.datetime.now()
    clockDelay = 5
    enabledArray = []
    
    #get settings from option file
    #weatherEnabled,weatherDelay,nhlEnabled,nhl_team_id, nhldelay, enabledArray  = readOptions(filename)
    options_list, enabledArray  = readOptions(filename)
    #set initial board to display
    #currentBoard = enabledArray[arrayCnt]
   
    while True:
        # get the current time
        now = datetime.datetime.now()
        currentBoard = get_board(enabledArray,arrayCnt)
        if arrayCnt == len(enabledArray)-1:
            arrayCnt = 0
        else:
            #move array position
            arrayCnt += 1
        
        if ((now - last_Time_chk).total_seconds()/60) > 60 and nhl_noGameCnt > 3:
            last_Time_chk = datetime.datetime.now()
            nhl_noGameCnt = 0

        # display clock    
        if currentBoard == "clock":
            #print ("clock")
            now = datetime.datetime.now()  # so seconds tick
            date_string = now.strftime('%A')
            date_string_2 = now.strftime('%B %d')
            time_string = now.strftime('%-I:%M %p')

            # calculate element positions
            time_pos_x = int((64 - len(time_string) * 7) / 2)
            date_pos_x = int((64 - len(date_string) * 5) / 2)
            date2_pos_x = int((64 - len(date_string_2) * 5) / 2)
            
            canvas.Clear()
            # fill canvas with black
            canvas.Fill(0, 0, 0) 

            # put elements on canvas
            graphics.DrawText(canvas, time_font, time_pos_x,11, textColor, time_string)
            graphics.DrawText(canvas, font, date_pos_x, 20, textColor, date_string)
            graphics.DrawText(canvas, font, date2_pos_x, 29, textColor, date_string_2)
            canvas = matrix.SwapOnVSync(canvas)
            
            #if now.strftime('%-H:%M') > '23:00':
            #    time.sleep(secs)
            #else:
            time.sleep(clockDelay)
        
        elif currentBoard == "nhl" and options_list['nhlEnabled'] == True and nhl_noGameCnt < 5:

            #print ("nhl")
            nhl_game_data= run_nhl(options_list['nhl_team_id'])
            #home_score, home_team, away_score, away_team, current_period, home_sog, away_sog, time_remaining, isgameday = run_nhl(nhl_team_id)
            canvas.Clear()

            if nhl_game_data['gameday'] == True and nhl_game_data['current_period'] > 0:
                text1 = "vs"
                text2 = str(nhl_game_data['home_score'])
                text3 = str(nhl_game_data['away_score'])
                text4 = str(nhl_game_data['home_sog'])
                text5 = str(nhl_game_data['away_sog'])
                text6 = "P:" + str(nhl_game_data['current_period'])
                text7 = str(nhl_game_data['time_remaining'])                               
                
                graphics.DrawText(canvas, font_very_small, posx+29, posy+8, textColor2, text1)
                graphics.DrawText(canvas, font_very_small, posx+47, posy+26, orange, "G:")
                graphics.DrawText(canvas, font_very_small, posx+54, posy+26, textColor2, text2)
                graphics.DrawText(canvas, font_very_small, posx+5, posy+26, orange, "G:")
                graphics.DrawText(canvas, font_very_small, posx+13, posy+26, textColor2, text3)
                graphics.DrawText(canvas, font_very_small, posx+39, posy+32, orange, "SOG:")
                graphics.DrawText(canvas, font_very_small, posx+55, posy+32, textColor2, text4)
                graphics.DrawText(canvas, font_very_small, posx, posy+32, orange, "SOG:")
                graphics.DrawText(canvas, font_very_small, posx+16, posy+32, textColor2, text5)
                graphics.DrawText(canvas, font_very_small, posx+27, posy+17, textColor, text6)
            
                if text7 == "Final":
                    graphics.DrawText(canvas, font_very_small, posx+23, posy+26, red2, text7)
                else:      
                    graphics.DrawText(canvas, font_very_small, posx+23, posy+26, textColor2, text7)
                
                canvas = matrix.SwapOnVSync(canvas)

                matrix.SetImage(displayLogo(currentBoard,nhl_game_data['away_team'], colout, 25, 25),-1,icony-4)
                matrix.SetImage(displayLogo(currentBoard,nhl_game_data['home_team'],colout, 25, 25),40,icony-4)

            elif nhl_game_data['gameday'] == True and nhl_game_data['current_period'] == 0:
                graphics.DrawText(canvas, font_very_small, 29, 12, textColor, "vs")
                graphics.DrawText(canvas, font_very_small, 25, 25, textColor, str(nhl_game_data['game_start_time']))
                graphics.DrawText(canvas, font_very_small, 11, 32, magenta, "TODAYS GAME")
                canvas = matrix.SwapOnVSync(canvas)
                matrix.SetImage(displayLogo(currentBoard,nhl_game_data['away_team'], colout, iconsizx, iconsizy),-5,icony-6)
                matrix.SetImage(displayLogo(currentBoard,nhl_game_data['home_team'],colout, iconsizx, iconsizy),40,icony-6)
            elif nhl_game_data['gameday'] == False:
                nhl_noGameCnt += 1
                graphics.DrawText(canvas, font_very_small, 35, 10, textColor, "No")
                graphics.DrawText(canvas, font_very_small, 38, 18, textColor, "Game")
                graphics.DrawText(canvas, font_very_small, 45, 25, textColor, "Today")
                canvas = matrix.SwapOnVSync(canvas)
                matrix.SetImage(displayLogo(currentBoard,options_list['nhl_team_id'],colout, iconsizx, iconsizy),3,icony+1)
            
            time.sleep(options_list['nhlDelay'])
        
        elif currentBoard == "mlb" and options_list['mlbEnabled'] == True:
            dt = datetime.datetime.now()
            canvas.Clear()

            if dt.time() > datetime.time(10):
                mlb_game_data_set = mlb_data.mlb_data_current(options_list['mlb_team_id'])
                arr_x = 30
                arr_y = 22
                if len(mlb_game_data_set) != 0:
                    if  mlb_game_data_set['status'] == "Scheduled" or mlb_game_data_set['status'] == "Pre-Game":
                        graphics.DrawText(canvas, font_very_small, 30, 20, textColor, "vs")
                        #print (str(mlb_game_data_set['game_datetime'])[14:-1])
                        graphics.DrawText(canvas, font_very_small, 20, 26, textColor, str(mlb_game_data_set['game_datetime']))
                        graphics.DrawText(canvas, font_very_small, 11, 32, magenta, "TODAYS GAME")               
                        canvas = matrix.SwapOnVSync(canvas)
                        matrix.SetImage(displayLogo(currentBoard,mlb_game_data_set['away_id'], colout, 30, 30),-1,icony-4)
                        matrix.SetImage(displayLogo(currentBoard,mlb_game_data_set['home_id'],colout, 30, 30),37,icony-4)                
                    else:
                        graphics.DrawText(canvas, font_very_small, 5, 25, orange, "R:")
                        graphics.DrawText(canvas, font_very_small, 12, 25, textColor2, str(mlb_game_data_set['away_score']))
                        graphics.DrawText(canvas, font_very_small, 5, 32, orange, "H:")
                        graphics.DrawText(canvas, font_very_small, 12, 32, textColor2, str(mlb_game_data_set['away_hits']))
                        graphics.DrawText(canvas, font_very_small, 48, 25, orange, "R:")
                        graphics.DrawText(canvas, font_very_small, 55, 25, textColor2, str(mlb_game_data_set['home_score']))
                        graphics.DrawText(canvas, font_very_small, 48, 32, orange, "H:")
                        graphics.DrawText(canvas, font_very_small, 55, 32, textColor2, str(mlb_game_data_set['home_hits']))


                        if mlb_game_data_set['status'] == "Final":
                            graphics.DrawText(canvas, font_very_small, 23, 28, red2, str(mlb_game_data_set['status']))
                        else:
                            if mlb_game_data_set['inning_state'] == "Top":
                                arr_y = arr_y - 2
                                direction = 1
                            elif mlb_game_data_set['inning_state'] == "Bottom":
                                direction = -1
                            elif mlb_game_data_set['inning_state'] == "Middle" or mlb_game_data_set['inning_state'] == "End":
                                direction = 0
                            
                            graphics.DrawText(canvas, font_very_small, 35, 24, textColor2, str(mlb_game_data_set['current_inning']))
                            graphics.DrawText(canvas, font_very_small, 20, 30, orange, "Outs:")
                            graphics.DrawText(canvas, font_very_small, 40, 30, textColor2, str(mlb_game_data_set['outs_count']))

                            for offset in range(3):
                                graphics.DrawLine(canvas, arr_x - offset, arr_y + (offset * direction), arr_x + offset, arr_y + (offset * direction), textColor)

                        canvas = matrix.SwapOnVSync(canvas)
                        matrix.SetImage(displayLogo(currentBoard,mlb_game_data_set['away_id'], colout, 30, 30),1,icony-3)
                        matrix.SetImage(displayLogo(currentBoard,mlb_game_data_set['home_id'],colout, 30, 30),37,icony-3)
                else:
                    #No MLB Game Today
                    graphics.DrawText(canvas, font_very_small, 35, 10, textColor, "No")
                    graphics.DrawText(canvas, font_very_small, 38, 18, textColor, "Game")
                    graphics.DrawText(canvas, font_very_small, 45, 25, textColor, "Today")
                    canvas = matrix.SwapOnVSync(canvas)
                    matrix.SetImage(displayLogo(currentBoard,options_list['mlb_team_id'],colout, iconsizx, iconsizy),3,icony+1)
            else:
                mlb_game_data_set = mlb_data.mlb_data_last_game(options_list['mlb_team_id'])
                
                if len(mlb_game_data_set) != 0:
                    graphics.DrawText(canvas, font_very_small, 5, 25, orange, "R:")
                    graphics.DrawText(canvas, font_very_small, 12, 25, textColor2, str(mlb_game_data_set['away_score']))
                    graphics.DrawText(canvas, font_very_small, 5, 32, orange, "H:")
                    graphics.DrawText(canvas, font_very_small, 12, 32, textColor2, str(mlb_game_data_set['away_hits']))
                    graphics.DrawText(canvas, font_very_small, 48, 25, orange, "R:")
                    graphics.DrawText(canvas, font_very_small, 55, 25, textColor2, str(mlb_game_data_set['home_score']))
                    graphics.DrawText(canvas, font_very_small, 48, 32, orange, "H:")
                    graphics.DrawText(canvas, font_very_small, 55, 32, textColor2, str(mlb_game_data_set['home_hits']))
                    graphics.DrawText(canvas, font_very_small, 23, 28, red, str(mlb_game_data_set['status']))

                    canvas = matrix.SwapOnVSync(canvas)
                    matrix.SetImage(displayLogo(currentBoard,mlb_game_data_set['away_id'], colout, 30, 30),1,icony-3)
                    matrix.SetImage(displayLogo(currentBoard,mlb_game_data_set['home_id'],colout, 30, 30),37,icony-3)
                else:
                    #No MLB game yesterday
                    graphics.DrawText(canvas, font_very_small, 35, 10, textColor, "No")
                    graphics.DrawText(canvas, font_very_small, 38, 18, textColor, "Game")
                    graphics.DrawText(canvas, font_very_small, 32, 25, textColor, "Yesterday")
                    canvas = matrix.SwapOnVSync(canvas)
                    matrix.SetImage(displayLogo(currentBoard,options_list['mlb_team_id'],colout, iconsizx, iconsizy),3,icony+1)                    

            time.sleep(options_list['mlbDelay'])

        elif currentBoard == "weather" and options_list['weatherEnabled'] == True:
            #print ("weather")
            weather_json_data = runWeather(filename)
            weatherLogosz = 30

            weather_icon_now = weather_json_data['current']['condition']['icon']
            weather_icon_now = weather_icon_now[-7:]
            now = datetime.datetime.now()
            canvas.Clear()

            text1 = "C: " + str(weather_json_data['current']['temp_f'])[:2] + u'\N{DEGREE SIGN}'
            text2 = "H: "+ str(weather_json_data['forecast']['forecastday'][0]['day']['maxtemp_f'])[:2] + u'\N{DEGREE SIGN}'
            text3 = "L: "+ str(weather_json_data['forecast']['forecastday'][0]['day']['mintemp_f'])[:2] + u'\N{DEGREE SIGN}' 

            graphics.DrawText(canvas, font_very_small, posx+40, posy+11, graphics.Color(255,255,153), text1)
            graphics.DrawText(canvas, font_very_small, posx+40, posy+17, graphics.Color(255,153,51), text2)
            graphics.DrawText(canvas, font_very_small, posx+40, posy+23, graphics.Color(0,128,255), text3)
            graphics.DrawText(canvas, font_very_small, posx+37, posy+32, textColor, now.strftime('%-I:%M %p'))
            
            canvas = matrix.SwapOnVSync(canvas)
            matrix.SetImage(displayLogo(currentBoard, weather_icon_now, colout, 33, 30),3,3)

            time.sleep(options_list['weatherDelay'])
