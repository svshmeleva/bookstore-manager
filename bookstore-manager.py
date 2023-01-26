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

    def search(self,  title:str=None, author:str=None, qty:int=None, id:int = None) -> List[Book]:
        list_book = []
        if id is not None:
            rows = self._cursor.execute("""SELECT * FROM books WHERE id = ?""", (id, ))
        if title is not None:
            if author is not None:
                rows = self._cursor.execute("""SELECT * FROM books WHERE Title LIKE ? and Author LIKE ?""", ('%'+title+'%', '%'+author+'%', ))
            else:
                rows = self._cursor.execute("""SELECT * FROM books WHERE Title LIKE ?""", ('%'+title+'%', ))
        else:
            if author is not None:
                rows = self._cursor.execute("""SELECT * FROM books WHERE Author LIKE ?""", ('%'+author+'%', ))
        
        if id is None and title is None and author is None and qty is None:
            rows = self._cursor.execute("""SELECT * FROM books""")
        
        for row in rows:
            list_book.append(Book(id=row[0], title=row[1], author=row[2], qty=row[3]))
        return list_book
    
    def delete(self, books:List[Book]) -> None:
        for book in books:
            book_info = book.get_info()
            self._cursor.execute("""DELETE FROM books WHERE id = ?""", (book_info[0], ))
        self._db.commit()

    def change(self, books:List[Book]) -> None:
        for book in books:
            book_info = book.get_info()
            self._cursor.execute("""UPDATE books SET Title = ?, Author = ?, Qty = ? WHERE id = ?""", (book_info[1], book_info[2], book_info[3], book_info[0], ))
        self._db.commit()
            
    
    def close(self) -> None:
        self._db.close()

def print_books(books:List[Book], header:List[str]):
    list_info = [i.get_info() for i in books]
    print(tabulate(list_info, headers=header))

def new_book():
    new_title = input("Title:  ")
    new_author = input("Author:  ")
    try:
        new_qty = int(input("Quantity:  "))
    except ValueError:
        new_qty = 0
        print("Incorrect entry. Quantity puts equal 0")
    new_book = [Book(title=new_title, author=new_author, qty=new_qty)]
    return new_book

def serch_by():
    menu = input("""
    Do you want to search by
    1 - id
    2 - Title or/and author
    OR any key to Exit
    : """)
    if menu == '1':
        id_serch = input("Enter id: ")
        return (book_db.search(id= int(id_serch)))
    elif menu == '2':
        title_serch = input("Enter title: ")
        author_serch = input("Enter author: ")
        return (book_db.search(title=title_serch, author=author_serch))
    else:
        return None

def change_parameters(book_info):
    changing = input("""
    Enter with ":" beetween parameters you want to change:
    title:author:qty
    :    """)
    list_of_changes = changing.split(':')
    b_id = book_info[0]
    if list_of_changes[0] == '':
        b_title = book_info[1]
    else:
        b_title = list_of_changes[0]
    if list_of_changes[1] == '':
        b_author = book_info[2]
    else:
        b_author = list_of_changes[1]
    if list_of_changes[2] == '':
        b_qty = book_info[3]
    else:
        b_qty = list_of_changes[2]
    
    book_updated = Book(id=b_id, title=b_title, author=b_author, qty=b_qty)
    return book_updated

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
    # Add new book
        n_book = new_book()
        book_db.add_book(n_book)
        print_books(n_book, book_db.header)
        
    elif main_menu == "2":
    # Search book by id, or title and/or author
        book_list = serch_by()
        if book_list is not None:
            print_books(book_list, book_db.header)
            menu_into_serch = input("""
        Do you want:
        1-update these books
        2-delete these books
        any key to exit
        : """)
            if menu_into_serch == '1':
                up_book_list = []
                for book in book_list:
                    book_info = book.get_info()
                    up_book = change_parameters(book_info)
                    up_book_list.append(up_book)
                
                print_books(up_book_list, book_db.header)
                book_db.change(up_book_list)
                print("Books have been updated")

            elif menu_into_serch == '2':
                confirmation = input("""Delete confirmation. Press "y" to delete : """)
                if confirmation == "y":
                    book_db.delete(book_list)
                    print("Books have been deleted")
            else:
                print("Exit")
        else:
            print("Search has been interrupted")

    elif main_menu == "3":
    # View all
        book_list = book_db.search()
        print_books(book_list, book_db.header)

    elif main_menu == "0":
    # Exit
        break

    else:
        print("Wrong enter. Try again please.")

print("Thank you for using BOOK Database")

book_db.close()