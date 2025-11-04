import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# ---------------- Database Connection ----------------
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aayush@#72",  # change as needed
    database="Library"
)
cursor = con.cursor()

# ---------------- Core Functions ----------------
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if title and author and genre and price and quantity:
        cursor.execute("INSERT INTO books (title, author, genre, price, quantity) VALUES (%s,%s,%s,%s,%s)",
                       (title, author, genre, price, quantity))
        con.commit()
        messagebox.showinfo("Success", "✅ Book added successfully!")
        clear_entries()
        view_books()
    else:
        messagebox.showwarning("Warning", "⚠ Please fill all fields!")

def update_book():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "⚠ Select a book to update!")
        return
    data = tree.item(selected)["values"]
    book_id = data[0]

    title = title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    cursor.execute("UPDATE books SET title=%s, author=%s, genre=%s, price=%s, quantity=%s WHERE book_id=%s",
                   (title, author, genre, price, quantity, book_id))
    con.commit()
    messagebox.showinfo("Updated", "📘 Book updated successfully!")
    clear_entries()
    view_books()

def delete_book():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "⚠ Select a book to delete!")
        return
    data = tree.item(selected)["values"]
    book_id = data[0]
    confirm = messagebox.askyesno("Confirm", "🗑 Delete this book?")
    if confirm:
        cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
        con.commit()
        messagebox.showinfo("Deleted", "🗑 Book deleted successfully!")
        view_books()

def search_book():
    search_term = search_entry.get()
    if not search_term:
        messagebox.showwarning("Warning", "🔍 Enter book title or author to search!")
        return

    query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
    results = cursor.fetchall()

    for row in tree.get_children():
        tree.delete(row)
    for row in results:
        tree.insert("", tk.END, values=row)

def clear_entries():
    for entry in [title_entry, author_entry, genre_entry, price_entry, quantity_entry]:
        entry.delete(0, tk.END)

def view_books():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# ---------------- Bill PDF Generator ----------------
def generate_bill():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "⚠ Please select a book to issue bill!")
        return

    data = tree.item(selected)["values"]
    book_id, title, author, genre, price, qty = data

    now = datetime.now()
    filename = f"Bill_{title}{now.strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = canvas.Canvas(filename, pagesize=letter)
    pdf.setTitle("Library Bill")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(200, 750, "LIBRARY BILL RECEIPT")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 700, f"Book ID: {book_id}")
    pdf.drawString(50, 680, f"Title: {title}")
    pdf.drawString(50, 660, f"Author: {author}")
    pdf.drawString(50, 640, f"Genre: {genre}")
    pdf.drawString(50, 620, f"Price: ₹{price}")
    pdf.drawString(50, 600, f"Quantity: {qty}")
    pdf.drawString(50, 580, f"Date: {now.strftime('%d-%m-%Y %H:%M:%S')}")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 550, f"Total Amount: ₹{float(price) * int(qty)}")
    pdf.line(50, 540, 550, 540)

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(50, 520, "Thank you for using Library Management System!")
    pdf.drawString(50, 505, "Developed by Sachin & Ayush | Guided by Sweta Ma’am")

    pdf.save()
    messagebox.showinfo("Bill Generated", f"🧾 Bill saved as '{filename}'")

# ---------------- GUI Design ----------------
root = tk.Tk()
root.title("📚 Library Management System - Mini Project")
root.geometry("900x620")
root.config(bg="#f2f2f2")

title_label = tk.Label(root, text="LIBRARY MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), bg="#004c99", fg="white", pady=10)
title_label.pack(fill="x")

# Input Frame
frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

labels = ["Title", "Author", "Genre", "Price", "Quantity"]
entries = []
for i, text in enumerate(labels):
    tk.Label(frame, text=text + ":", font=("Arial", 11, "bold"), bg="#f2f2f2").grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = tk.Entry(frame, width=35)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

title_entry, author_entry, genre_entry, price_entry, quantity_entry = entries

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="➕ Add", width=10, bg="#4CAF50", fg="white", command=add_book).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="🔄 Update", width=10, bg="#2196F3", fg="white", command=update_book).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="❌ Delete", width=10, bg="#f44336", fg="white", command=delete_book).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="🧾 Bill", width=10, bg="#9C27B0", fg="white", command=generate_bill).grid(row=0, column=3, padx=5)

tk.Label(btn_frame, text="Search:", bg="#f2f2f2", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10)
search_entry = tk.Entry(btn_frame, width=20)
search_entry.grid(row=0, column=5, padx=5)
tk.Button(btn_frame, text="🔍 Go", width=8, bg="#FF9800", fg="white", command=search_book).grid(row=0, column=6, padx=5)

# Table Frame
columns = ("ID", "Title", "Author", "Genre", "Price", "Quantity")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)
tree.pack(pady=10, fill="both", expand=True)
view_books()

# Footer
footer = tk.Label(root, text="Developed by Sachin & Aayush | Mini Project | Guided by Sweta Ma’am ",
                  bg="#004c99", fg="white", font=("Arial", 10, "bold"), pady=5)
footer.pack(fill="x", side="bottom")

root.mainloop()
