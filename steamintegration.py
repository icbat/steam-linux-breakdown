class Steam:
	__api_key = ""

	def __init__(self):
		self.__api_key = self.__read_secret_key()

	def get_library(self, user_id):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + self.__api_key
		endpoint += "&steamid=" + user_id
		endpoint += "&format=json"
		return endpoint

	def __read_secret_key(self):
		with open ("secret/steam-api-key.secret") as keyfile:
			content = keyfile.readline()
			return content