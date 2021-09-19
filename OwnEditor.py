from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
import os, sys
import win32print
import win32api

root = Tk()
root.title("My Own Text Editor")
root.iconbitmap('C:/Users/hp/Downloads/icnew.ico')
root.geometry('1200x710')


global open_status_name
open_status_name = False
global selected
selected = False


# Create a new file function
def new_file():
    my_text.delete("1.0", END)
    root.title('New File - TextPad')
    status_bar.config(text="New File      ")

    global open_status_name
    open_status_name = False


# Create Open files
def open_file():
    my_text.delete("1.0", END)

    # Now we have to grab filename
    text_file = filedialog.askopenfilename(initialdir="C:/Users/hp", title="Open File",
                                           filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                      ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        global open_status_name
        open_status_name = text_file

    name = text_file
    status_bar.config(text=f'{name}     ')
    name = name.replace("C:/Users/hp/", "")
    root.title(f'{name} - TextPad')

    # Now we open the file
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    my_text.insert(END, stuff)
    text_file.close()


def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Users/hp", title="Save File",
                                             filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                        ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        status_bar.config(text=f'Saved: {name}     ')
        name = name.replace("C:/Users/hp/", "")
        root.title(f'{name} - TextPad')

        # Now we save the file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()


def save_file():
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()
        status_bar.config(text=f'Saved: {open_status_name}     ')

    else:
        save_as_file()


# Cut Text
def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)


# Copy Text
def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


# Paste Text
def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()

    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


def bold_it():
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    # Now we configure a tag
    my_text.tag_configure("bold", font=bold_font)

    current_tags = my_text.tag_names("sel.first")
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")


def italics_it():
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")

    # Now we configure a tag
    my_text.tag_configure("italic", font=italics_font)

    current_tags = my_text.tag_names("sel.first")
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")


# Change Selected text color
def text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:

        color_font = font.Font(my_text, my_text.cget("font"))

        # Now we configure a tag
        my_text.tag_configure("colored", font=color_font, foreground=my_color)

        current_tags = my_text.tag_names("sel.first")
        if "colored" in current_tags:
            my_text.tag_remove("colored", "sel.first", "sel.last")
        else:
            my_text.tag_add("colored", "sel.first", "sel.last")


# Change background color
def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)


def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)


def print_file():
    file_to_print = filedialog.askopenfilename(initialdir="C:/Users/hp", title="Open File",
                                               filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                          ("Python Files", "*.py"), ("All Files", "*.*")))
    if file_to_print:
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)


def select_all(e):
    my_text.tag_add('sel', '1.0', 'end')


def clear_all():
    my_text.delete(1.0, END)


# Here we turn on Night mode
def night_on():
    main_color = "#000000"
    second_color = "grey"
    text_color = "green"
    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg="black", insertbackground="white", fg=text_color)
    toolbar_frame.config(bg=main_color)

    # toolbar buttons
    bold_button.config(bg=second_color)
    italics_button.config(bg=second_color)
    redo_button.config(bg=second_color)
    undo_button.config(bg=second_color)
    color_text_button.config(bg=second_color)

    # File menu colors
    file_menu.config(bg=main_color, fg=text_color)
    edit_menu.config(bg=main_color, fg=text_color)
    color_menu.config(bg=main_color, fg=text_color)


def night_off():
    main_color = "SystemButtonFace"
    second_color = "SystemButtonFace"
    text_color = "black"
    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg="white")
    toolbar_frame.config(bg=main_color)

    # toolbar buttons
    bold_button.config(bg=second_color)
    italics_button.config(bg=second_color)
    redo_button.config(bg=second_color)
    undo_button.config(bg=second_color)
    color_text_button.config(bg=second_color)

    # File menu colors
    file_menu.config(bg=main_color, fg=text_color)
    edit_menu.config(bg=main_color, fg=text_color)
    color_menu.config(bg=main_color, fg=text_color)


# Create toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Now we will create main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Scrollbar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create horizontal scrollbar
hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# Now create text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="orange",
               undo=True, yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
my_text.pack()

# Configure the scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Print File", command=print_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Now add Edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut         Ctrl-x", command=lambda: cut_text(False))
edit_menu.add_command(label="Copy      Ctrl-c", command=lambda: copy_text(False))
edit_menu.add_command(label="Paste      Ctrl-v", command=lambda: paste_text(False))
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=lambda: select_all(True), accelerator="(Ctrl+a)")
edit_menu.add_command(label="Clear", command=clear_all, accelerator="(Ctrl+y)")

# Now we add Color menu
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Selected Text", command=text_color)
color_menu.add_command(label="All Text", command=all_text_color)
color_menu.add_command(label="Background", command=bg_color)

# Add Options menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Night Mode On", command=night_on)
options_menu.add_command(label="Night Mode Off", command=night_off)

# Add status Bar
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# Here we will edit bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)
root.bind('Control-A', select_all)
root.bind('Control-a', select_all)

# Here we will create buttons
bold_button = Button(toolbar_frame, text="Bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

italics_button = Button(toolbar_frame, text="Italics", command=italics_it)
italics_button.grid(row=0, column=1, padx=5)

undo_button = Button(toolbar_frame, text="Undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)

redo_button = Button(toolbar_frame, text="Redo", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

color_text_button = Button(toolbar_frame, text="Text Color", command=text_color)
color_text_button.grid(row=0, column=4, padx=5)

root.mainloop()
