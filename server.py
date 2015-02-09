from flask import Flask, render_template, request, redirect
from steam import Steam
app = Flask(__name__)

api_key = None
steam = None
@app.route('/')
def landing_page():
	return render_template('landing.html')

@app.route('/', methods=['POST'])
def redirect_to_output():
	steamid = request.form['steamid']
	return redirect("/" + steamid, code=302)


@app.route('/<username>')
def get_breakdown(username):
	game_list = steam.get_library(username, api_key)
	linux_compat_count = 0
	for game in game_list:
		if game.is_linux:
			linux_compat_count += 1
	return render_template('output.html', 
		games=game_list, 
		username=username, 
		linux_compat_count = linux_compat_count, 
		total_games = len(game_list), 
		non_compat=len(game_list) - linux_compat_count)

if __name__ == '__main__':
	app.debug = True
	key_location = "secret/steam-api-key.secret"
	print "Reading key file from " + key_location
	with open (key_location) as keyfile:
		api_key = keyfile.readline()
	print "Instantiating master 'Steam' object"
	steam = Steam()
	app.run()
