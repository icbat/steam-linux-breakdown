from flask import Flask, render_template
from steamintegration import Steam
app = Flask(__name__)

api_key = None
steam = None
@app.route('/')
def landing_page():
	return 'The home page'

@app.route('/<username>')
def get_breakdown(username):
	game_list = steam.get_library(username, api_key)
	return render_template('output.html', games=game_list)

if __name__ == '__main__':
	app.debug = True
	key_location = "secret/steam-api-key.secret"
	print "Reading key file from " + key_location
	with open (key_location) as keyfile:
		api_key = keyfile.readline()
	print "Instantiating master 'Steam' object"
	steam = Steam()
	app.run()
