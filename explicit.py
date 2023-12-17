from selenium import webdriver
from bs4 import BeautifulSoup
import requests, time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from dotenv import load_dotenv

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
SPOTIFY = "https://open.spotify.com/"

load_dotenv()
SPOTIFY_EMAIL = os.getenv("SPOTIFY-EMAIL")
SPOTIFY_PASSWORD = os.getenv("SPOTIFY-PASSWORD")

print(SPOTIFY_EMAIL)
print(SPOTIFY_PASSWORD)

service = ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get(SPOTIFY)


def get_login_page():
    print("done sleep")
    login_button = driver.find_element(
        By.CLASS_NAME,
        "fyugtm",
    )
    print("loginbutton", login_button)
    login_button.click()


def main():
    get_login_page()


if __name__ == "__main__":
    main()
