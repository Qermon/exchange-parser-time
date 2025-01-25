import asyncio
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from openpyxl import Workbook

# Асинхронний парсер інформації про ігри зі збереженням в Excel таблицю


def save_to_excel(data, filename="games_data.xlsx"):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Games Data"

    headers = ["Title", "Description", "Release Date", "Genre", "Platforms", "Developer", "Image"]
    sheet.append(headers)

    for game in data:
        sheet.append(game)

    workbook.save(filename)
    print(f"Data saved to {filename}")


async def get_page_html(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-finderProductCard"))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        games = soup.find_all('div', class_="c-finderProductCard c-finderProductCard-game")

        games_data = []
        for game in games:
            image_url = None
            picture_tag = game.find('picture', class_='c-cmsImage c-cmsImage-loaded')
            if picture_tag:
                img_tag = picture_tag.find('img')
                if img_tag:
                    image_url = img_tag.get('src')

            game_url = 'https://www.metacritic.com' + game.find('a').get('href')
            games_data.append((game_url, image_url))

        return games_data
    except Exception as ex:
        print(f"Error: {ex}")
        return []


async def get_game_data(driver, game_url, image_url):
    try:
        driver.get(game_url)
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-productHero_title"))
        )
        soup = BeautifulSoup(driver.page_source, 'lxml')

        name = soup.find('div', class_="c-productHero_title")
        name_text = name.text.strip() if name else "Not specified"

        description = soup.find('span', class_="c-productionDetailsGame_description g-text-xsmall")
        description_text = description.text.strip() if description else "Not specified"

        release_time = soup.find('span', class_="g-outer-spacing-left-medium-fluid g-color-gray70 u-block")
        release_time_text = release_time.text.strip() if release_time else "Not specified"

        genre = soup.find('a', class_="c-globalButton_container g-text-normal g-height-100 "
                                      "u-flexbox u-flexbox-alignCenter u-pointer "
                                      "u-flexbox-justifyCenter g-width-fit-content")
        genre_text = genre.find('span', class_="c-globalButton_label").text.strip() if genre else "Not specified"

        platforms = soup.find('ul', class_="g-outer-spacing-left-medium-fluid")
        platforms_text = []
        if platforms:
            platforms_block = platforms.find_all('li',
                                                 class_="c-gameDetails_listItem g-color-gray70 u-inline-block")
            platforms_text = [platform.text.strip() for platform in platforms_block]

        developer = soup.find('div', class_="c-gameDetails_Developer u-flexbox u-flexbox-row")
        developer_text = developer.find('li',
                                        class_="c-gameDetails_listItem g-color-gray70 u-inline-block").text.strip() if developer else "Not specified"

        return [name_text, description_text, release_time_text, genre_text, ", ".join(platforms_text), developer_text,
                image_url]
    except Exception as ex:
        print(f"Error: {ex}")


async def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 '
                         'Safari/537.36 OPR/77.0.4054.172')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options=options)

    try:
        all_games_data = []
        for i in range(1, 5):
            page_url = f"https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&page={i}"
            games_data = await get_page_html(driver, page_url)
            for game_url, image_url in games_data:
                game_data = await get_game_data(driver, game_url, image_url)
                all_games_data.append(game_data)

        save_to_excel(all_games_data)
    finally:
        driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
