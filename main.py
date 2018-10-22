import requests, time, re, json
import matplotlib.pyplot as plt
import numpy as np

interval = 10 #Seconds
user_id = 330 #Found at end of url when looking at page

ranks = []
times = []

def get_rank(user_ID):
	web_page = requests.get(f"https://api.2018.halite.io/v1/api/user/{user_ID}").text
	profile_json = json.loads(web_page)
	return profile_json['rank']

while True:
	print("Gathering web page")
	ranks.append(get_rank(user_id))
	times.append(time.time())
	plt.plot(times, ranks, color="k")
	plt.pause(interval)