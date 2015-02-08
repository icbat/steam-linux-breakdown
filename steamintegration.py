import urllib2, json

class Steam:
	def get_library(self, user_id, api_key):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + str(api_key)
		endpoint += "&steamid=" + str(user_id)
		endpoint += "&format=json"
		libraryJson = self.__get_json(endpoint)
		game_appids = libraryJson["response"]["games"]
		print "Steam ID " + str(user_id) + " has " + str(len(game_appids)) + " games"
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
		self.__bad_ids = []

	def get_game(self, appid):
		if appid in self.__bad_ids:
			return Game(appid)
		if appid in self.__games:
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
		print "Fetching game from Steam:  " + str(appid)
		raw_html = urllib2.urlopen(game.url).read()
		game.is_linux = "platform_img linux" in raw_html
		game.name = self.__determine_name(appid, raw_html)
		return game

	def __determine_name(self, appid, raw_html):
		key = "<div class=\"apphub_AppName\">"
		if key not in raw_html:
			if "<div id=\"agegate_disclaim\">" in raw_html:
				print "Game is age gated!"
			self.__bad_ids.append(appid)
			print "ERROR Could not find game with ID " + str(appid)
			return str(appid)
		else:
			temp = raw_html.split(key)[1]
			name = temp.split("<")[0]
			decoded = name.decode('ascii', 'ignore')		
			return decoded


game_cache = Cache()

class Game:
	def __init__(self, id):
		self.appid = id
		self.url = "https://store.steampowered.com/app/" + str(self.appid) + "/"
		self.is_linux = False		
		self.name = str(id)

	def __str__(self):
		return str(self.appid) + " " + str(self.name) + " " + str(self.is_linux)


import unittest

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

	def test_age_verification_passed(self):
		age_required_game = Cache().get_game(17460)
		self.assertEquals(age_required_game.name, "Mass Effect")

	def test_games_without_store_pages_dont_do_age_verification(self):
		game_without_page = Cache().get_game(29650)
		self.assertEquals(game_without_page.name, str(29650))


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