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

class Cache:
	__games = {}
	__max_size = 100000

	def get_game(self, appid):
		return

class Game:
	__id = "DEFAULT"
	name = "DEFAULT"
	is_linux = False
	url = "placeholderurl.com"

	def __init__(self, id):
		self.__id = id
		self.url = "https://store.steampowered.com/app/" + str(id) + "/"
		page_data = self.__get_app_html(id)		
		self.is_linux = "platform_img linux" in page_data
		self.name = self.__determine_name(page_data)

	def __get_app_html(self, id):
		return urllib2.urlopen(self.url).read()

	def __determine_name(self, raw_html):
		key = "<div class=\"apphub_AppName\">"
		return raw_html.split(key)[1].split("<")[0]

	def __str__(self):
		return str(self.__id) + " " + str(self.name) + " " + str(self.is_linux)


import unittest

class SteamIntegrationTest(unittest.TestCase):
	def test_get_library_happy(self):
		test_id = "76561197972713139"
		steam = Steam()
		library = steam.get_library(test_id)
		self.failIf(len(library) == 0)

	def test_game_populates(self):
		happy_game = Game(211820)
		self.assertTrue(happy_game.is_linux, "Game is linux but marked false" + str(happy_game))
		self.assertEquals(happy_game.name, "Starbound")

		subtler_happy_game = Game(220)
		self.assertTrue(subtler_happy_game.is_linux, "Game is linux but marked false" + str(subtler_happy_game))
		self.assertEquals(subtler_happy_game.name, "Half-Life 2")

		negative_game = Game(346160)
		self.assertFalse(negative_game.is_linux, "Game not linux but marked true" + str(negative_game))
		self.assertEquals(negative_game.name, "Barter Empire")

if __name__ == '__main__':
	unittest.main()