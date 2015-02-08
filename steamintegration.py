import urllib2, json



class Steam:
	def __init__(self):
		self.__api_key = self.__read_secret_key()

	def get_library(self, user_id, api_key):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + str(api_key)
		endpoint += "&steamid=" + str(user_id)
		endpoint += "&format=json"
		libraryJson = self.__get_json(endpoint)
		game_appids = libraryJson["response"]["games"]
		games = []
		for raw_game in game_appids:
			id = raw_game["appid"]
			games.append(game_cache.get_game(id))
		return games

	def __get_json(self, endpoint):
		response = urllib2.urlopen(endpoint).read()
		return json.loads(response)



class Cache:
	def __init__(self, max_size = 100000):
		self.__max_size = max_size
		self.__games = dict()

	def get_game(self, appid):
		if (appid in self.__games):
			return self.__games[appid]
		game = self.__get_from_steam(appid)
		self.__add_to_cache(game)
		return game

	def get_current_size(self):
		return len(self.__games)

	def __add_to_cache(self, game):
		if len(self.__games) == self.__max_size:
			self.__games.popitem()
		self.__games[game.appid] = game

	def __get_from_steam(self, appid):
		game = Game(appid)
		raw_html = urllib2.urlopen(game.url).read()
		game.is_linux = "platform_img linux" in raw_html
		game.name = self.__determine_name(raw_html)		
		return game

	def __determine_name(self, raw_html):
		key = "<div class=\"apphub_AppName\">"
		return raw_html.split(key)[1].split("<")[0]

game_cache = Cache()

class Game:
	def __init__(self, id):
		self.appid = id
		self.url = "https://store.steampowered.com/app/" + str(self.appid) + "/"
		self.is_linux = False		
		self.name = "DEFAULT"

	def __str__(self):
		return str(self.appid) + " " + str(self.name) + " " + str(self.is_linux)


import unittest

class SteamIntegrationTest(unittest.TestCase):
	# Too long right now. Need to do some mocking I think
	def skip_get_library_happy(self):
		test_id = "76561197972713139"
		steam = Steam()
		library = steam.get_library(test_id)
		self.failIf(len(library) == 0)

class GamePopulationTest(unittest.TestCase):
	def test_game_populates(self):
		happy_game = Cache().get_game(211820)
		self.assertTrue(happy_game.is_linux, "Game is linux but marked false" + str(happy_game))
		self.assertEquals(happy_game.name, "Starbound")

		subtler_happy_game = Cache().get_game(220)
		self.assertTrue(subtler_happy_game.is_linux, "Game is linux but marked false" + str(subtler_happy_game))
		self.assertEquals(subtler_happy_game.name, "Half-Life 2")

		negative_game = Cache().get_game(346160)
		self.assertFalse(negative_game.is_linux, "Game not linux but marked true" + str(negative_game))
		self.assertEquals(negative_game.name, "Barter Empire")

class CacheTest(unittest.TestCase):
	def test_cache_growth(self):
		cache = Cache(5)
		self.assertEquals(cache.get_current_size(), 0, "Cache not empty at start!")
		
		cache.get_game(220)
		self.assertEquals(cache.get_current_size(), 1, "One game not added")
		
		cache.get_game(220)
		self.assertEquals(cache.get_current_size(), 1, "Duplicate game added!")

	def test_boundaries(self):
		cache = Cache(1)
		self.assertEquals(cache.get_current_size(), 0, "Cache not empty at start!")
		cache.get_game(220)
		cache.get_game(211820)
		self.assertEquals(cache.get_current_size(), 1, "Max size not upheld")		


if __name__ == '__main__':
	unittest.main()