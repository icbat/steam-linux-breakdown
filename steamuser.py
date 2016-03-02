import requests, json
class User:
	id = "DEFAULT ID"
	name = "DEFAULT NAME"

	def __init__(self, user_input):
		print ("building user " + user_input)
		profile_text = self.__get_steam_profile_page(user_input)
		try:
			self.id = self.__get_steam_id(profile_text)
			self.name = self.__get_steam_name(profile_text)
		except IndexError:
			raise LookupError("Could not find steamid or name of user " + str(user_input))

	def get_library(self, api_key):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + str(api_key)
		endpoint += "&steamid=" + str(self.id)
		endpoint += "&format=json"
		libraryJson = self.__get_json(endpoint)
		raw_json = libraryJson["response"]["games"]
		print ("Steam ID " + str(self.name) + " has " + str(len(raw_json)) + " games")
		appids = []
		for game_json in raw_json:
			appids.append(game_json["appid"])
		return appids

	def __get_steam_profile_page(self, user_input):
		endpoint = "http://steamcommunity.com/id/" + str(user_input)
		print ("Getting user from " + endpoint	)
		response = requests.get(endpoint)
		print (response)
		if "Error" in str(response.content):
			print ("oh no")
			raise LookupError("Could not find steamid or name of user " + str(user_input))
		print ("Found a user!")
		return response.content

	def __get_steam_id(self, raw_html):
		print ("getting steam id")
		id = find_between(raw_html, "\"steamid\":\"", "\"")
		print ("found steamid: " + str(id))
		return id

	def __get_steam_name(self, raw_html):
		print ("getting steam name")
		name = find_between(raw_html, "\"personaname\":\"", "\"")
		print ("found user's display name: " + str(name))
		return name

	def __get_json(self, endpoint):
		response = requests.get(endpoint).content
		return json.loads(response)

def find_between(input, start, end):
	print ("splitting on '" + start + "' to '" + end + "'")
	return input.split(start)[1].split(end)[0]
