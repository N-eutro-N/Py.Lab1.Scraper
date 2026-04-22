import os
import requests
from bs4 import BeautifulSoup
import time

def save_review(folder, idx, film_title, text):
    filename = str(idx).zfill(4) + '.txt'
    path = os.path.join('dataset', folder, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(film_title + '\n')
        f.write(text.strip())

FILM_ID = '89515'
FILM_TITLE = 'Гарри Поттер и Принц-полукровка'
STATUS = 'good' 
PER_PAGE = 50
MAX_REVIEWS = 100      

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

count = 0
page = 1

while count < MAX_REVIEWS:
    url = f"https://www.kinopoisk.ru/film/{FILM_ID}/reviews/ord/date/status/{STATUS}/perpage/{PER_PAGE}/page/{page}/"
    print(f"Страница {page} ({STATUS})...")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка загрузки страницы {page}. Код: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = soup.find_all('div', class_='response')

    if not reviews:
        print("Рецензии закончились.")
        break

    for review in reviews:
        if count >= MAX_REVIEWS:
            break

        spoiler = review.find('span', class_='spoiler_content')
        brand_words = review.find('div', class_='brand_words')
        text = spoiler.text if spoiler else (brand_words.text if brand_words else "")

        if text:
            save_review(STATUS, count, FILM_TITLE, text)
            count += 1

    print(f"  Собрано {count} рецензий")
    page += 1
    time.sleep(1)

print(f"Готово! Сохранено {count} рецензий в папке dataset/{STATUS}")