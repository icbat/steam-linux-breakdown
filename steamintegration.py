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




import unittest

class SteamIntegrationTest(unittest.TestCase):
	def test_get_library_happy(self):
		test_id = "76561197972713139"
		steam = Steam()
		library = steam.get_library(test_id)
		self.failIf(len(library) == 0)
		self.failUnless(220 in library)
		return

if __name__ == '__main__':
	unittest.main()