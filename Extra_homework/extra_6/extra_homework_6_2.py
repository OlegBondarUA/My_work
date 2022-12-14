import json
import sqlite3
from sqlite3 import *


def create_connect(path):
    try:
        con = connect(path)
        return con
    except Error as error:
        print(error)


def execute_build(con, query):
    try:
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except Error as error:
        print(error)


conn = sqlite3.connect('laptop_2.db')


def execute_select(con, query):
    try:
        cursor = con.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return res
    except Error as error:
        print(error)


query_build_laptop_table = """
CREATE TABLE IF NOT EXISTS laptops_2 (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    img TEXT,
    title TEXT,
    price TEXT,
    status TEXT,
    link TEXT
    );
"""


with open('Extra_homework/laptops.json', 'r') as file:
    data = json.load(file)


def main():

    execute_build(conn, query_build_laptop_table)

    for value in data:
        query_add_rows = f"""
            INSERT INTO
                laptops_2 (img, title, price, status, link)
            VALUES (
                '{value['img']}',
                '{value['title']}', 
                '{value['price']}', 
                '{value['status']}', 
                '{value['link']}'
                );
            """

        execute_build(conn, query_add_rows)


if __name__ == '__main__':
    main()
