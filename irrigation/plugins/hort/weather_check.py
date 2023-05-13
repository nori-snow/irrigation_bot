# -*- coding:utf-8 -*-

from datetime import datetime
import json
import codecs
import sys
import urllib.parse
import urllib.request

#livedoor weather hacks と dark sky forecastから気象情報メッセージを生成する
def getWeatherForecastMessage(date):

	#weather Hacks
	wh_info = getLivedoorWeatherHackInfo()

	#darksky forecast
	fc_info = getDarkskyForecastsInfo(date)
	daily_info = fc_info['daily']['data'][0]
	currentWeather = convertDarkSkyWeatherToJapanese(fc_info['currently']['icon'])

	msg = ('現在の練馬の気温は' + str(fc_info['currently']['temperature']) + '℃、'
	+ '天気は「'+ currentWeather +'」だよ。\n'
	+ '今日の最低気温は' + str(daily_info['temperatureMin']) + '℃,'  
	+'最高気温は' + str(daily_info['temperatureMax']) + '℃の予報だよ。\n'
	+ '予想湿度は' + str(daily_info['humidity']*100) +'%, 降水確率は' 
	+ str(daily_info['precipProbability']*100) + '%だよ!\n'
	+ '天気概況はこんな感じだよ！\n```'
	+ wh_info['description']['text'] + '```'
	)

	return msg

#Weather Hacks から天気予報の情報を取得
def getLivedoorWeatherHackInfo():

	# Livedoor Weather hacksのURL
	# ※2020年7月でLivedoorのAPIの提供が終了
	# url = 'http://weather.livedoor.com/forecast/webservice/json/v1?'
	# 以後は互換サービス利用
	url = 'https://weather.tsukumijima.net/api/forecast?'

	#api用のパラメータ
	param = {'city': '130010'}

	paramStr = urllib.parse.urlencode(param)

	#APIを叩いて天気予報を取得する
	wh_info = getApiJsonData(url + paramStr)
	
	return wh_info
#DarkSky Forecast API から気象情報を取得
def getDarkskyForecastsInfo(daytime):
	#forecasts TOKEN
	forecast_secret = '3abcc339fb78ed13091444d38b50d77a'

	#forecast url
	url = 'https://api.darksky.net/forecast/'

	#自宅付近の緯度経度
	lat = '35.729061'
	lon = '139.585301'

	#日時をunixtimeに変換
	time = datetime.now().strftime('%s')

	param ={'exclude' : 'minutely,hourly,flags',
	'units' : 'si'}
	paramStr = urllib.parse.urlencode(param)

	urlStr = url + forecast_secret + '/' + lat + ',' + lon + ','+ time + '?' + paramStr

	fc_info = getApiJsonData(urlStr)

	return fc_info

#APIを叩いてJSON形式のデータを得る
def getApiJsonData(urlStr):
	#apiを叩いて返り値をえる
	res = urllib.request.urlopen(urlStr).read()

	#データをjson形式に変換
	result = res.decode('utf-8')
	api_info = json.loads(result)

	return api_info

#英語の天気メッセージを日本語に変換する
def convertDarkSkyWeatherToJapanese(icon):
	if icon == 'clear-day':
		weather = '快晴'
	elif icon == 'clear-night':
		weather = '快晴'
	elif icon == 'partly-cloudy-day':
		weather = '晴れ'
	elif icon == 'partly-cloudy-night':
		weather = '晴れ'
	elif icon == 'cloudy':
		weather = '曇り'
	elif icon == 'rain':
		weather = '雨'
	elif icon == 'snow':
		weather = '雪'
	elif icon == 'sleet':
		weather = 'みぞれ'
	elif icon == 'wind':
		weather = '強風'
	elif icon == 'fog':
		weather = '霧'
	else:
		weather = icon
	return weather

