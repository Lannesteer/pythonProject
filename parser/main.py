import os
import requests
import random
import json
from bs4 import BeautifulSoup as bs
from fake_headers import Headers as H
from urllib.parse import urlparse


class Parse(object):

    def __init__(self, url, from_file=None):
        self.url = url
        self.headers = H().generate()
        self.category = urlparse(url).path.split('/')[-2]
        if from_file:
            with open(from_file, "r", encoding='UTF-8') as f:
                self.soup = bs(f.read(), "html5lib")
        else:
            self.soup = bs(requests.get(self.url, headers=self.headers).text, "html5lib")

    def save_file(self, path_file):
        if not os.path.exists(path_file):
            os.makedirs(path_file)

        filename = f"{path_file}/{self.category}.html"
        with open(filename, "w", encoding='UTF-8') as fileW:
            fileW.write(str(self.soup))
        return filename

    def extract_data(self):
        data = self.soup.find_all('script')
        main_json = {}
        for _length in data:
            _length = str(_length).split("\n")
            for _len in _length:
                if "window.digitalData =" in _len:
                    main_json["digitalData"] = json.loads(_len.split("= ")[1].replace(';', ''))
                elif "window.digitalDataCache =" in _len:
                    main_json["digitalDataCache"] = json.loads(_len.split("= ")[1].replace(';', ''))
        return main_json


def get_data(url="https://street-beat.ru/cat/man/obuv/", path="data"):  # если нужно спарсить другую категорию меняем
    # название категории в конце url
    pp = Parse(url)
    path_file = f"{path}/{pp.category}"
    if os.path.exists(path_file):
        print("Using existing file:", path_file)
        files = os.listdir(path_file)
        html_file = f'{path_file}/{random.choice([f for f in files if f.endswith(".html")])}'
        print("Using HTML file:", html_file)
        pp = Parse(url, from_file=html_file)
    else:
        print("Downloading HTML...")
        html_file = pp.save_file(path_file)
        print("Saved HTML file:", html_file)

    json_file = f"{path}/{pp.category}.json"
    print("Processing data...")
    data = pp.extract_data()
    print("Saving JSON file:", json_file)
    with open(json_file, 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    get_data()
