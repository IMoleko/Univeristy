import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Classes import *

class BookshelfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookshelf Application")

        # Initialize manager
        self.manager = BookshelfManager()
        self.manager.load_shelves()

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_tabs()

    def create_tabs(self):
        """Initialize application tabs."""
        self.create_input_tab()
        self.create_data_tab()
        self.create_visualization_tab()

    def create_input_tab(self):
        input_tab = ttk.Frame(self.notebook)
        self.notebook.add(input_tab, text="Input Data")
        BookshelfInputWindow(input_tab, self.manager)

    def create_data_tab(self):
        data_tab = ttk.Frame(self.notebook)
        self.notebook.add(data_tab, text="Raw Data")
        BookshelfDataView(data_tab, self.manager)

    def create_visualization_tab(self):
        visualization_tab = ttk.Frame(self.notebook)
        self.notebook.add(visualization_tab, text="Visualization")
        BookshelfVisualizer(visualization_tab, self.manager)

class BookshelfInputWindow:
    def __init__(self, parent, manager):
        self.manager = manager

        # Frames for inputs
        self.create_frames(parent)

        # Shelf inputs
        self.create_shelf_inputs()

        # Book inputs
        self.create_book_inputs()

    def create_frames(self, parent):
        self.shelf_frame = ttk.LabelFrame(parent, text="Add Shelf", padding=10)
        self.shelf_frame.pack(fill=tk.X, padx=10, pady=10)

        self.book_frame = ttk.LabelFrame(parent, text="Add Book", padding=10)
        self.book_frame.pack(fill=tk.X, padx=10, pady=10)

    def create_shelf_inputs(self):
        ttk.Label(self.shelf_frame, text="Width:").grid(row=0, column=0, sticky="e", padx=5)
        self.shelf_width = ttk.Entry(self.shelf_frame)
        self.shelf_width.grid(row=0, column=1)

        ttk.Label(self.shelf_frame, text="Height:").grid(row=1, column=0, sticky="e", padx=5)
        self.shelf_height = ttk.Entry(self.shelf_frame)
        self.shelf_height.grid(row=1, column=1)

        ttk.Button(self.shelf_frame, text="Add Shelf", command=self.add_shelf).grid(row=2, columnspan=2, pady=10)

    def create_book_inputs(self):
        inputs = [
            ("Title:", "book_title"),
            ("Author:", "book_author"),
            ("Width:", "book_width"),
            ("Height:", "book_height"),
            ("Volume:", "book_volume"),
            ("Orientation:", "book_orientation"),
            ("Shelf ID:", "book_shelf_id"),
        ]

        for i, (label, var_name) in enumerate(inputs):
            ttk.Label(self.book_frame, text=label).grid(row=i, column=0, sticky="e", padx=5)
            setattr(self, var_name, ttk.Entry(self.book_frame))
            getattr(self, var_name).grid(row=i, column=1)

        ttk.Button(self.book_frame, text="Add Book", command=self.add_book).grid(row=len(inputs), columnspan=2, pady=10)

    def add_shelf(self):
        try:
            width = int(self.shelf_width.get())
            height = int(self.shelf_height.get())
            shelf = self.manager.add_shelf(width, height)
            messagebox.showinfo("Success", f"Shelf {shelf.id} added!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dimensions for the shelf.")

    def add_book(self):
        try:
            title = self.book_title.get()
            author = self.book_author.get()
            width = int(self.book_width.get())
            height = int(self.book_height.get())
            volume = int(self.book_volume.get())
            orientation = self.book_orientation.get()
            shelf_id = int(self.book_shelf_id.get())

            book = self.manager.add_book_to_shelf(shelf_id, title, author, width, height, volume, orientation)
            messagebox.showinfo("Success", f"Book '{book.title}' added!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid book details.")

class BookshelfDataView:
    def __init__(self, parent, manager):
        """
        View for displaying raw data from the shelves and books with search and filtering.
        """
        self.manager = manager

        # Frame for search and data view
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Search entry and button
        self.search_label = ttk.Label(self.frame, text="Search:")
        self.search_label.pack(side=tk.TOP, padx=10)

        self.search_entry = ttk.Entry(self.frame)
        self.search_entry.pack(side=tk.TOP, padx=5, fill=tk.X, expand=True)

        self.search_button = ttk.Button(self.frame, text="Filter", command=self.apply_filter)
        self.search_button.pack(side=tk.TOP, padx=10)

        # Treeview to display shelves and books
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Type", "ID", "Shelf/Book Title", "Width", "Height", "Additional Info"),
            show="headings",
        )
        self.tree.heading("Type", text="Type")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Shelf/Book Title", text="Shelf/Book Title")
        self.tree.heading("Width", text="Width")
        self.tree.heading("Height", text="Height")
        self.tree.heading("Additional Info", text="Additional Info (Volume/Author)")

        # Adjust column widths
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Shelf/Book Title", width=200, anchor="w")
        self.tree.column("Width", width=100, anchor="center")
        self.tree.column("Height", width=100, anchor="center")
        self.tree.column("Additional Info", width=150, anchor="w")

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Populate data
        self.load_data()

    def load_data(self, filter_text=None):
        """
        Load data from the manager into the treeview with an optional filter.
        """
        # Clear the treeview before reloading
        self.tree.delete(*self.tree.get_children())

        # Populate shelves and books
        for shelf in self.manager.shelves:
            # If there is a filter, only include shelves that match the filter
            if filter_text and filter_text.lower() not in str(shelf.id).lower() and filter_text.lower() not in str(shelf.width).lower() and filter_text.lower() not in str(shelf.height).lower():
                continue

            # Add shelf information
            self.tree.insert(
                "",
                "end",
                values=(
                    "Shelf",
                    shelf.id,
                    f"Shelf {shelf.id}",
                    shelf.width,
                    shelf.height,
                    "N/A",
                ),
                tags=("shelf",),  # Optional: Add tags for styling
            )

            # Add books belonging to this shelf
            for book in shelf.books:
                # If there is a filter, only include books that match the filter
                if filter_text and filter_text.lower() not in book.title.lower() and filter_text.lower() not in book.author.lower():
                    continue

                # Add book information
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        "Book",
                        book.id,
                        book.title,
                        book.width,
                        book.height,
                        f"{book.author} (Vol: {book.volume})",
                    ),
                    tags=("book",),  # Optional: Add tags for styling
                )

    def apply_filter(self):
        """
        Apply the filter based on the search input and reload the data.
        """
        filter_text = self.search_entry.get()
        self.load_data(filter_text=filter_text)

class BookshelfVisualizer:
    def __init__(self, parent, manager):
        self.manager = manager
        self.canvas = tk.Canvas(parent, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_bookshelf())

    def draw_bookshelf(self):
        self.canvas.delete("all")

        # Constants for drawing
        margin = 20
        scale = 5  # Scale dimensions for better visualization
        y_offset = margin

        canvas_width = self.canvas.winfo_width()
        for shelf in self.manager.shelves:
            shelf_width = shelf.width * scale
            x_margin = (canvas_width - shelf_width) / 2

            # Draw shelf
            self.canvas.create_rectangle(x_margin, y_offset, x_margin + shelf_width, y_offset + 20, fill="brown")
            self.canvas.create_text(x_margin - 10, y_offset + 10, text=f"Shelf {shelf.id}", anchor="e")

            # Draw books
            x_offset = x_margin
            for book in shelf.books:
                book_width = book.width * scale
                book_height = book.height * scale
                self.canvas.create_rectangle(
                    x_offset, y_offset - book_height, x_offset + book_width, y_offset,
                    fill="skyblue"
                )
                self.canvas.create_text(
                    x_offset + book_width / 2, y_offset - book_height / 2,
                    text=book.title[:10], anchor="center"
                )
                x_offset += book_width

            y_offset += 30  # Move down for next shelf

if __name__ == "__main__":
    root = tk.Tk()
    app = BookshelfApp(root)
    root.mainloop()
