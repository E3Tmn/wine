from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections


def get_difference():
    word = "лет"
    time_diff = datetime.datetime.today().year - 1920
    if time_diff % 10 == 1:
        word = 'год'
    elif time_diff % 10 > 1 and time_diff % 10 < 5:
        word = 'года'
    return f'{time_diff} {word}'


def main():
    excel_data_df = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)
    list_wine = (excel_data_df.to_dict(orient='records'))

    wine_data = collections.defaultdict(list)
    for product in list_wine:
        wine_data[product['Категория']].append(product)

    template = env.get_template('template.html')
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    rendered_page = template.render(
        time=get_difference(),
        products=wine_data
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    main()
    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
