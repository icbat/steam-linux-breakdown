import unittest
from steamuser import User

class UserTests(unittest.TestCase):
	# hard to get a live api key... needs mocking
	# can run locally though!
	def skip_get_library_happy(self):
		test_id = "76561198036780759"
		steam = User()
		key_location = "secret/steam-api-key.secret"
		with open (key_location) as keyfile:
			api_key = keyfile.readline()
			library = steam.get_library(test_id, api_key)
		self.failIf(len(library) == 0)

if __name__ == '__main__':
	unittest.main()