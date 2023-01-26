import sqlite3
from tabulate import tabulate
from typing import List, Tuple, Any

class Book():
    """
    Class presenting a book for database with id, title, author and qty Value
    """
    def __init__(self, title:str, author:str, qty:int, id:int = None) -> None:
        self._id = id
        self._title = title
        self._author = author
        self._qty = qty
    
    @property
    def id(self):
        """
        Retern id
        """
        return self._id
    
    def get_db_info(self) -> List[Any]:
        """
        Return instance as a list of parameters
        """
        if self._id is not None:
            return [self._id, self._title, self._author, self._qty]
        else:
            return [self._title, self._author, self._qty]

class BookDatabase():
    """
    Class database 
    Create Database 'ebookstore' and Table 'books' in it
    Create 'cursor'
    """"
    def __init__(self, db_file_name:str) -> None:
        self._db_file_name = db_file_name
        self._db = sqlite3.connect('ebookstore')
        self._cursor = self._db.cursor()
        self._cursor.execute('''
CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Author TEXT NUT NULL, Qty INT DEFAULT 0)''')
        self._db.commit()
    
    def is_empty(self) -> bool:
        """
        Method for check if Table is empty
        """
        self._cursor.execute("""SELECT * FROM books""")
        row = self._cursor.fetchone()
        return row is None
    
    @property
    def header(self) -> List[str]:
        self._cursor.execute('PRAGMA table_info("books")')
        column_names = [i[1] for i in self._cursor.fetchall()]
        return column_names
    
    def add_book(self, books:List[Book]) -> None:
        """
        Method for adding new book to the table books
        doesn't matter if we know the id or don't know
        parameter - List of elements class Book
        """
        for book in books:
            book_info = book.get_db_info()
            if book.id is None:
                self._cursor.execute('''INSERT INTO books (Title, Author, Qty) VALUES(?,?,?)''', book_info)
            else:
                self._cursor.execute('''INSERT INTO books (id, Title, Author, Qty) VALUES(?,?,?,?)''', book_info)
        self._db.commit()

    def search(self, title:str=None, author:str=None, qty:int=None, id:int = None) -> List[Book]:
        """
        Metod for Select rows from table detend on different search terms
        parameters - title, author, qty, id
        Returns: List of elements class Book
        """
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
    
    def search_qty(self, num1, num2) -> List[Book]:
        """
        Method for Select rows from table books selected by qty parameter
        Returns: List of elements class Book
        """
        list_book = []
        if num2 == 0 and num1 !=0 :
            rows = self._cursor.execute("""SELECT * FROM books WHERE Qty >= ?""", (num1,))
        else:
            rows = self._cursor.execute("""SELECT * FROM books WHERE Qty BETWEEN ? AND ?""", (num1, num2))
        
        for row in rows:
            list_book.append(Book(id=row[0], title=row[1], author=row[2], qty=row[3]))
        return list_book

    def delete(self, books:List[Book]) -> None:
        """
        Method to Delete rows from the table books
        Nothing to retern
        """
        for book in books:
            book_info = book.get_db_info()
            self._cursor.execute("""DELETE FROM books WHERE id = ?""", (book_info[0], ))
        self._db.commit()

    def update(self, books:List[Book]) -> None:
        """
        Method to Update row in the table books
        Nothing to retern
        """
        for book in books:
            book_info = book.get_db_info()
            self._cursor.execute("""UPDATE books SET Title = ?, Author = ?, Qty = ? WHERE id = ?""", (book_info[1], book_info[2], book_info[3], book_info[0], ))
        self._db.commit()

    def close(self) -> None:
        self._db.close()

def print_books(books:List[Book], header:List[str]):
    """
    Function to print out rows from books as a table
    """
    list_info = [i.get_db_info() for i in books]
    print(tabulate(list_info, headers=header))

def new_book():
    """
    Request data about new book
    Returns: new object class Book
    """
    new_title = input("Title:  ")
    new_author = input("Author:  ")
    try:
        new_qty = int(input("Quantity:  "))
    except ValueError:
        new_qty = 0
        print("Incorrect entry. Quantity set to 0")
    new_book = [Book(title=new_title, author=new_author, qty=new_qty)]
    return new_book

def search_by():
    """
    This Function use to Select rows from database by using id or title/author or qty as a parameter to search
    """
    # TODO: function can return a dictionary like {"id": <id from input>, "title": <title from input>, ...} 
    # and book.db.search() would be called outside search_by()
    menu = input("""
    Do you want to search by
    1 - id
    2 - Title or/and author
    3 - quantity
    OR any key to Exit
    : """)
    if menu == '1':
        id_search = input("Enter id: ")
        return (book_db.search(id= int(id_search)))
    elif menu == '2':
        title_search = input("Enter title: ")
        author_search = input("Enter author: ")
        return book_db.search(title=title_search, author=author_search)
    elif menu == '3':
        print(""" Quantity search
    Enter TWO numbers to find all books in the range
    If numbers are equal program will return books with this current quantity
    if the second is 0 program will return books with more than first number quantity
    if the first number is 0 program will return books with less than second number quantity
    """)
        try:
            num1 = int(input("First number:  "))
            num2 = int(input("Second number: "))
            return book_db.search_qty(num1, num2)
        except ValueError:
            print("Wrong enter")
    else:
        return None

def change_parameters(book_info):
    """
    Change parameter of elemets class Book
    Args:
        book_info (List): List of book parameners[id, title, author, qty]

    Returns:
        element class Book: with the same id, but changed title or/and author or/and qty
    """
    #TODO: You can return a dictionary from here and update Book instance outside change_parameters() 
    # so that you're not mixing two different things. Rather than creating a new instance of Book, you'd 
    # better add add more properties for title, author etc (the same way you have for id) in Book class 
    # via @property and assign these outside of change_parameters()
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
        book_list = search_by()
        if book_list is not None:
            print_books(book_list, book_db.header)
            menu_into_search = input("""
        Do you want:
        1-update these books
        2-delete these books
        any key to exit
        : """)
            if menu_into_search == '1':
                up_book_list = []
                for book in book_list:
                    book_info = book.get_db_info()
                    up_book = change_parameters(book_info)
                    up_book_list.append(up_book)
                
                print_books(up_book_list, book_db.header)
                book_db.update(up_book_list)
                print("Books have been updated")

            elif menu_into_search == '2':
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