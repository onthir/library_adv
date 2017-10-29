
from tkinter import *
import sqlite3
import time
import datetime
import random
from tkinter import messagebox



class Application(Text):
    """docstring for ClassName"""
    def __init__(self, master):
        Text.__init__(self, master)


        #heading for the main window
        self.heading = Label(master, text="Welcome to Library Prototype", font=('arial 40 bold'))
        self.heading.place(x=0, y=0)

        #labels for name date author genre position
        self.name = Label(master, text="Name of the Book: ")
        self.author = Label(master, text="Author of the book: ")
        self.genre = Label(master, text="Genre of the book: ")
        self.position = Label(master, text="Position of the book: ")

        self.name.place(x=0, y=60)
        self.author.place(x=0, y=100)
        self.genre.place(x=0, y=140)
        self.position.place(x=0, y=180)

        #entries for labels
        self.book = StringVar()
        self.name_ent = Entry(master, width=30, textvariable=self.book).place(x=150 , y=60)
        self.writer = StringVar()
        self.author_ent = Entry(master, width=30, textvariable=self.writer).place(x=150 , y=100)
        self.tags = StringVar()
        self.genre_ent = Entry(master, width=30, textvariable=self.tags).place(x=150 , y=140)
        self.placed = StringVar()
        self.position_ent = Entry(master, width=30, textvariable=self.placed).place(x=150 , y=180)

        #button to perform
        self.submit = Button(master, text="Add To Database",command=self.dynamic_data_entry, width=20, height=2).place(
            x=150, y=220)
        self.search = Button(master, text="Search Books", width=20, height=2, command=self.search_root).place(x=150, y=300)

        #textbox to display updates
        self.box = Text(master, height=15, width=60)
        self.box.focus_set()
        self.box.place(x=400, y=60)
    #Now adding the user input to database. 
    global conn
    global c   
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    def dynamic_data_entry(self):
        #creating the database if it doesnot exist
        c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(datestamp TEXT, name TEXT, author TEXT, genre TEXT, position TEXT)")
    

        #adding fields and values to the databse
        unix = time.time()
        datestamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        name = self.book.get()
        author = self.writer.get()
        genre = self.tags.get()
        position = self.placed.get()
        if len(name) == 0 or len(author) == 0 or len(genre) == 0 or len(position) == 0:
            print("Failed. Please Fill up all the information")
            messagebox.showwarning("Failed", "Please don't leave anything blank.")


        else:
            c.execute("INSERT INTO stuffToPlot (datestamp, name, author, genre, position) VALUES (?, ?,?, ?, ?)",(datestamp, name, author, genre, position))
            conn.commit()
            self.box.insert(END, ('Logs: Added ' +name.upper() + " by " + author+ "\n" ))
            messagebox.showinfo("Success", "Successfully added to the database")

    #search funtionality feature.
    def search_root(self):
        class Search(Text):
            def __init__(self, faster):
                Text.__init__(self, faster)

                #labels for window
                self.heading = Label(faster, text="Search Books Here.", font=('arial 25 bold'))
                self.heading.place(x=0, y=0)
                
                self.name = Label(faster, text="Name of the Book: ")
                self.name.place(x=0, y=60)

                #self.entrybox

                self.ent = Entry(faster, width=30)
                self.ent.place(x=150, y=60)

                self.sbox = Text(faster, height=15, width=60, bg="lightgreen")
                self.sbox.place(x=50, y=130)
                self.sbox.focus_set()



                #button to perform search
                self.bt = Button(faster,text="Search",command=self.get_it ,width=20, height=2)
                self.bt.place(x=390, y=50)


            def get_it(self):
                conn = sqlite3.connect('books.db')
                c = conn.cursor()                
                c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(datestamp TEXT, name TEXT, author TEXT, genre TEXT, position TEXT)")
                c.execute("SELECT * FROM stuffToPlot WHERE name LIKE ?", (self.ent.get(),))
                #data = c.fetchall()
                #print(data)
                for row in c.fetchall():
                    self.sbox.insert(END, (row[0] +" "+ row[1]) +" " + row[4]+ "\n")



                #dynamic_data_entry()

                c.close
                conn.close()





        window = Tk()
        window.geometry('900x400')
        window.resizable(False, False)
        c = Search(window)
        window.mainloop()

root = Tk()
root.geometry('900x400')
root.resizable(False, False)

b = Application(root)
root.mainloop()
