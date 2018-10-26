#TODO: Use json to save user data; Use matplotlib dates to make that aspect better
import requests, time, re, json, sys, datetime, os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

config = json.load(open("config.json"))
interval = config["interval"]#Seconds
user_ids = config["user_ids"]

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

	def save_to_file(self, filepath=Path(f"{Path.cwd()}/Users")):
		dict_to_dump = {"username": self.name, "user_id": self.user_id, "ranks": self.ranks, "times": self.times}
		json.dump(dict_to_dump, open(f"{filepath}/{self.user_id}.json", "w"), indent=4)

def get_rank(user_ID):
	try:
		web_page = requests.get(f"https://api.2018.halite.io/v1/api/user/{user_ID}").text
	except:
		return "Could not receive data! Please check your internet connection!"
	profile_json = json.loads(web_page)
	return profile_json['rank']

def get_profile(user_ID):
	try:
		return json.loads(requests.get(f"https://api.2018.halite.io/v1/api/user/{user_ID}").text)
	except:
		print("Could not connect to server. Please check your internet connection and try again. If your connection is fine, then the api must be down.")
		sys.exit()

def create_user_from_json(filepath):
	user_json = json.load(open(filepath))
	return_user = User(user_json["username"], user_json["user_id"])
	return_user.ranks = user_json["ranks"]
	return_user.times = user_json["times"]
	return return_user

def trim_data(data):
	trimmed_data = []
	for i in range(len(data)):
		if i == 0:
			trimmed_data.append(data[i])
		elif i == len(data)-1:
			trimmed_data.append(data[i])
		elif not (data[i] == data[i+1] and data[i] == data[i-1]):
			trimmed_data.append(data[i])
	return trimmed_data

def trim_two_data(data_1, data_2):
	trimmed_data_1 = []
	trimmed_data_2 = []
	for i in range(len(data_1)):
		if i == 0:
			trimmed_data_1.append(data_1[i])
			trimmed_data_2.append(data_2[i])
		elif i == len(data_1)-1:
			trimmed_data_1.append(data_1[i])
			trimmed_data_2.append(data_2[i])
		elif not (data_1[i] == data_1[i+1] and data_1[i] == data_1[i-1]):
			trimmed_data_1.append(data_1[i])
			trimmed_data_2.append(data_2[i])
	return (trimmed_data_1, trimmed_data_2)

def reloadConfigJson():
	global config
	json.dump(config, open("config.json", "w"), indent=4)
	config = json.load(open("config.json"))

def setup_plot():
	plt.gca().invert_yaxis()
	plt.xlabel("Time")
	plt.ylabel("Rank")
	plt.title("Rank over time")

if __name__ == "__main__":
	for user_id in user_ids:
		if Path(f"{Path.cwd()}/Users/{user_id}.json").exists():
			print("Loading existing user")
			user_from_file = create_user_from_json(Path(f"{Path.cwd()}/Users/{user_id}.json"))
			user_from_file.color = colors[len(users)-1]
			users.append(user_from_file)
		else:
			print("Creating new user")
			account_info = get_profile(user_id)
			users.append(User(account_info["username"], user_id, color=colors[len(users)-1]))

	while True:
		if not os.path.exists("Users"):
			os.makedirs("Users")
		print("Gathering new data")
		plt.clf()
		setup_plot()
		for user in users:
			returned_rank = get_rank(user.user_id)
			if not returned_rank == "Could not receive data! Please check your internet connection!":
				user.ranks, user.times = trim_two_data(user.ranks, user.times)
				user.ranks.append(returned_rank)
				user.times.append(time.time())
				plt.plot([datetime.datetime.fromtimestamp(time) for time in user.times], user.ranks, color=user.color, label=user.name + " " + str(returned_rank))
				plt.plot([datetime.datetime.fromtimestamp(time) for time in user.times], user.ranks, color=user.color, marker="o")
			else:
					print(returned_rank)
			user.save_to_file()
		plt.legend()
		plt.pause(interval)