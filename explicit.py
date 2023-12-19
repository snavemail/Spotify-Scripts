from selenium import webdriver
from bs4 import BeautifulSoup
import requests, time, os
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
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
CLEAN_EXPLICIT_PLAYLIST = "C + E Songs"

service = ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)


def get_login_page():
    """
    Enters login page from spotify main page
    """
    try:
        login_button = WebDriverWait(driver, 100).until(
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
        email_text_box = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "login-username"))
        )
        email_text_box.send_keys(SPOTIFY_EMAIL)
        password_text_box = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "login-password"))
        )
        password_text_box.send_keys(SPOTIFY_PASSWORD)

        login_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()
    except:
        driver.quit()


def get_liked_page():
    """
    Goes to liked page
    Since the left sidebar seems to be open always, it looks like I can call this
    from anywhere in the code to get back to liked songs

    Could also be used easily to get to 2020's folder for other script
    """
    try:
        buttons = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "hIehTT"))
        )
        liked_songs_button = buttons[0]
        liked_songs_button.click()
    except:
        driver.quit()


def get_liked_song(index: int):
    """
    Given an index 0-based?, finds a song in the liked_songs_page
    Maybe I should call that here before trying anything else
    """
    try:
        song = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f'//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div/div[2]/div[2]/div[{index}]/div',
                )
            )
        )
        song_title = song.find_element(By.XPATH, "./div[2]/div/a/div").text
        try:
            song.find_element(By.XPATH, "./div[2]/div/span[1]/span")
            song_explicit = True
            song_artist = song.find_element(By.XPATH, "./div[2]/div/span[2]/div/a").text
        except:
            song_explicit = False
            song_artist = song.find_element(By.XPATH, "./div[2]/div/span/div/a").text
        song_mins, song_seconds = song.find_element(
            By.XPATH, "./div[5]/div"
        ).text.split(":")
        song_mins = int(song_mins)
        song_seconds = int(song_seconds)
        song = Song(
            title=song_title,
            artist=song_artist,
            explicit=song_explicit,
            mins=song_mins,
            seconds=song_seconds,
        )
        return song
    except:
        driver.quit()


def check_for_explicit(censored_song: Song):
    """
    Given a song, it will go into the search bar and search for explicit songs
    Should be able to be called from anywhere
    """
    if not censored_song.explicit:
        try:
            search_button = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "UYeKN11KAw61rZoyjcgZ")
                )
            )[1]
            search_button.click()
            try:
                search_bar = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "QO9loc33XC50mMRUCIvf")
                    )
                )
                search_bar.send_keys(f"{censored_song.title} {censored_song.artist}")

                searched_songs = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//*[@id='searchPage']/div/div/section[2]/div[2]/div/div/div/div[2]",
                        )
                    )
                )
                for j in range(4):
                    searched_song = searched_songs.find_element(
                        By.XPATH, f"./div[{j + 1}]"
                    )
                    try:
                        e_tag = searched_song.find_element(
                            By.XPATH, "./div/div[1]/div[2]/span[1]/span"
                        )
                        if e_tag.text == "E":
                            song_explicit = True
                        else:
                            song_explicit = False

                    except:
                        song_explicit = False
                    if song_explicit:
                        song_title = searched_song.find_element(
                            By.XPATH, "./div/div[1]/div[2]/a/div"
                        ).text
                        song_artist = searched_song.find_element(
                            By.XPATH, "./div/div[1]/div[2]/span[2]/span/a"
                        ).text
                        song_mins, song_seconds = searched_song.find_element(
                            By.XPATH, "./div/div[2]/div"
                        ).text.split(":")
                        song_mins = int(song_mins)
                        song_seconds = int(song_seconds)
                        explicit_song = Song(
                            title=song_title,
                            artist=song_artist,
                            explicit=song_explicit,
                            mins=song_mins,
                            seconds=song_seconds,
                        )
                        if censored_song == explicit_song:
                            # Right click the searched_song
                            actions = ActionChains(driver)
                            actions.context_click(searched_song).perform()
                            try:
                                add_to_playlist_button = WebDriverWait(
                                    driver, 100
                                ).until(
                                    EC.element_to_be_clickable(
                                        (By.CLASS_NAME, "wC9sIed7pfp47wZbmU6m")
                                    )
                                )
                                add_to_playlist_button.click()
                            except:
                                print("failed finding add_to_playlist")
                            try:
                                find_playlist = WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located(
                                        (By.CLASS_NAME, "QZhV0hWVKlExlKr266jo")
                                    )
                                )[1]
                                find_playlist.clear()
                                find_playlist.send_keys(EXPLICIT_PLAYLIST)
                            except:
                                print("failed finding find_playlist")
                            try:
                                playlist_button = WebDriverWait(driver, 100).until(
                                    EC.element_to_be_clickable(
                                        (
                                            By.XPATH,
                                            f"//button[.//text()='{EXPLICIT_PLAYLIST}']",
                                        )
                                    )
                                )
                                playlist_button.click()
                            except:
                                print("failed finding playlist_button")
                        go_back()
                        return explicit_song
                go_back()
                return None
            except:
                print("q1")
        except:
            print("q2")
    else:
        return None


def go_back():
    try:
        back_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ql0zZd7giPXSnPg75NR0"))
        )
        back_button.click()
    except:
        driver.quit()


def check_all_songs():
    try:
        body = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main']/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div",
                )
            )
        )
    except:
        driver.quit()
    scroll_count = 15  # Adjust the number of scrolls as needed
    for i in range(1, scroll_count + 1):
        liked_song = get_liked_song(i)
        explict = check_for_explicit(liked_song)
        body.send_keys(Keys.ARROW_DOWN)


def main():
    driver.get(SPOTIFY)
    get_login_page()
    enter_credentials()
    get_liked_page()
    # check_all_songs()
    # liked_song = get_liked_song(13)
    # print(liked_song.title)
    # check_for_explicit(liked_song)


if __name__ == "__main__":
    main()
