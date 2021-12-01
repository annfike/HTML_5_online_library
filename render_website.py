# -*- coding: utf-8 -*-

import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def on_reload():
    with open("books.json", "r") as file:
        books = json.load(file)
    for book in books:
        book['Обложка'] = book['Обложка'].replace('\\', '/')
        book['Ссылка'] = book['Ссылка'].replace('\\', '/')

    books_on_page = 10
    pages = list(chunked(books, books_on_page))

    os.makedirs('pages', exist_ok=True)
    for number, page in enumerate(pages, 1):
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('template.html')

        books_chunked = list(chunked(page, 2))

        rendered_page = template.render(
            books=books_chunked,
            current_page=number,
            last_page=len(pages),      
            before_last_page=len(pages)-1,  
        )

        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

