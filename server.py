from flask import Flask
app = Flask(__name__)

@app.route('/')
def landing_page():
	return 'The home page'

@app.route('/<username>')
def get_breakdown(username):
	return 'hello' + username

if __name__ == '__main__':
	app.debug = True
	app.run()