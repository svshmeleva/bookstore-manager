import sqlite3
from tabulate import tabulate
from typing import List, Tuple, Any

class Book():
    
    def __init__(self, title:str, author:str, qty:int, id:int = None) -> None:
        self._id = id
        self._title = title
        self._author = author
        self._qty = qty
    
    @property
    def id(self):
        return self._id
    
    def get_db_info(self) -> List[Any]:
        if self._id is not None:
            return [self._id, self._title, self._author, self._qty]
        else:
            return [self._title, self._author, self._qty]
    
    def get_info(self) -> List[Any]:
        return [self._id, self._title, self._author, self._qty] 

class BookDatabase():

    def __init__(self, db_file_name:str) -> None:
        self._db_file_name = db_file_name
        self._db = sqlite3.connect('ebookstore')
        self._cursor = self._db.cursor()
        self._cursor.execute('''
CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Author TEXT NUT NULL, Qty INT DEFAULT 0)''')
        self._db.commit()
    
    def is_empty(self) -> bool:
        self._cursor.execute("""SELECT * FROM books""")
        row = self._cursor.fetchone()
        return row is None
    
    @property
    def header(self) -> List[str]:
        self._cursor.execute('PRAGMA table_info("books")')
        column_names = [i[1] for i in self._cursor.fetchall()]
        return column_names
    
    def add_book(self, books:List[Book]) -> None:
        for book in books:
            book_info = book.get_db_info()
            if book.id is None:
                self._cursor.execute('''INSERT INTO books (Title, Author, Qty) VALUES(?,?,?)''', book_info)
            else:
                self._cursor.execute('''INSERT INTO books (id, Title, Author, Qty) VALUES(?,?,?,?)''', book_info)
        self._db.commit()

    def search(self, title:str=None, author:str=None, qty:int=None, id:int = None) -> List[Book]:
        list_book = []
        if id is not None:
            rows = self._cursor.execute("""SELECT * FROM books WHERE id = ?""", (id, ))
        for row in rows:
            list_book.append(Book(id=row[0], title=row[1], author=row[2], qty=row[3]))
        return list_book
    
    def close(self) -> None:
        self._db.close()

def print_books(books:List[Book], header:List[str]):
    list_info = [i.get_info() for i in books]
    print(tabulate(list_info, headers=header))






book_db = BookDatabase('ebookstore')

if book_db.is_empty():
    books = [Book(id=3001, title="A Tale of Two Cities", author="Charles Dickens", qty=30), 
            Book(id=3002, title="Harry Potter and the Philosopher's Stone", author="J.K. Rowling", qty=40), 
            Book(id=3003, title="The Lion, the Witch and the Wardrobe", author="C.S. Lewis", qty=25), 
            Book(id=3004, title="The Lord of the Rings", author="J.R.R Tolkien", qty=37), 
            Book(id=3005, title="Alice in Wonderland", author="Lewis Carroll", qty=12)]
    book_db.add_book(books)
    
while True:
    main_menu = input("""\nMain menu:
    1 - Enter book
    2 - Search books (to update or delete)
    3 - View all books
    0 - Exit
    :  """)

    if main_menu == "1":
        pass

    elif main_menu == "2":
        book_list = book_db.search(id=3002)
        print_books(book_list, book_db.header)

    elif main_menu == "3":
        pass

    elif main_menu == "0":
        break

    else:
        print("Wrong enter. Try again please.")

print("Thank you for using BOOK Database")

book_db.close()