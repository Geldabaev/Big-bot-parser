import requests
from bs4 import BeautifulSoup
import help_file
from help_file import encod_work, agent_or_prox_random, download_html, soup, selenium_nou_bot
import json
import os.path
from pagination2 import get_total_pages
import main_product2

headers = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"}


def get_data():
    odin = 1
    # ссылка на json с ссылками на все категории и под категории
    url = "https://www.xcom-shop.ru/var-static-18/var/catalog/menu.js"
    r = requests.get(url=url, headers=headers).text

    # исправим json
    r = r.split("=")[1].strip()[:-1]

    # чтобы не собирать ссылки по страницам, так как из-за это есть риск бана из-за большого количества запросов, сохраняем скрытую страницу js, перводим в json
    with open("index.json", "w", encoding="utf-8") as file:
        file.write(r)

    # открываем json
    with open("index.json", encoding='utf-8') as file:
        src = file.read()




    # переводим json в python объект
    elements = json.loads(src)
    # print(elements)
    # создадим папку data для наших деректории и поддеректории
    if not os.path.exists("data"):
        os.mkdir("data")


    # берем сначала заголвки категории
    result = {}
    for i in elements:
        url = "https://www.xcom-shop.ru/" + "catalog/" + elements[i]['value']['name_url']
        name = elements[i]['value']['name']
        result[name] = url
        # print(url)
        # создадим папки
        if not os.path.exists(f"data/{name}"):
            os.mkdir(f"data/{name}")
    # под папки
    for k in elements:
        pod_result = {}
        name = elements[k]['value']['name']
        url = "https://www.xcom-shop.ru/" + "catalog/" + elements[k]['value']['name_url']
        # k id категории
        id_pod_new = k
        for q in elements[k]['in']:
            # q id подкатегории
            # if id_pod_old != id_pod_new:
            name_pod = elements[k]['in'][q]['value']['name']
            name_pod = name_pod.replace('/', "_")
            url_pod = elements[k]['in'][q]['value']['name_url']
            result_url = url + "/" + url_pod
            print("Категория: ", name)
            print("Подкатегория: ", name_pod)
            # print(result_url)
            if not os.path.exists(f"data/{name}/{name_pod}"):
                os.mkdir(f"data/{name}/{name_pod}")

            print("__________________________________")
            # вернем url с пагинациями
            sylky = get_total_pages(result_url)
            # соберем ссылки на товары
            categ_csv = 0
            for i in sylky:
                main_product2.start(i, q)

                # соберем все уникальные характеристики для дальнейщего сравнения с ними
                main_product2.characteristics_all(q)
                # сохарняем в csv
                main_product2.get_data2(name, name, name_pod, q, categ_csv)
                categ_csv = 1


def main():
    get_data()
    # удаляем лишние папки
    help_file.dir_file('Пакеты сервисных услуг', 'Распродажа', 'Услуги', 'Уцененные товары', 'file_html', 'file_json')


if __name__ == '__main__':
    main()