# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from datetime import datetime


import RPi.GPIO as GPIO
import time
import re
import sys
import os
sys.path.append('/home/noriyuki/bot/irrigation/plugins/hort')
import irrigation
import weather_check

@listen_to('(.*)')

def agriculturalResponse(message,something):
	direction = "{0}".format(something)
	if ('水やり' in direction):
		wateringtime = re.search("\d+", direction)
		if wateringtime != None:
			ir_time = wateringtime.group()
			msg = irrigation.wateringResponse(ir_time)
		else:
			msg= '半角数字で時間を指定してね'

	elif("天気" in direction):
		checktime = datetime.now()
		#日付に対応する天気予報のメッセージを取得
		msg = weather_check.getWeatherForecastMessage(checktime)
	else:
		msg = 'ごめん、よくわからなかったんだ...'

	message.reply(msg)

