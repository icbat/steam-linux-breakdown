def read_secret_key():
	with open ("secret/steam-api-key.secret") as keyfile:
		content = keyfile.readline()
		return content

api_key = read_secret_key()

class Steam:
	def get_library(self, user_id):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + api_key
		endpoint += "&steamid=" + user_id
		endpoint += "&format=json"
		return endpoint