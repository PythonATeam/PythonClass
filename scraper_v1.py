""" Web scraper to gather game information that can be inserted into the database """
from bs4 import BeautifulSoup
import urllib, re, sys, requests

#main page url to start from and system tags to use when searching on the main page
url = "https://www.gamestop.com"
genres = ["1|text|all|notpaid", "2|text|action|notpaid", "3|text|casual|notpaid", "5|text|fighting|notpaid", 
		"7|text|musicparty|notpaid", "8|text|puzzlecards|notpaid", "9|text|roleplaying|notpaid", "10|text|shooter|notpaid",
		"11|text|simulation|notpaid", "12|text|sports|notpaid", "13|text|strategy|notpaid"]
systems = ["#pf_xboxone", "#pf_ps4", "#pf_xbox360", "#pf_ps3", "#pf_wiiu"]

#get the html for the main page and use it to create a Beatiful Soup object
main_page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(main_page, 'html.parser')

def get_data():
	""" top-level function that gathers the links for each system and then calls get_system """
	system_links = []
	for link in soup.find_all("li", class_="dropdown", rel=systems):
		system_links.append(link.a.get("href"))

	if link:
		for index in system_links:
			system_page = urllib.request.urlopen(index).read()
			system_soup = BeautifulSoup(system_page, 'html.parser')
			return get_system(system_soup)
	else:
		return None

def get_system(system_soup):
	genre_links = []
	for link in system_soup.find_all(attrs={"data-track":genres}):
		nextlink = url + link.get("href")
		genre_links.append(nextlink)

	if link:
		for index in genre_links:
			genre_page = urllib.request.urlopen(index).read()
			genre_soup = BeautifulSoup(genre_page, 'html.parser')
			return get_genre(genre_soup)
	else:
		return None

def get_genre(genre_soup):
	game_links = []
	games = []
	for link in genre_soup.find_all("div", class_="grid_2 alpha"):
		nextlink = url + link.findNext("a").get("href")
		game_links.append(nextlink)

	if link:
		for index in game_links:
			game_page = urllib.request.urlopen(index).read()
			game_soup = BeautifulSoup(game_page, "html.parser")
			games.append(get_game(game_soup))
		return games
	else:
		return None

def get_game(game_soup):
	data = []
	game_info = game_soup.find("div").h1.contents
	data.append([game_info[0], game_info[1]])
	return data

if __name__ == "__main__":
	results = get_data()
	print("results: ", results)