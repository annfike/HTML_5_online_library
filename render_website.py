# -*- coding: utf-8 -*-

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from more_itertools import chunked
import os


def on_reload():
    with open("books.json", "r") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json)
    for book in books:
        book['Обложка'] = book['Обложка'].replace('\\', '/')
        book['Ссылка'] = book['Ссылка'].replace('\\', '/')

    pages = list(chunked(books, 10))

    os.makedirs('pages', exist_ok=True)
    for number, page in enumerate(pages, 1):
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('template.html')

        books_chunked = list(chunked(page, 2))
        prev_page = number - 1
        current_page = number
        next_page = number + 1
        last_page = len(pages)
        rendered_page = template.render(
            books=books_chunked,
            prev_page=prev_page,
            current_page=current_page,
            next_page=next_page,
            last_page=last_page,
        )

        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

#server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#server.serve_forever()