import csv
import requests
from datetime import datetime
from multiprocessing import Pool
from bs4 import BeautifulSoup
from urllib3.util import url


def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')

    links = []

    for td in tds:
        a = td.find('a', class_='currency-name-container').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links


def text_before_word(text, word):
    line = text.split(word)[0].strip()
    return line


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        name = text_before_word(soup.find('title').text, 'price')
    except:
        name = ''
    try:
        price = text_before_word(soup.find('div', class_='col-xs-6 col-sm-8 col-md-4 text-left').text, 'USD')
    except:
        price = ''
    data = {'name': name,
            'price': price}
    return data


def write_csv(data):
    with open('coinmarket.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['name'],
                         data['price']))

        print(data['name'], 'parsed')


def make_all(link):
    html = get_html(link)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'

    all_links = get_all_links(get_html(url))

    # for index, url in enumerate(all_links):

    with Pool(60) as p:
        p.map(make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))
    a = input()


if __name__ == '__main__':
    main()
