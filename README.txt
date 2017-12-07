James “Dustin” Moody
Breanna Eubanks
Bayan Kharazmi
Erik David
CIS 4930
Fall 2017

README

Problem:
Users could benefit from help in selecting their next game to play or purchase. Our website provides video game information to users in an accurate and convenient manner. 

Our flow to do this is as follows:
1) Execute scraper.py to generate the output file with our data from the web scraping. (data.txt)
2) Execute conversion2.py to generate a sql script to update our database with our newly scraped data. (insert2.sql)
3) Through our MySQL terminal run the command “source insert2.sql” to execute the script.


URL: http://tilted4.pythonanywhere.com

Special Instructions
You must login as an admin (admin:admin) to see the administrator console which allows you to remove users and modify game titles.

Python Libraries Used
Datetime
Flask
Flask_sqlalchemy
Flask_migrate
Flask_login
Werkzeug.security
Sqlalchemy
Sqlalchemy.sql
Sys
String
Bs4
Urllib
Re
Requests

References

Beautiful Soup Documentation https://www.crummy.com/software/BeautifulSoup/bs4/doc/

SQLAlchemy Documentation http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

PythonAnywhere Blog/Tutorial https://blog.pythonanywhere.com/


Division of Labor

Dustin – Back-end, Front-end, database support
(majority of code in our flask_app.py except for the database structure classes, main_page.html, login_page.html, register_page.html)
Breanna – Primary database admin, some front-end & back-end work
(SQLAlchemy database structure code (in flask_app.py), game.html)
Bayan – Data conversion, general support
(conversion2.py)
Eric – Data analysis, web scraping
(scraper.py)
