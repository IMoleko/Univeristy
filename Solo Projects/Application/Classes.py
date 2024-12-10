from Database import *  # Assuming the improved DatabaseManager is in `database.py`

class Shelf:
    def __init__(self, width, height, shelf_id=None):
        """
        Represents a shelf with dimensions and an optional ID for database tracking.
        """
        self.id = shelf_id
        self.width = width
        self.height = height
        self.books = []

    def add_book(self, book):
        """
        Attempt to add a book to the shelf if it fits.
        Returns True if successful, otherwise False.
        """
        if self.can_fit_book(book):
            self.books.append(book)
            book.shelf_id = self.id
            return True
        return False

    def can_fit_book(self, book):
        """
        Check if the book's dimensions fit within the shelf's dimensions.
        """
        total_width = sum(b.width for b in self.books) + book.width
        return total_width <= self.width and book.height <= self.height

    def save(self, db_manager):
        """
        Save the shelf to the database.
        """
        if self.id is None:
            db_manager.execute_query(
                "INSERT INTO shelves (width, height) VALUES (?, ?)",
                (self.width, self.height)
            )
            self.id = db_manager.cursor.lastrowid


class Book:
    def __init__(self, title, author, width, height, volume, orientation, shelf_id=None, book_id=None):
        """
        Represents a book with dimensions, metadata, and optional database tracking IDs.
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.width = width
        self.height = height
        self.volume = volume
        self.orientation = orientation
        self.shelf_id = shelf_id

    def save(self, db_manager):
        """
        Save the book to the database.
        """
        if self.id is None:
            db_manager.execute_query(
                '''
                INSERT INTO books (title, author, width, height, volume, orientation, shelf_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (self.title, self.author, self.width, self.height, self.volume, self.orientation, self.shelf_id)
            )
            self.id = db_manager.cursor.lastrowid


class BookshelfManager:
    def __init__(self):
        """
        Manager to handle shelves and books, and interact with the database.
        """
        self.shelves = []
        self.db_manager = DatabaseManager()  # Initialize database manager

    def load_shelves(self):
        """
        Load shelves from the database and populate with books.
        """
        shelves_data = self.db_manager.fetch_all("SELECT * FROM shelves")
        for shelf_data in shelves_data:
            shelf = Shelf(shelf_data[1], shelf_data[2], shelf_data[0])
            self.shelves.append(shelf)
            self.load_books(shelf)

    def load_books(self, shelf):
        """
        Load books for a specific shelf from the database.
        """
        books_data = self.db_manager.fetch_all("SELECT * FROM books WHERE shelf_id = ?", (shelf.id,))
        for book_data in books_data:
            book = Book(
                book_data[1], book_data[2], book_data[3], book_data[4],
                book_data[5], book_data[6], book_data[7], book_data[0]
            )
            shelf.books.append(book)

    def add_shelf(self, width, height):
        """
        Add a new shelf to the system and save it to the database.
        """
        shelf = Shelf(width, height)
        shelf.save(self.db_manager)
        self.shelves.append(shelf)
        return shelf

    def add_book_to_shelf(self, shelf_id, title, author, width, height, volume, orientation):
        """
        Add a book to a specific shelf, save it to the database if it fits.
        """
        shelf = next((s for s in self.shelves if s.id == shelf_id), None)
        if shelf:
            book = Book(title, author, width, height, volume, orientation)
            if shelf.add_book(book):
                book.save(self.db_manager)
                return book
            else:
                print("Book does not fit on the shelf.")
        else:
            print("Shelf not found.")
        return None
