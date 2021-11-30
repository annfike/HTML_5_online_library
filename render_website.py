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

    pages = list(chunked(books, books_on_page=10))

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
            current_page_minus3=number - 3,
            current_page_minus2=number - 2,
            current_page_minus1=number - 1,
            current_page=number,
            current_page_plus1=number + 1,
            current_page_plus2=number + 2,
            last_page=len(pages),
            current_page_plus3=number + 3,    
            before_last_page=len(pages) - 1,       
        )

        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

