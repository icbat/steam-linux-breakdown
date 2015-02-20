import requests, json
class User:
	id = "DEFAULT ID"
	name = "DEFAULT NAME"

	def __init__(self, user_input):
		self.id = self.__get_steam_id(user_input)
		self.name = self.__get_steam_name(self.id)

	def get_library(self, api_key):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + str(api_key)
		endpoint += "&steamid=" + str(self.id)
		endpoint += "&format=json"
		libraryJson = self.__get_json(endpoint)
		raw_json = libraryJson["response"]["games"]
		print "Steam ID " + str(self.name) + " has " + str(len(raw_json)) + " games"
		appids = []
		for game_json in raw_json:
			appids.append(game_json["appid"])
		return appids

	def __get_steam_id(self, user_input):
		return user_input

	def __get_steam_name(self, id):
		return id

	def __get_json(self, endpoint):
		response = requests.get(endpoint).content
		return json.loads(response)