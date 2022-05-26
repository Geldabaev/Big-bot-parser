# дает все url страниц пагинации
import requests
from bs4 import BeautifulSoup


def get_total_pages(url):
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    sylky = []
    # Завернем всё в try except на случае если нет пагинации
    url_html = url
    try:
        html = requests.get(url_html, headers=headers).text
        pagenation = url_html + '?list_page='
        # сохраняем весь сайт в файл html и будем рабатать с ним, делается это для того чтобы мы не получили бан от сайта за частые запросы
        with open("index1.html", "w", encoding='utf-8') as file:
            file.write(html)

        # откроем созданный нами файл, и сохраним код из него в переменноую
        with open("index1.html", encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'lxml')

        pages = soup.find('div', class_='navigation block-universal clear gray').find_all('span')[-1].text
        for i in range(1, int(pages) + 1):
            # print(i)
            result = pagenation + str(i)
            result = result.strip()
            # print(result)
            sylky.append(result)
        # print(sylky)
        return sylky
    except:
        pagenation = url_html + "/" + '?list_page=1'
        pagenation = pagenation.strip()
        sylky.append(pagenation)
        # print(sylky)
        return sylky


