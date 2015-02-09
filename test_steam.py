
import unittest
from steamintegration import Steam, Cache

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