# Поиск вакансий
import requests
import pprint

url = 'https://api.hh.ru/vacancies'

where = input('Где искать вакансию?')
query_string = input('Строка запроса?')

params = {
    'text': 'NAME:(Python OR Java) AND COMPANY_NAME:(1 OR 2 OR YANDEX) AND (DJANGO OR SPRING)',
    # есть страницы т.к. данных много
    'page': 1
}

result = requests.get(url, params=params).json()

pprint.pprint(result)
print(result['items'][0]['url'])
print(result['items'][0]['alternate_url'])