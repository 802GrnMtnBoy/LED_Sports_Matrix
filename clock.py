from PIL import Image, ImageFont, ImageDraw, ImageSequence
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import datetime
import re
import debug
from time import sleep

matrix = Matrix(RGBMatrix(options = matrixOptions))

time = datetime.datetime.now()

font_large = ImageFont.truetype(get_file("fonts/score_large.otf"), 16)

matrix.clear()
matrix.draw_text_layout(time, self.time, fillColor=self.clockfill)

matrix.draw_text_layout(self.layout.date, self.date.strftime("%b %d %Y").upper(), fillColor=self.wxdtfill)

if time_format == "%I:%M":
    matrix.draw_text_layout(self.layout.meridiem, "{}\n{}".format(self.meridiem[0], self.meridiem[1]),fillColor=self.wxdtfill)