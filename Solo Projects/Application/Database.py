import sqlite3

class DatabaseManager:
    def __init__(self, db_name="bookshelf.db"):
        """Initialize the database connection and set up tables."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create the necessary tables for the application."""
        try:
            # Create the shelves table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS shelves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL
                )
            ''')

            # Create the books table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT,
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL,
                    volume INTEGER,
                    orientation TEXT,
                    shelf_id INTEGER,
                    FOREIGN KEY (shelf_id) REFERENCES shelves (id) ON DELETE CASCADE
                )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def execute_query(self, query, params=None):
        """Execute a query with optional parameters."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()

# Usage example (uncomment to test)
if __name__ == "__main__":
    db = DatabaseManager()

    # Example: Add a shelf
    db.execute_query("INSERT INTO shelves (width, height) VALUES (?, ?)", (100, 200))

    # Example: Retrieve all shelves
    shelves = db.fetch_all("SELECT * FROM shelves")
    print("Shelves:", shelves)

    # Close the database connection
    db.close_connection()
