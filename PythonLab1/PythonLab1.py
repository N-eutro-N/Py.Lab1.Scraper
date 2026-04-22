import os
import requests
from bs4 import BeautifulSoup
import time
import random

def save_review(folder, idx, film_title, text):
    filename = str(idx).zfill(4) + '.txt'
    path = os.path.join('dataset', folder, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(film_title + '\n')
        f.write(text.strip())

films = [
    ('89515', 'Гарри Поттер и Принц-полукровка'),
    ('251733', 'Аватар'),
    ('258687', 'Интерстеллар'),
    ('447', 'Звёздные войны: Эпизод 6 – Возвращение Джедая'),
    ('32898', 'Достучаться до небес'),
    ('111543', 'Темный рыцарь'),
    ('462682', 'Волк с Уолл-стрит'),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}

TARGET_COUNT = 1000
good_count, bad_count = 0, 0
good_idx, bad_idx = 0, 0
per_page = 50

for film_id, film_title in films:
    if good_count >= TARGET_COUNT and bad_count >= TARGET_COUNT:
        break

    for status in ['good', 'bad']:
        if (status == 'good' and good_count >= TARGET_COUNT) or \
           (status == 'bad' and bad_count >= TARGET_COUNT):
            continue

        page = 1
        while True:
            if (status == 'good' and good_count >= TARGET_COUNT) or \
               (status == 'bad' and bad_count >= TARGET_COUNT):
                break

            url = f"https://www.kinopoisk.ru/film/{film_id}/reviews/ord/date/status/{status}/perpage/{per_page}/page/{page}/"
            print(f"Фильм: {film_title}, статус: {status}, страница: {page}")

            try:
                delay = random.uniform(2, 5)
                time.sleep(delay)

                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code != 200:
                    print(f"  Статус код: {response.status_code}. Прерываем страницу.")
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                reviews = soup.find_all('div', class_='response')

                if not reviews:
                    print("  Отзывы не найдены.")
                    break

                for review in reviews:
                    if status == 'good' and good_count >= TARGET_COUNT:
                        break
                    if status == 'bad' and bad_count >= TARGET_COUNT:
                        break

                    spoiler = review.find('span', class_='spoiler_content')
                    brand_words = review.find('div', class_='brand_words')
                    text = spoiler.text if spoiler else (brand_words.text if brand_words else "")

                    if text:
                        if status == 'good':
                            save_review('good', good_idx, film_title, text)
                            good_count += 1
                            good_idx += 1
                        else:
                            save_review('bad', bad_idx, film_title, text)
                            bad_count += 1
                            bad_idx += 1

                print(f"  Собрано: +{good_count} | -{bad_count}")
                page += 1

            except requests.exceptions.RequestException as e:
                print(f"  Ошибка запроса: {e}")
                time.sleep(10)  
                break
            except Exception as e:
                print(f"  Непредвиденная ошибка: {e}")
                break

print(f"\nСбор завершён. Положительных: {good_count}, отрицательных: {bad_count}")