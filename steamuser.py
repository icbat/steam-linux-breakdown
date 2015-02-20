import requests, json
class User:
	def get_library(self, user_id, api_key):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + str(api_key)
		endpoint += "&steamid=" + str(user_id)
		endpoint += "&format=json"
		libraryJson = self.__get_json(endpoint)
		raw_json = libraryJson["response"]["games"]
		print "Steam ID " + str(user_id) + " has " + str(len(raw_json)) + " games"
		appids = []
		for game_json in raw_json:
			appids.append(game_json["appid"])
		return appids

	def __get_json(self, endpoint):
		response = requests.get(endpoint).content
		return json.loads(response)