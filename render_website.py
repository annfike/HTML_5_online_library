# -*- coding: utf-8 -*-

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

def on_reload():
    with open("books.json", "r") as my_file:
        books_json = my_file.read()

    books = json.loads(books_json)

    for book in books:
        book['Обложка'] = book['Обложка'].replace('\\', '/')


    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

#server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
#server.serve_forever()