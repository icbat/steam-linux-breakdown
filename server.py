from flask import Flask
from steamintegration import Steam
app = Flask(__name__)

steam = Steam()

@app.route('/')
def landing_page():
	return 'The home page'

@app.route('/<username>')
def get_breakdown(username):	
	return steam.get_library(username)

if __name__ == '__main__':
	app.debug = True
	app.run()