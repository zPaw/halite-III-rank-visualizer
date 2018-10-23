import requests, time, re, json, sys
import matplotlib.pyplot as plt
import numpy as np

interval = 10 #Seconds
# user_id = 330 #Found at end of url when looking at page
user_ids = [330, 323]#, 2024, 3154]

ranks = []
times = []
colors = ["r", "g", "b", "c", "m", "y", "k"]
users = []

class User:
	def __init__(self, name, user_id, color="k"):
		self.name = name
		self.user_id = user_id
		self.color = color
		self.ranks = []
		self.times = []

def get_rank(user_ID):
	try:
		web_page = requests.get(f"https://api.2018.halite.io/v1/api/user/{user_ID}").text
	except ConnectionError:
		return "Could not receive data! Please check your internet connection!"
	profile_json = json.loads(web_page)
	return profile_json['rank']

def get_profile(user_ID):
	try:
		return json.loads(requests.get(f"https://api.2018.halite.io/v1/api/user/{user_ID}").text)
	except:
		print("Could not connect to server. Please check your internet connection and try again. If your connection is fine, then the api must be down.")
		sys.exit()

for user_id in user_ids:
	account_info = get_profile(user_id)
	users.append(User(account_info["username"], user_id))

plt.gca().invert_yaxis()

while True:
	print("Gathering new data")
	for user in users:
		returned_rank = get_rank(user.user_id)
		if not returned_rank == "Could not receive data! Please check your internet connection!":
			user.ranks.append(returned_rank)
			user.times.append(time.time())
			plt.plot(user.times, user.ranks, color=user.color)
			plt.plot(user.times, user.ranks, color=user.color, marker="o")
		else:
			print(returned_rank)
	plt.pause(interval)