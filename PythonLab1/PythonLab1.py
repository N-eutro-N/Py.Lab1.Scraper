import os
import requests
from bs4 import BeautifulSoup
import time
import random

def save_review(folder, idx, film_title, text):
    filename = str(idx).zfill(4) + '.txt'
    path = os.path.join('dataset', folder, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,'w',encoding='utf-8') as f:
        f.write(film_title + '\n')
        f.write(text.strip())

good_count, bad_count = 0, 0
good_idx, bad_idx = 0, 0

films = [
    ('6695', 'Звёздные войны: Эпизод 1 – Скрытая угроза (1999)'),
    ('844', 'Звёздные войны: Эпизод 2 – Атака клонов (2002)'),
    ('5619', 'Звёздные войны: Эпизод 3 – Месть ситхов (2005)'),
    ('333', 'Звёздные войны: Эпизод 4 – Новая надежда (1977)'),
    ('338', 'Звёздные войны: Эпизод 5 – Империя наносит ответный удар (1980)'),
    ('447', 'Звёздные войны: Эпизод 6 – Возвращение Джедая (1983)'),
    ('714888', 'Звёздные войны: Пробуждение силы (2015)'),
    ('718223', 'Звёздные войны: Последние джедаи (2017)'),
    ('718222', 'Звёздные войны: Скайуокер. Восход (2019)'),
    ('89515', 'Гарри Поттер и Принц-полукровка'),
    ('707407', 'Викинг'),
    ('407636', 'Гарри Поттер и Дары Смерти: Часть II'),
    ('582101', 'Дивергент'),
    ('251733', 'Аватар'),
    ('258687', 'Интерстеллар'),
    ('462682', 'Волк с Уолл-стрит'),
    ('111543', 'Темный рыцарь'),
    ('32898', 'Достучаться до небес'),
    ('9691', 'Бесславные ублюдки'),
    ('406408', 'Законопослушный гражданин'),
    ('649917', 'По соображениям совести')
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}

start_script_time = time.time()

for film_id, film_title in films:
    if good_count >= 1000 and bad_count >= 1000:
        print("Собрано достаточное количество отзывов.")
        break

    per_page = 50
    
    for status in ['good', 'bad']:
        if status == 'good' and good_count >= 1000:
            continue
        if status == 'bad' and bad_count >= 1000:
            continue

        page = 1
        
        while True:
            if status == 'good' and good_count >= 1000:
                break
            if status == 'bad' and bad_count >= 1000:
                break

            url = f"https://www.kinopoisk.ru/film/{film_id}/reviews/ord/date/status/{status}/perpage/{per_page}/page/{page}/"
            
            print(f"Скачиваем страницу {page} ({status}) для фильма {film_title}...")
            
            try:
                delay = random.uniform(2, 5)
                time.sleep(delay)

                page_start_time = time.time()

                r = requests.get(url, headers=headers)
                
                if r.status_code != 200:
                    print(f"Статус код: {r.status_code}. Возможно, блокировка или конец страниц.")
                    break
                    
                soup = BeautifulSoup(r.text, 'html.parser')
                reviews = soup.find_all('div', class_='response')
                
                if not reviews:
                    print(f"  -> Отзывы не найдены!")
                    print(f"  -> Код ответа: {r.status_code}")
                    break
                    
                for review in reviews:
                    if status == 'good' and good_count >= 1000:
                        break
                    if status == 'bad' and bad_count >= 1000:
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
                
                page_end_time = time.time()
                page_duration = page_end_time - page_start_time
                
                total_reviews = good_count + bad_count
                total_elapsed = page_end_time - start_script_time
                avg_time_per_review = total_elapsed / total_reviews if total_reviews > 0 else 0
                
                print(f"  -> Страница обработана за {page_duration:.2f} сек. "
                      f"Всего отзывов: {total_reviews}   |   (+ {good_count} | {bad_count} -) "
                      f"Среднее время/отзыв: {avg_time_per_review:.4f} сек.")
                
                page += 1
                
            except Exception as e:
                print(f"Ошибка: {e}")
                time.sleep(10)
                break

end_script_time = time.time()
total_script_duration = end_script_time - start_script_time
total_reviews = good_count + bad_count


print(f"СБОР ДАННЫХ ЗАВЕРШЕН")
print(f"Общее время работы: {total_script_duration:.2f} сек ({total_script_duration/60:.2f} мин)")
print(f"Всего собрано отзывов: {total_reviews}")
print(f"Положительных: {good_count}")
print(f"Отрицательных: {bad_count}")
if total_reviews > 0:
    print(f"Итоговое среднее время на отзыв: {total_script_duration / total_reviews:.4f} сек")
