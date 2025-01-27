# Currency Exchange & Country Time & Async Parser
This project is a Django-based web application that provides two main functionalities:

Currency Exchange: A tool for converting one currency to another based on real-time exchange rates.
Country Time: A tool for displaying the current time in different time zones worldwide.
Additionally, there is a background service that fetches game data from Metacritic and stores it in an Excel sheet for offline use.

# Features
Currency Exchange

Users can input an amount and choose currencies to convert between.
Displays real-time conversion rates based on the latest data from an external API.
The conversion history is stored in a database.
Country Time

Users can select a country to get the current local time.
The time is fetched from a public API and displayed to the user.
The queried times are stored in the database for future reference.
Game Data Fetcher

An asynchronous Python script that scrapes game data from Metacritic using Selenium and BeautifulSoup.
Stores the game information into an Excel sheet.

# Technologies:
Python,
Django,
Postgresql,
Beautifulsoup,
Selenium,
Asyncio,
Docker

# Set-Up
1) git clone https://github.com/Qermon/exchange-parser-time.git or get from version control
2) In the root folder(currency) you need to create a .env file and add SECRET_KEY with any code there Example: SECRET_KEY = 123
3) docker-compose up --build
