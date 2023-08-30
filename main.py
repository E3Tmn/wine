from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from dotenv import load_dotenv
import os
import argparse


def fetch_booze():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default=os.getenv("FILE_WITH_BOOZE"))
    args = parser.parse_args()
    excel_data_df = pandas.read_excel(args.filename, sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)
    alcohol_df = excel_data_df.to_dict(orient='records')
    cards_for_site = collections.defaultdict(list)
    for product in alcohol_df:
        cards_for_site[product['Категория']].append(product)
    return cards_for_site


def get_difference():
    word = "лет"
    YEAR_OF_FOUNDATION = 1920
    time_diff = datetime.datetime.today().year - YEAR_OF_FOUNDATION
    if time_diff % 10 == 1:
        word = 'год'
    elif time_diff % 10 > 1 and time_diff % 10 < 5:
        word = 'года'
    return f'{time_diff} {word}'


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        time=get_difference(),
        products=fetch_booze()
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
