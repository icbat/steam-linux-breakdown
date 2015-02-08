import urllib2, json

class Steam:
	__api_key = ""

	def __init__(self):
		self.__api_key = self.__read_secret_key()

	def get_library(self, user_id):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + str(self.__api_key)
		endpoint += "&steamid=" + str(user_id)
		endpoint += "&format=json"
		libraryJson = self.__get_json(endpoint)
		raw_games = libraryJson["response"]["games"]
		games = []
		for raw_game in raw_games:
			games.append(raw_game["appid"])
		return games

	def __read_secret_key(self):
		with open ("secret/steam-api-key.secret") as keyfile:
			return keyfile.readline()

	def __get_json(self, endpoint):
		response = urllib2.urlopen(endpoint).read()
		return json.loads(response)

class Game:
	__id = "DEFAULT"
	name = "DEFAULT"	
	is_linux = False

	def __init__(self, id):
		self.__id = id		
		page_data = self.__get_app_html(id)

	def __get_app_html(self, id):
		url = "https://store.steampowered.com/app/" + str(id) + "/"
		return urllib2.urlopen(url).read()

	def __str__(self):
		return self.__id


import unittest

class SteamIntegrationTest(unittest.TestCase):
	def test_get_library_happy(self):
		test_id = "76561197972713139"
		steam = Steam()
		library = steam.get_library(test_id)
		self.failIf(len(library) == 0)

	def test_game_populates(self):
		happy_game = Game(211820)
		self.assertTrue(happy_game.is_linux, "Game should be linux-compat but is marked not")

if __name__ == '__main__':
	unittest.main()