""" Web scraper to gather game information that can be inserted into the database """
from bs4 import BeautifulSoup
import urllib, re, sys, requests

#main page url to start from and system tags to use when searching on the main page
url = "https://www.gamestop.com"
systems = ["pf_xboxone", "pf_ps4", "pf_xbox360", "pf_ps3", "pf_wiiu"]

#get the html for the main page and use it to create a Beatiful Soup object
main_page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(main_page, 'html.parser')

def get_data():
	system_links = []
	results = []
	for link in soup.find_all("div", id=systems):
		next_link = link.findNext("ul").findNext("li").a.get("href")
		system_links.append(next_link)

	if link:
		for index in system_links:
			games_page = urllib.request.urlopen(index).read()
			games_soup = BeautifulSoup(games_page, 'html.parser')
			results.append(get_games(games_soup))
		return results
	else:
		return None

def get_games(games_soup):
	game_links = []
	games = []
	for link in games_soup.find_all("div", class_="grid_2 alpha"):
		nextgame_link = url + link.findNext("a").get("href")
		game_links.append(nextgame_link)

	if link:
		for index in game_links:
			game_page = urllib.request.urlopen(index).read()
			game_soup = BeautifulSoup(game_page, 'html.parser')
			games.append(get_game_data(game_soup))
		return games
	else:
		return None

def get_game_data(game_soup):
	game_data = []
	#getting the game name and publisher
	header_contents = game_soup.find("div").h1.contents
	game_name = str(header_contents[0])
	publisher = str(header_contents[1]).strip("<cite>").strip("</").split()[1]
	#getting the developer, genre, cost, platform, and rating
	developer = str(game_soup.find("li", class_="ats-prodRating-devDet").span.contents[0]).strip()
	genre = game_soup.find("li", class_="ats-prodRating-categDet").span.contents[0].split(',')[0].strip()
	var_data = game_soup.find("script", language="JavaScript").contents
	#cost = var_data[0].split(';')[4].split("=")[1].strip()
	platform = str(var_data[0].split(';')[2].split("=")[1].strip())
	#rating = str(game_soup.find("span", itemprop="ratingValue"))

	#packaging the data into a list
	game_data.append(game_name)
	game_data.append("description")
	game_data.append("rating")
	game_data.append(developer)
	game_data.append(publisher)
	game_data.append(genre)
	game_data.append("cost")
	game_data.append("release Date")
	game_data.append(platform)

	return game_data

	
if __name__ == "__main__":
	dbinfo = get_data()
	f = open("data1.txt", "w")
	for index in dbinfo:
		for subindex in index:
			f.write(str(subindex))
			f.write("\n")
	f.close()