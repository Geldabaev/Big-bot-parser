# парсит все товары на указанной url странице и сохраняет в csv
import os.path
import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
from help_file import encod_work, agent_or_prox_random, punctuation
import re


def start(url, q):
    # сразу заходим по прямой ссылке на нужную нам категорию
    user, proxy = agent_or_prox_random()
    time.sleep(random.randint(4, 7))
    req = requests.get(url=url, headers=user, proxies=proxy)
    src = req.text

    #сохраняем сайт в html
    with open("xcom-shop.html", "w", encoding="utf-8") as file:
        file.write(src)

    # открываем сохраненный нами файл, и сохраняем содержимое в переменную
    with open("xcom-shop.html", encoding="utf-8") as file:
        src = file.read()


    # варим с супом для удобства работы
    soup = BeautifulSoup(src, "lxml")

    # создадим папки для json файлов
    if not os.path.exists('file_json'):
        os.mkdir('file_json')

    # создадим папки для json файлов
    if not os.path.exists('file_html'):
        os.mkdir('file_html')

    # все товары в общем
    # на случай если товаров нет, завернем в try except
    try:
        iter = soup.find_all('div', class_="catalog_item__inner catalog_item__inner--tiles")
        # print(iter)
        # собирём ссылки на товары, чтобы потом заходить на них, и брать данные о харектеристиках
        all_products_hrefs = []
        for i in iter:
            all_products_ap = i.find('div', class_="catalog_item__description_wrapper catalog_item__description_wrapper--tiles")
            all_products_hrefs.append(all_products_ap)
            # print(all_products_hrefs)

        all_categories_vladelec = {}
        for item in all_products_hrefs:
            item_text = item.find('div', class_='catalog_item__type catalog_item__type--tiles').text
            item_href = "https://www.xcom-shop.ru" + item.find('a').get("href")
            # print(f"{item_text}: {item_href}")
            # сохраним всё в словарь
            # так как у нас одинаковые название у некоторых товаров, а ключи могут быть только уникальные, и рас так, то-
            # одинаковы перезапишут своих близнецов, и чтобы этого небыло сделаем ссылки ключами(потому, что ссылки не повторяются), а название словарями
            all_categories_vladelec[item_href] = item_text

        # запишем всё в json
        with open(f"file_json/all_categories_vladelec_{q}.json", "w", encoding="cp1251") as file:
            json.dump(all_categories_vladelec, file, indent=4, ensure_ascii=False)
    except:
        # запишем всё в json
        with open(f"file_json/all_categories_vladelec_{q}.json", "w", encoding="cp1251") as file:
            json.dump("", file, indent=4, ensure_ascii=False)


def characteristics_all(q):
    # собирает все уникальные характеристики для дальнейшего сравнения

    # выведем полученную информацию в переменную
    with open(f'file_json/all_categories_vladelec_{q}.json', encoding="cp1251") as file:
        all_categories = json.load(file)
        print("Работаю")

    harak = []
    result_har = {}
    count = 0
    har_count = 0
    for category_href, category_name in all_categories.items():
        if count > 24:
            break
        # print(category_name, ": ", category_href)
        category_name = category_name.replace("'", "").replace('"', "")
        print(f"Хожу по товару: {category_name}")
        time.sleep(random.randint(5, 10))
        user, proxy = agent_or_prox_random()
        response = requests.get(category_href, headers=user, proxies=proxy)

        # пока собираем характеристики сохраняем эти страницы чтобы по два раза поним не ходить во время сравнения
        with open(f"file_html/xcom-shop-har{har_count}.html", "w", encoding="utf-8") as file:
            file.write(response.text)

        # открываем сохраненный нами файл, и сохраняем содержимое в переменную
        with open(f"file_html/xcom-shop-har{har_count}.html", encoding="utf-8") as file:
            response = file.read()
        har_count += 1
        soup = BeautifulSoup(response, "lxml")
        print("Собираю все уникальные характеристики")
        # сперва собираем все характеристики потом сравниваем какие есть из собранных у товар
        # там два списка одиноковых, в первом не все характеристики, а в втором все, берем второй
        # завернем в try exept на случае если нет характеристик
        try:
            information2 = soup.find_all('ul', class_='product-block-description__list')[1]
            # print(information2, "********")
            information = information2.find_all('li', class_='product-block-description__item')
            # print(information)
        except:
            # пропускаем итерацию если нет характеристик
            continue
        odin_razny = []
        for i in information:
            opis_name = i.find('div', class_='product-block-description__first-elem').text.strip()
            # исправляем ошибки в кириллице
            opis_name = encod_work(opis_name)
            # если у одного товара есть одинаковые название разных характеристик, то чтобы второй не стер первый в дальнейшем для уникальности, меняем второй добовляя число 2
            if opis_name in odin_razny:
                opis_name = opis_name + "2"
            odin_razny.append(opis_name)
            harak.append(opis_name)
    print("Ждите!")
    print("Все характеристики собраны, теперь некоторые манипуляуии с ними для уникальности")
    #запишем всё в json
    number = 0
    for opis_name in harak:
        result_har[opis_name] = f"характеристика-{number}"
        # исправляем ошибки в кириллице
        number += 1
    with open(f"file_json/characteristics3_{q}.json", "w", encoding="cp1251") as file:
        json.dump(result_har, file, indent=4, ensure_ascii=False)


def get_data2(name_csv, dat_name, dat_n, q, categ_csv):
    # выведем полученную информацию в переменную
    with open(f'file_json/all_categories_vladelec_{q}.json', encoding="cp1251") as file:
        all_categories = json.load(file)

    # выведем полученную информацию в функции def characteristics_all() в переменную
    with open(f"file_json/characteristics3_{q}.json", encoding="cp1251") as file:
        result_new_pos = json.load(file)
        # print(result_new_pos)
    # заголовки нужны только один раз
    if categ_csv == 0:
        # создадим одну заголовку
        with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", encoding="cp1251") as file:
            writer = csv.writer(file, delimiter=';', lineterminator=';')
            writer.writerow(
                [   "Главная категория",
                    "Категория",
                    "Путь к фото",
                    "Наименование"
                ]
            )


    try:
        sravneny = []
        for category_names, category_hrak in result_new_pos.items():
            # заголовки нужны только один раз
            if categ_csv == 0:
                # создадим заголовки характеристик
                with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", encoding="cp1251", newline='') as file:
                    writer = csv.writer(file, delimiter=';', lineterminator=';')
                    writer.writerow(
                        [
                            category_names
                        ]
                    )
            # и добавим всё в список, для дальнейшего сравнения
            sravneny.append(category_names)

        # print(sravneny)
        # -----------------------------------------------------------------------------------#
        # сохраняем характеристики всех товаров
        # переходя по каждой ссылке сохраняем данные о товарах
        produc = 1
        number = 1
        har_count = 0
        for category_href, category_name in all_categories.items():
            print(f"Собираю данные товара {produc}")
            produc += 1

            # для перехода на новую строку
            with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    [
                        ''
                    ]
                )



            # открываем сохраненный нами файлы во время парсинга характеристик
            with open(f"file_html/xcom-shop-har{har_count}.html", encoding="utf-8") as file:
                response = file.read()

            soup = BeautifulSoup(response, "lxml")

            # если есть добавляем, если нет Нет
            try:
                # сравним какие есть у товаров из собранных нами характеристик
                # там два списка одиноковых, в первом не все характеристики, а в втором все, берем второй
                information2 = soup.find_all('ul', class_='product-block-description__list')[1]
                information = information2.find_all('li', class_='product-block-description__item')

                # ссылка на фото и название
                img_down = soup.find('div', class_='card-bundle-preview__main-slider-wrapper').find('li').find('img').get('data-lazy')
                name_photo = soup.find('h1', id='card-main-title').text.strip().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")

                # изменим название с помощью регулярных выражений
                pattern = "_+"
                name_photo = re.sub(pattern, " ", name_photo).replace("-", " ").replace(" ", "_")

                # print("Ссылка на фото: ", img_down)
                # print("Нзвание фото: ", name_photo)
                # сохраняем фото

                # исправим пунктуацию подходящую для назване в windows
                name_photo = punctuation(name_photo)
                dat_name = punctuation(dat_name)
                dat_n = punctuation(dat_n)

                download_imgs(img_down, name_photo, dat_name, dat_n, number)

                with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", encoding="cp1251", newline='') as file:
                    writer = csv.writer(file, delimiter=';', lineterminator=';')
                    writer.writerow(
                        [
                            dat_name,
                            dat_n,
                            f"C:\data\{dat_name}\{dat_n}\img_{name_photo}_{str(number)}"

                        ]
                    )

                with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", encoding="cp1251", newline='') as file:
                    writer = csv.writer(file, delimiter=';', lineterminator=';')
                    writer.writerow(
                        [
                            category_name
                        ]
                    )

                number += 1

                # print(information)

                for i in sravneny:
                    # print(i)
                    is_name = 1
                    odin_razny = []
                    for y in information:
                        # print(y)
                        name = y.find('div', class_='product-block-description__first-elem').text.strip()
                        opis_name = y.find('div', class_='product-block-description__second-elem').text.strip().replace("/", " ").replace("(", " ").replace(")", " ").replace(",", "")
                        # исправляем кириллицу
                        opis_name = encod_work(opis_name)
                        # print(name, "name????")
                        # print(opis_name, "opisname")
                        if name in odin_razny:
                            name = name + "2"
                        odin_razny.append(name)

                        if name == i:
                            is_name = 2
                            with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", encoding="cp1251", newline='') as file:
                                writer = csv.writer(file, delimiter=';', lineterminator=';')
                                writer.writerow(
                                    [
                                        opis_name
                                    ]
                                )


                    if is_name == 1:
                        nou = 'Нет'

                        with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", encoding="cp1251", newline='') as file:
                            writer = csv.writer(file, delimiter=';', lineterminator=';')
                            writer.writerow(
                                [
                                    nou
                                ]
                            )


            except Exception as ex:
                print("Ошибка: ", ex)
    except:
        with open(f"data/{dat_name}/{dat_n}/{name_csv}.csv", "a", encoding="cp1251", newline='') as file:
            writer = csv.writer(file, delimiter=';', lineterminator=';')
            writer.writerow(
                [
                    "Товаров нет"
                ]
            )




    print("Все данные успешно собраны!!!")


def download_imgs(img_down, name_photo, dat_name, dat_n, number):
    print("сохраняю фото")
    # на случае если нету фото
    try:
        # отправляем запрос на ссылку фото
        time.sleep(random.randint(3, 7))
        user, proxy = agent_or_prox_random()
        r = requests.get(url=img_down, headers=user, proxies=proxy)

        if not os.path.exists(f'data/{dat_name}/{dat_n}/img_{name_photo}_{str(number)}'):
            os.mkdir(f'data/{dat_name}/{dat_n}/img_{name_photo}_{str(number)}')

        # сохраним фото
        with open(f"data/{dat_name}/{dat_n}/img_{name_photo}_{str(number)}/{name_photo}.png", "wb", encoding='cp1251') as file:
            file.write(r.content)
    except Exception as ex:
        print(ex)
        print("не удалось сохранить фото")
