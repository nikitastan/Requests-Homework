import requests
import json
from datetime import datetime, timedelta
import os


def most_intelligent_hero(list_):
    res = requests.get(url='https://akabab.github.io/superhero-api/api/all.json')
    dict_of_heroes = json.loads(res.content)
    max_intelligence = 0
    for superhero in dict_of_heroes:
        if superhero['name'] in list_ and superhero['powerstats']['intelligence'] > max_intelligence:
            most_intelligent_name = superhero['name']
            max_intelligence = superhero['powerstats']['intelligence']
    print('Самый умный супергеро из списка: ', most_intelligent_name)


class YaUploader:
    def __init__(self, token: str):
        if not token:
            self.token = input('Введите токен: ')
        else:
            self.token = token

    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth '+self.token
        }

    def get_upload_link(self, path_to_file: str):
        headers = self._headers()
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path':  path_to_file,
            'overwrite': 'true'
        }
        res_ = requests.get(url=url, headers=headers, params=params)
        return res_.json()

    def upload(self, path_to_file: str, filename: str):
        headers = self._headers()
        href = self.get_upload_link(path_to_file)['href']

        with open(filename, 'rb') as f:
            res_ = requests.put(href, data=f, headers=headers)
        if res_.status_code == 201:
            return 'Файл успешно загружен'


class StackOver:
    def __init__(self):
        pass

    def fromdate(self):
        date = datetime.date(datetime.today()) - timedelta(days=2)
        return str(date)

    def questions_get(self):
        url = "https://api.stackexchange.com/2.3/questions"
        pagenum = 0
        has_more = True
        len_questions = 0
        while has_more:
            pagenum += 1
            params = {
                "order": "asc",
                "sort": "creation",
                "site": "stackoverflow",
                "tagged": "python",
                "fromdate": self.fromdate(),
                "pagesize": 100,
                "page": pagenum
            }
            res_ = requests.get(url=url, params=params)
            questions = json.loads(res_.content)["items"]
            for question in questions:
                print(f"Question creation date: {datetime.utcfromtimestamp(int(question['creation_date'])).strftime('%d.%m.%y %H:%M:%S')}",
                      f"Question: {question['title']}",
                      f"Tags: {', '.join(question['tags'])}\n", sep="\n")
            len_questions += len(json.loads(res_.content)["items"])
            has_more = json.loads(res_.content)['has_more']
        print(f"Всего вопросов за последние 2 дня: {len_questions}")


if __name__ == '__main__':
    # Задание 1
    list_of_heroes = ['Hulk', 'Captain America', 'Thanos']
    most_intelligent_hero(list_of_heroes)

    # Задание 2
    TOKEN = None
    filename = 'upload_tst.txt'
    path_to_file = os.path.normpath(filename)
    ya = YaUploader(token=TOKEN)
    print(ya.upload(path_to_file, filename))

    # Задание 3
    st = StackOver()
    st.questions_get()
