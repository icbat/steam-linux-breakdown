import requests, urllib2, json

class Steam:
	def get_library(self, user_id, api_key):
		endpoint = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
		endpoint += "key=" + str(api_key)
		endpoint += "&steamid=" + str(user_id)
		endpoint += "&format=json"
		libraryJson = self.__get_json(endpoint)
		game_appids = libraryJson["response"]["games"]
		print "Steam ID " + str(user_id) + " has " + str(len(game_appids)) + " games"
		games = []
		for raw_game in game_appids:
			id = raw_game["appid"]
			try:
				games.append(game_cache.get_game(id))
			except Exception, e:
				print str(e) + ", skipping"
		return games

	def __get_json(self, endpoint):
		response = urllib2.urlopen(endpoint).read()
		return json.loads(response)

class Cache:
	def __init__(self, max_size = 100000):
		self.__max_size = max_size
		self.__games = dict()
		self.__bad_ids = []

	def get_game(self, appid):
		if appid in self.__bad_ids:
			return Game(appid)
		if appid in self.__games:
			return self.__games[appid]
		try:
			game = GameFetcher().get_from_steam(appid)
		except LookupError, e:
			self.__bad_ids.append(appid)
			raise e
		self.__add_to_cache(game)
		return game

	def get_current_size(self):
		return len(self.__games)

	def __add_to_cache(self, game):
		if len(self.__games) == self.__max_size:
			self.__games.popitem()
		self.__games[game.appid] = game	


game_cache = Cache()

class Game:
	def __init__(self, id):
		self.appid = id
		self.url = "https://store.steampowered.com/app/" + str(self.appid) + "/"
		self.is_linux = False		
		self.name = str(id)

	def __str__(self):
		return str(self.appid) + " " + str(self.name) + " " + str(self.is_linux)

class GameFetcher():
	def get_from_steam(self, appid):
		game = Game(appid)
		print "Fetching game from Steam:  " + str(appid)
		raw_html = urllib2.urlopen(game.url).read()
		game.is_linux = "platform_img linux" in raw_html
		game.name = self.__determine_name(appid, raw_html)
		return game

	def __determine_name(self, appid, raw_html):
		key = "<div class=\"apphub_AppName\">"
		if key not in raw_html:
			if "<div id=\"agegate_disclaim\">" in raw_html:
				print "Game is age gated!"
				raw_html = self.__bypass_age_gate(appid)
			else:
				raise LookupError("Cannot find game " + str(appid))
		temp = raw_html.split(key)[1]
		name = temp.split("<")[0]
		decoded = name.decode('ascii', 'ignore')		
		return decoded
	
	def __bypass_age_gate(self, appid):
		form_action = "http://store.steampowered.com/agecheck/app/"+ str(appid) + "/"
		header = {'User-Agent' : "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
		values = {
			'ageYear' : "1989",
			'ageMonth' : "January",
			'ageDay' : "10" }

		r = requests.post(form_action, headers=header, data=values)
		return r.content
