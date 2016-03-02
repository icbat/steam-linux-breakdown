import urllib.request, json

class Cache:
	def __init__(self, max_size = 100000):
		self.__max_size = max_size
		self.__games = dict()
		self.__bad_ids = []

	def get_game(self, appid):
		print("getting game by id " + str(appid))
		if appid in self.__bad_ids:
			print("game was already known to be incompatible")
			return Game(appid)
		if appid in self.__games:
			print("game was already a known to to be linux friendly")
			return self.__games[appid]
		try:
			game = GameFetcher().get_from_steam(appid)
		except LookupError:
			self.__bad_ids.append(appid)
			raise new_exc from original_exc
		self.__add_to_cache(game)
		return game

	def get_games(self, game_appids):
		games = []
		for appid in game_appids:
			try:
				games.append(self.get_game(appid))
			except Exception:
				print (str("something bad happened") + ", skipping")
		return games

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
		print ("Fetching game from Steam:  " + str(appid))
		print ("Using url:  " + game.url)
		raw_html = requests.get(game.url).content
		game.is_linux = "platform_img linux" in raw_html
		game.name = self.__determine_name(appid, raw_html)
		return game

	def __determine_name(self, appid, raw_html):
		key = "<div class=\"apphub_AppName\">"
		if key not in raw_html:
			print ("Having some trouble finding the app name, details to follow")
			if "<div id=\"agegate_disclaim\">" in raw_html:
				print ("Game is age gated!")
				raw_html = self.__bypass_age_gate(appid)
			else:
				print ("Had trouble finding the right elements")
				raise LookupError("Cannot find game " + str(appid))
		temp = raw_html.split(key)[1]
		name = temp.split("<")[0]
		print(name)
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
