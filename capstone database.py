import sqlite3

# Connect to the database 
db = sqlite3.connect("ebookstore.db")
cursor = db.cursor()

# Create a table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS book (
                    id INTEGER PRIMARY KEY,
                    Title VARCHAR(15),
                    Author VARCHAR(20),
                    Qty INTEGER
                )""")

data = [
    (3001, 'A tale of two cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the philosophers', 'J.K Rowling', 40),
    (3003, 'The lion, the witch and the Wardrobe', 'C.S Lewis', 25),
    (3004, 'Lord of the rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in wonderland', 'Lewis Carroll', 12)
]

# Insert data into the table
cursor.executemany("INSERT OR IGNORE INTO book (id, Title, Author, Qty) VALUES (?, ?, ?, ?)", data)
db.commit()

# Print a success message
print("Data inserted successfully into the 'book' table.")

def enter_book():
    # Get user input for book details
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    qty = int(input("Enter the quantity: "))

    # Insert the book into the database
    cursor.execute("INSERT INTO book (Title, Author, Qty) VALUES (?, ?, ?)", (title, author, qty))
    db.commit()
    print(f"{title} by {author} with quantity {qty} has been added to the database.")

def update_book():
    # Get user input for book ID and new quantity
    book_id = int(input("Enter the book ID to update: "))
    new_qty = int(input("Enter the new quantity: "))

    # Update the quantity for the specified book ID
    cursor.execute("UPDATE book SET Qty = ? WHERE id = ?", (new_qty, book_id))
    db.commit()
    print(f"Quantity for book ID {book_id} has been updated to {new_qty}.")

def delete_book():
    # Get user input for book ID to delete
    book_id = int(input("Enter the book ID to delete: "))

    # Delete the book with the specified ID
    cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
    db.commit()
    print(f"Book with ID {book_id} has been deleted from the database.")

def search_books():
    # Get user input for search keyword
    keyword = input("Enter a keyword to search for books: ")

    # Search for books containing the keyword in title or author
    cursor.execute("SELECT * FROM book WHERE Title LIKE ? OR Author LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
    results = cursor.fetchall()

    if results:
        print("Search results:")
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Qty: {row[3]}")
    else:
        print("No books found matching the search criteria.")

# Main menu loop
while True:
    print("\n*****OPTIONS*****")
    print("1 = Enter book")
    print("2 = Update book")
    print("3 = Delete book")
    print("4 = Search books")
    print("0 = Exit")

    user_input = input("Please enter your option: ")

    if user_input == "1":
        enter_book()
    elif user_input == "2":
        update_book()
    elif user_input == "3":
        delete_book()
    elif user_input == "4":
        search_books()
    elif user_input == "0":
        break
    else:
        print("Invalid option. Please try again.")
