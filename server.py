from flask import Flask

app = Flask(__name__)

def read_secret_key():
	with open ("secret/steam-api-key.secret") as keyfile:
		content = keyfile.readline()
		return content

api_key = read_secret_key()

@app.route('/')
def landing_page():
	return 'The home page'

@app.route('/<username>')
def get_breakdown(username):
	return get_library(username)

def get_library(user_id):
	endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
	endpoint += "key=" + api_key
	endpoint += "&steamid=" + user_id
	endpoint += "&format=json"
	return endpoint

if __name__ == '__main__':
	app.debug = True
	app.run()