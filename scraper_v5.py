""" Web scraper to gather game information that can be inserted into the database """
from bs4 import BeautifulSoup
import urllib, re, sys, requests

#constant value that can be modified easily
NUMPAGES = 0

#main page url to start from and system tags to use when searching on the main page
url = "https://www.gamestop.com"
systems = ["pf_xboxone", "pf_ps4", "pf_xbox360", "pf_ps3", "pf_wiiu"]

#get the html for the main page and use it to create a Beatiful Soup object
main_page = urllib.request.urlopen(url).read()
soup = BeautifulSoup(main_page, 'html.parser')

def get_data():
	""" top-level function that starts crawling the website """
	system_links = []
	results = []
	count = 0
	for link in soup.find_all("div", id=systems): #getting the top-level links for each system - the first page url
		next_link = link.findNext("ul").findNext("li").a.get("href")
		system_links.append(next_link)

	if link:
		for index in system_links: #for each top-level link, call get_games() to proceed with crawling down to the next level
			games_page = urllib.request.urlopen(index).read()
			games_soup = BeautifulSoup(games_page, 'html.parser')
			results.append(get_games(games_soup))

			next_Page = url + games_soup.find("a", class_="next_page").get("href") #get the link for the next page of games

			while next_Page and count < NUMPAGES: #loop to keep crawling to the next page of games for each system
				next_page = urllib.request.urlopen(next_Page).read()
				next_soup = BeautifulSoup(next_page, 'html.parser')
				results.append(get_games(next_soup))
				next_Page = url + next_soup.find("a", class_="next_page").get("href")
				count += 1
			count = 0

		return results
	else:
		return None

def get_games(games_soup):
	game_links = []
	games = []
	for link in games_soup.find_all("div", class_="grid_2 alpha"): #get individual game links and put them in a list
		nextgame_link = url + link.findNext("a").get("href")
		game_links.append(nextgame_link)

	if link:
		for item in game_links: #put together what I need and call get_game_data(), which actually scrapes the data
			game_page = urllib.request.urlopen(item).read()
			game_soup = BeautifulSoup(game_page, 'html.parser')
			games.append(get_game_data(game_soup))

		return games
	else:
		return None

def get_game_data(game_soup):
	header_contents = game_soup.find("h1", itemprop="name").contents #getting the header contents, to get the game name
	game_name = str(header_contents[0])
	publisher = str(game_soup.find("li", class_="ats-prodRating-pubDet").span.contents[0]).strip()

	#getting the developer, genre, and cost for each game
	try:
		developer = str(game_soup.find("li", class_="ats-prodRating-devDet").span.contents[0]).strip()
	except AttributeError as e:
		developer = "N/A"
	else:
		pass
	finally:
		pass

	genre = game_soup.find("li", class_="ats-prodRating-categDet").span.contents[0].split(',')[0].strip()
	var_data = game_soup.find("script", language="JavaScript").contents
	cost = game_soup.find("h3", class_="ats-prodBuy-price").span.contents
	cover_image = game_soup.find("meta", property="og:image")["content"]

	#formatting the cost based on the length of the list returned by the find function
	if(len(cost) != 1):
		cost = cost[1].contents[0]
	else:
		cost = cost[0]

	#getting the platform and the rating
	platform = str(var_data[0].split(';')[2].split("=")[1].strip())
	rating = game_soup.find("span", itemprop="ratingValue")

	#checking for valid input and setting a default value for items without a rating
	if(rating != None):
		rating = rating.contents[0]
	else:
		rating = "None"

	#packaging the data into a list and returning it
	game_data = [game_name, "description", rating, developer, publisher, genre, cost, "release Date", platform, cover_image]
	return game_data
	
if __name__ == "__main__":
	results = get_data() #call the top-level function and store the results
	f = open("data5.txt", "w") #open an output file
	for index in results: #series of loops to write the data to the output file
		for subindex in index:
			for pos in subindex:
				f.write(pos)
				f.write(',')
			f.write('\n')
	f.close() #closing the output file