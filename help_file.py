import requests
from bs4 import BeautifulSoup
import os.path
import random
import time
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import shutil



def encod_work(encod):
    "исправляем ошибки в кадировках"
    rep = ["\u20bd", "\xb3", "\xb2", "\xd8", "\u2011", '\u2011', "\xe9", "\xed", "\u25ba", "\u2103", "\uff08", "\uff09", "\u2714", "\u0130", "\u0131", "\xdc", "\xfc", "\u015f"]
    for item in rep:
        if item in encod:
            encod = encod.replace(item, "")
    return encod


def agent_or_prox_random():
    "меняем рандомна прокси и юзеры для безопасности"
    proxies1 = {"https": "http://88.218.74.244:8000"}
    proxies2 = {"https": "http://88.218.74.144:8000"}
    proxies3 = {"https": "http://88.218.73.116:8000"}
    proxies5 = {"https": "http://46.3.178.49:8000"}
    proxies6 = {"https": "http://46.3.178.197:8000"}

    user_agent1 = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
    user_agent2 = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
    user_agent3 = {"accept": "*/*", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}
    user_agent5 = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"}
    user_agent6 = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}


    proxies = [[proxies1, user_agent1], [proxies2, user_agent2], [proxies3, user_agent3], [proxies5, user_agent5], [proxies6, user_agent6]]

    proxii = random.choice(proxies)

    user = proxii[1]
    prox = proxii[0]
    print("proxy изменился")
    print("user agent изменился")


    return user, prox


def download_html(url, name_html, user, prox):
    "сохранение страниц"
    s = requests.Session()
    src = s.get(url=url, headers=user, proxies=prox)

    if not os.path.exists("data"):
        os.mkdir("data")

    # сохраним весь главный сайт
    with open("data/name_html.html", "w", encoding='utf-8') as file:
        file.write(src)

    #откроем сохраненный сайт
    with open("data/name_html.html", encoding="utf-8") as file:
        src = file.read()

    return src


def soup(src):
    "готовим суп"
    soup = BeautifulSoup(src.text, 'lxml')
    return soup


def selenium_nou_bot(url, page):
    "на крайний случий для обхода блокировок"
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('--proxy-server=46.3.182.109:8000')
    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # старый метод
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # новый метод
    s = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    url = url
    driver.get(url)
    time.sleep(random.randint(30, 40))

    # сохраним весь главный сайт
    with open(f"data/index_{page}.html", "w", encoding='utf-8') as file:
        file.write(driver.page_source)

    # закроем браузер
    driver.quit()

    # откроем сохраненный сайт
    with open(f"data/index_{page}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    return soup

def dir_file(name, name2, name3, name4, name5, name6):
    shutil.rmtree(name, ignore_errors=True)
    shutil.rmtree(name2, ignore_errors=True)
    shutil.rmtree(name3, ignore_errors=True)
    shutil.rmtree(name4, ignore_errors=True)
    shutil.rmtree(name5, ignore_errors=True)
    shutil.rmtree(name6, ignore_errors=True)


def punctuation(encod):
    rep = ["!", '"', "#", "$", "%", "&", "'", "(", ")", '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
           '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    for item in rep:
        if item in encod:
            encod = encod.replace(item, "")
    return encod