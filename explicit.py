from selenium import webdriver
from bs4 import BeautifulSoup
import requests, time, os
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from song import Song

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
SPOTIFY = "https://open.spotify.com/"

load_dotenv()
SPOTIFY_EMAIL = os.getenv("SPOTIFY-EMAIL")
SPOTIFY_PASSWORD = os.getenv("SPOTIFY-PASSWORD")

CLEAN_PLAYLIST = "Clean Songs"
EXPLICIT_PLAYLIST = "Explicit Songs"
CLEAN_EXPLICIT_PLAYLIST = "Clean and Explicit Songs"

service = ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)


def get_login_page():
    """
    Enters login page from spotify main page
    """
    try:
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@id='main']/div/div[2]/div[3]/header/div[4]/div[2]/button[2]",
                )
            )
        )
        login_button.click()
    except:
        driver.quit()


def enter_credentials():
    """
    Enters email and password anad click login button
    """
    try:
        email_text_box = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "login-username"))
        )
        email_text_box.send_keys(SPOTIFY_EMAIL)
        password_text_box = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "login-password"))
        )
        password_text_box.send_keys(SPOTIFY_PASSWORD)

        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()
    except:
        driver.quit()


def get_liked_page():
    try:
        buttons = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "hIehTT"))
        )
        liked_songs_button = buttons[0]
        liked_songs_button.click()
    except:
        driver.quit()


"""
Get song, make Song class, add to list
Find search button
search song title and song 
"""


def get_liked_song(index: int):
    try:
        song = driver.find_element(
            By.XPATH,
            f'//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div[{index + 1}]/div',
        )
        song_title = song.find_element(By.XPATH, "./div[2]/div/a/div").text
        try:
            song.find_element(By.XPATH, "./div[2]/div/span[1]/span")
            song_explicit = True
            song_artist = song.find_element(By.XPATH, "./div[2]/div/span[2]/div/a").text
        except:
            song_explicit = False
            song_artist = song.find_element(By.XPATH, "./div[2]/div/span/div/a").text
        song_album = song.find_element(By.XPATH, "./div[3]/span/span/a").text
        song_mins, song_seconds = song.find_element(
            By.XPATH, "./div[5]/div"
        ).text.split(":")
        song_mins = int(song_mins)
        song_seconds = int(song_seconds)
        song = Song(
            title=song_title,
            artist=song_artist,
            album=song_album,
            explicit=song_explicit,
            mins=song_mins,
            seconds=song_seconds,
        )
        return song
    except:
        driver.quit()


# body = driver.find_element(
#     By.XPATH,
#     "//*[@id='main']/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div",
# )
# songs = []
# scroll_count = 15  # Adjust the number of scrolls as needed
# body.send_keys(Keys.ARROW_DOWN)


def main():
    print(date.today())
    driver.get(SPOTIFY)
    driver.fullscreen_window()
    get_login_page()
    enter_credentials()
    get_liked_page()
    time.sleep(4)
    print(get_liked_song(2))


if __name__ == "__main__":
    main()
