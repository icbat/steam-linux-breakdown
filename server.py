from flask import Flask
from steamintegration import Steam
app = Flask(__name__)

api_key = None
steam = None
@app.route('/')
def landing_page():
	return 'The home page'

@app.route('/<username>')
def get_breakdown(username):

	return str(steam.get_library(username, api_key))

if __name__ == '__main__':
	app.debug = True
	key_location = "secret/steam-api-key.secret"
	print "Reading key file from " + key_location
	with open (key_location) as keyfile:
		api_key = keyfile.readline()
	print "Instantiating master 'Steam' object"
	steam = Steam()
	app.run()
