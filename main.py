import requests
import json
import pprint


def search_vacancies(keyword, region):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': keyword,
        'area': region,
        'per_page': 10,  # Максимальное количество вакансий на одной странице
        'page': 0
    }

    response = requests.get(url, params=params)
    result = response.json()

    pprint.pprint(result)  # Вывод содержимого ответа API для отладки

    return result


def analyze_vacancies(vacancies):
    total_vacancies = vacancies['found']
    average_salary = calculate_average_salary(vacancies['items'])
    skills_counter = {}
    vacancies_with_requirement = {}

    for vacancy in vacancies['items']:
        if 'snippet' in vacancy and 'requirement' in vacancy['snippet']:
            requirements = vacancy['snippet']['requirement']
            if requirements:
                requirements = requirements.lower().split(', ')
                for requirement in requirements:
                    if requirement in skills_counter:
                        skills_counter[requirement] += 1
                    else:
                        skills_counter[requirement] = 1

                    if requirement in vacancies_with_requirement:
                        vacancies_with_requirement[requirement].append(vacancy['name'])
                    else:
                        vacancies_with_requirement[requirement] = [vacancy['name']]

    total_requirements = sum(skills_counter.values())
    skill_percentages = {skill: (count / total_requirements) * 100 for skill, count in skills_counter.items()}

    return total_vacancies, average_salary, skill_percentages, vacancies_with_requirement


def calculate_average_salary(vacancies):
    total_salary = 0
    count = 0

    for vacancy in vacancies:
        salary = vacancy['salary']
        if salary and salary.get('from') is not None:  # Проверка наличия значения 'from'
            total_salary += salary['from']
            count += 1

    if count > 0:
        average_salary = total_salary / count
        return average_salary
    else:
        return None


def save_result(result, filename):
    skill_percentages = result[2]
    with open(filename, 'w') as file:
        json.dump(skill_percentages, file, indent=4)

def print_skill_percentages(skill_percentages):
    print("Процентное отношение требований к общему количеству вакансий:")
    for skill, percentage in skill_percentages.items():
        print(f"{skill}: {percentage:.1f}%")



# Пример использования
keyword = 'Python OR Java AND SQL'
region = '113'

vacancies = search_vacancies(keyword, region)
result = analyze_vacancies(vacancies)

filename = 'vacancy_analysis.json'
save_result(result, filename)

# Открываем файл с данными
with open(filename, 'r') as file:
    # Загружаем JSON-данные
    data = json.load(file)

# Выводим данные
print()
print('*' * 100)
print('Выводим данные из списка "json"')
pprint.pprint(data)


with open('vacancy_analysis.json', 'r') as file:
    skill_percentages = json.load(file)

print()
print('*' * 100)
print("Процентное отношение требований к общему количеству вакансий:")
for skill, percentage in skill_percentages.items():
    print(f"Skill: {skill}, Percentage: {percentage:.1f}%")



