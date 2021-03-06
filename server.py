from flask import Flask, render_template, request, redirect
from steam import Cache
from steamuser import User
import argparse
app = Flask(__name__)

api_key = None
cache = None
@app.route('/')
def landing_page():
	return render_template('landing.html')

@app.route('/', methods=['POST'])
def redirect_to_output():
	user_input = request.form['steamid']
	return redirect("/" + user_input, code=302)


@app.route('/<user_input>')
def get_breakdown(user_input):
	try:
		user = User(user_input)
	except LookupError:
		return redirect("/")
	game_appids = user.get_library(api_key)
	game_list = cache.get_games(game_appids)
	linux_compat_count = 0
	for game in game_list:
		if game.is_linux:
			linux_compat_count += 1
	return render_template('output.html', 
		games=game_list, 
		username=user.name, 
		linux_compat_count = linux_compat_count, 
		total_games = len(game_list), 
		non_compat=len(game_list) - linux_compat_count)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default="5000")
parser.add_argument('--ip', default="127.0.0.1")
parser.add_argument('--debug', default=False)
args = parser.parse_args()

if __name__ == '__main__':
	print "Server starting up!"	
	print "Is debug mode? " + str(args.debug)
	key_location = "secret/steam-api-key.secret"
	print "Reading key file from " + key_location
	with open (key_location) as keyfile:
		api_key = keyfile.readline()
	print "Instantiating master 'Steam' object"
	cache = Cache()
	print "Server startup complete"
	app.run(
    	host = args.ip,
    	debug = args.debug,
    	port = args.port,
    	)
