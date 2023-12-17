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


def get_liked_songs():
    try:
        body = driver.find_element(
            By.XPATH,
            "//*[@id='main']/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div",
        )
        songs = []
        scroll_count = 15  # Adjust the number of scrolls as needed
        for i in range(scroll_count):
            body.send_keys(Keys.ARROW_DOWN)
            song = driver.find_element(
                By.XPATH,
                f'//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div[{i + 1}]/div',
            )
            song_title = song.find_element(By.XPATH, "./div[2]/div/a/div").text
            print("title", song_title)
            try:
                explicit_span = song.find_element(By.XPATH, "./div[2]/div/span[1]/span")
                print("in try", explicit_span.text)
                if "E" in explicit_span.text:
                    song_explicit = True
                else:
                    song_explicit = False
                song_artist = song.find_element(
                    By.XPATH, "./div[2]/div/span[2]/div/a"
                ).text
            except:
                song_explicit = False
                song_artist = song.find_element(
                    By.XPATH, "./div[2]/div/span/div/a"
                ).text
            print("expl", song_explicit)
            print("artist", song_artist)
            song_album = song.find_element(By.XPATH, "./div[3]/span/span/a").text
            print("alb", song_album)
            song_mins, song_seconds = song.find_element(
                By.XPATH, "./div[5]/div"
            ).text.split(":")
            print("mins", song_mins)
            print("secs", song_seconds)
            print("**********")
            song = Song(
                title=song_title,
                artist=song_artist,
                song_album=song_album,
                explicit=song_explicit,
                mins=song_mins,
                seconds=song_seconds,
                date_added=None,
            )

            songs.append(song)
        print("songs", songs, "length of songs", len(songs), "done")
    except:
        driver.quit()


def main():
    print(date.today())
    driver.get(SPOTIFY)
    driver.fullscreen_window()
    get_login_page()
    enter_credentials()
    get_liked_page()
    time.sleep(4)
    get_liked_songs()


if __name__ == "__main__":
    main()
