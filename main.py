from fastapi import FastAPI
import sqlite3
import uvicorn
import argparse
import sys

app = FastAPI()

with sqlite3.connect("books.db") as conn:
    c = conn.cursor()
    # проверяем создана ли таблица
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books' ''')
    if not c.fetchone()[0]:
        c.execute('CREATE TABLE books (title TExT, pages INT)')
        conn.commit()


@app.get('/')
def home():
    with sqlite3.connect("books.db") as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM books')
        return dict(c.fetchall())


@app.post('/create_book/{title}/{pages}')
def create_book(title: str, pages: int):
    with sqlite3.connect("books.db") as conn:
        c = conn.cursor()
        # проверяем есть ли книга в таблице
        c.execute('SELECT COUNT(*) FROM books WHERE title=?', (title,))
        if not c.fetchone()[0]:
            c.execute('INSERT INTO books VALUES (?,?)', (title, pages))
            conn.commit()
            return 'Success'
        else:
            return {'Error': title + ' already in the library'}


@app.get('/read_book/{title}')
def read_book(title: str):
    with sqlite3.connect("books.db") as conn:
        c = conn.cursor()
        # проверяем есть ли книга в таблице
        c.execute('SELECT COUNT(*) FROM books WHERE title=?', (title,))
        if c.fetchone()[0]:
            c.execute('SELECT * FROM books WHERE title=?', (title, ))
            return dict([c.fetchone()])
        else:
            return {'Error': title + ' not in the library'}


@app.put('/update_book/{title}/{pages}')
def update_book(title: str, pages: int):
    with sqlite3.connect("books.db") as conn:
        c = conn.cursor()
        # проверяем есть ли книга в таблице
        c.execute('SELECT COUNT(*) FROM books WHERE title=?', (title,))
        if c.fetchone()[0]:
            c.execute('UPDATE books SET pages=? WHERE title=?', (pages, title))
            conn.commit()
            return 'Success'
        else:
            return {'Error': title + ' not in the library'}


@app.delete('/delete_book/{title}')
def delete_book(title: str):
    with sqlite3.connect("books.db") as conn:
        c = conn.cursor()
        # проверяем есть ли книга в таблице
        c.execute('SELECT COUNT(*) FROM books WHERE title=?', (title,))
        if c.fetchone()[0]:
            c.execute('DELETE FROM books WHERE title=?', (title,))
            conn.commit()
            return 'Success'
        else:
            return {'Error': title + ' not in the library'}


@app.delete('/delete_all')
def delete_all():
    with sqlite3.connect("books.db") as conn:
        c = conn.cursor()
        c.execute('DELETE FROM books')
        conn.commit()
        return 'Success'


def createParser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default='8000')
    parser.add_argument('-d', '--debug', action='store_true')
    return parser


if __name__ == '__main__':

    parser = createParser()
    namaspace = parser.parse_args(sys.argv[1:])

    if namaspace.debug:
        uvicorn.run("main:app", host=namaspace.host, port=int(namaspace.port), reload=True, log_level='debug')
    else:
        uvicorn.run("main:app", host=namaspace.host, port=int(namaspace.port))