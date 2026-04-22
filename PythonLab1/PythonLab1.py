import requests
from bs4 import BeautifulSoup

FILM_ID = '6695' 
STATUS = 'good'     
PAGE = 1
PER_PAGE = 10

url = f"https://www.kinopoisk.ru/film/{FILM_ID}/reviews/ord/date/status/{STATUS}/perpage/{PER_PAGE}/page/{PAGE}/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Загружаем: {url}")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = soup.find_all('div', class_='response')
    print(f"Найдено рецензий: {len(reviews)}")

    for i, review in enumerate(reviews, 1):
        spoiler = review.find('span', class_='spoiler_content')
        brand_words = review.find('div', class_='brand_words')
        text = spoiler.text if spoiler else (brand_words.text if brand_words else "Текст не найден")
        print(f"\n--- Рецензия {i} ---")
        print(text.strip())
else:
    print(f"Ошибка загрузки страницы. Код: {response.status_code}")
