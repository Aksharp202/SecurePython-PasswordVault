# Libraries
from tkinter import *
from functools import partial
from tkinter import simpledialog
import sqlite3
import hashlib

# Database
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

# Window Settings
window = Tk()
window.title("Password Vault")

# Pop - Ups


def pop_up(text):
    answer = simpledialog.askstring("input string", text)

    return answer

# Functions


def hash_passwords(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash


def first_screen():
    window.geometry('250x150')

    lbl = Label(window, text="Create Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text="Re-Enter Master Password")
    lbl1.config(anchor=CENTER)
    lbl1.pack()

    txt1 = Entry(window, width=20, show="*")
    txt1.pack()

    lbl2 = Label(window)
    lbl2.pack()

    def save_password():
        if txt.get() == txt1.get():
            hashedpassword = hash_passwords(txt.get().encode('utf-8'))

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashedpassword)])
            db.commit()

            password_vault()
        else:
            lbl2.config(text="Passwords Do Not Match")
            txt.delete(0, 'end')
            txt1.delete(0, 'end')

    btn = Button(window, text="Save", command=save_password)
    btn.pack(pady=10)


def login_screen():
    window.geometry('250x100')

    lbl = Label(window, text="Enter Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.pack()

    def get_masterpassword():
        checkhashedpassword = hash_passwords(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkhashedpassword)])
        return cursor.fetchall()

    def check_password():
        match = get_masterpassword()

        if match:
            password_vault()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Password")

    btn = Button(window, text="Submit", command=check_password)
    btn.pack(pady=10)


def password_vault():
    for widget in window.winfo_children():
        widget.destroy()

    def add_entry():
        txt1 = "Website"
        txt2 = "Username"
        txt3 = "Password"

        website = pop_up(txt1)
        username = pop_up(txt2)
        password = pop_up(txt3)

        insert_fields = """INSERT INTO vault(website, username, password)
        VALUES(?, ?, ?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        password_vault()

    def remove_entry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input, ))
        db.commit()

        password_vault()

    window.geometry('700x350')

    lbl = Label(window, text="Password Vault")
    lbl.config(anchor=CENTER)
    lbl.grid(column=1)

    btn = Button(window, text="+", command=add_entry)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if(cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl1.grid(column=1, row=i+3)
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl1.grid(column=2, row=i+3)

            btn = Button(window, text="Delete", command=partial(remove_entry, array[i][0]))
            btn.grid(column=3, row=i+3, pady=10)

            i = i+1

            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall()) <= i):
                break


# Running the App
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    login_screen()
else:
    first_screen()
window.mainloop()
