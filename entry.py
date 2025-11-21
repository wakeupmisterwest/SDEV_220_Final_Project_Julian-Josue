from tkinter import *

root = Tk()
root.title("Entry Widget - Intro To Tkinter")
root.iconbitmap('images/1d178f37c8208ad2c497833fafb17e41.ico')
root.geometry('500x300')

def insert():
    # Insert "John" into the entry box
    my_entry.insert(0, "John")

def answer():
    # Delete Hidden Label
    hidden_label.config(text="")
    # Logic to make sure they typed in a name
    my_variable = my_entry.get()
    if my_entry.get():
        # Output to hidden label
        hidden_label.config(text=f'Hello {my_entry.get()}')
        # Delete The Entry Box
        my_entry.delete(0, END)
    else:
        hidden_label.config(text="Hey! You Forgot To Enter Your Name!")

# Create a Label
my_label = Label(root, text="Enter Your Name", font=("Helvetica", 24))
my_label.pack(pady=20)

# Create an Entry Box
my_entry = Entry(root, width=20, font=("Helvetica", 24))
my_entry.pack(pady=20)

# Create a Button
my_button = Button(root, text="Answer", command=answer)
my_button.pack(pady=20)

insert_button = Button(root, text="Insert John", command=insert)
insert_button.pack(pady=20)

# Create a hidden label
hidden_label = Label(root, text="", font=("Helvetica", 18))
hidden_label.pack(pady=20)



root.mainloop()

