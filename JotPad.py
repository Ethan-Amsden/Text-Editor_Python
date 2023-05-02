import tkinter as tk
#import customtkinter
from tkinter import *
# from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import WORD
#import tkFont

"""----- Global variables for the GUI -----"""
global openStatusName
global selected
openStatusName = False
selected = False
wrapType = 0

"""----- Functions for the GUI -----"""
#---------------------
def newFile(e):
    global openStatusName

    openStatusName = False
    textBox.delete("1.0", END)
    main.title('untitled - JotPad')
    statusBar.config(text='New File       ')

#---------------------
def openFile(e):
    textBox.delete("1.0", END)

    textFile = filedialog.askopenfilename(title="Open File",
                                          filetypes=(("Text Files", "*.txt"),
                                                     ("HTML Files", "*.html"),
                                                     ("Python Files", "*.py"),
                                                     ("All Files", "*.*")))
    # check for file name
    if textFile:
        global openStatusName
        openStatusName = textFile
    
    # update status bars
    url = textFile
    url = url.rsplit("/", 1)
    #path = url[0]
    name = url[1]
    
    statusBar.config(text=f'{name}        ')
    main.title(f'{name} - JotPad')

    # Open File
    textFile = open(textFile, 'r')
    contents = textFile.read()
    # add file to textBox
    textBox.insert(END, contents)
    #Close the opened File
    textFile.close()

#---------------------
def saveFile(e):
    global openStatusName

    if openStatusName:
        # Save the file
        textFile = open(openStatusName, 'w')
        textFile.write(textBox.get(1.0, END))
        #Close the opened File
        textFile.close()

        # update status bars
        url = openStatusName
        url = url.rsplit("/", 1)
        #path = url[0]
        name = url[1]

        statusBar.config(text=f'Saved: {name}        ')
    else:
        saveAsFile()

#---------------------
def saveAsFile(e):
    textFile = filedialog.asksaveasfilename(defaultextension=".*",
                                            title="Save File",
                                            filetypes=(("Text Files", "*.txt"),
                                                 ("HTML Files", "*.html"),
                                                 ("Python Files", "*.py"),
                                                 ("All Files", "*.*")))
    if textFile:
        # update status bars
        url = textFile
        url = url.rsplit("/", 1)
        #path = url[0]
        name = url[1]
        
        statusBar.config(text=f'Saved: {name}        ')
        main.title(f'{name} - JotPad')

        # Save the file
        textFile = open(textFile, 'w')
        textFile.write(textBox.get(1.0, END))
        #Close the opened File
        textFile.close()

#---------------------

def wrap():

    if textBox['wrap'] == 'none':
        textBox.config(wrap=WORD)
        horScroll.pack(side=BOTTOM, fill=X) #side=BOTTOM,
    
    elif textBox['wrap'] == 'word':
        textBox.config(wrap=NONE)
        horScroll.pack_forget()
        
    #print line for testing the wrap status
    #print(textBox['wrap'])

#---------------------
def cutText(e):
    global selected

    # check to see if keyboard was used
    if e:
        selected = main.clipboard_get()
    else:
        # check for value
        if textBox.selection_get():
        
            selected = textBox.selection_get()
            textBox.delete("sel.first", "sel.last")
            # replace clipboard contents
            main.clipboard_clear()
            main.clipboard_append(selected)

#---------------------
def copyText(e):
    global selected

    # check to see if keyboard was used
    if e:
        selected = main.clipboard_get()

    # check for value
    if textBox.selection_get():
        
        selected = textBox.selection_get()
        # replace clipboard contents
        main.clipboard_clear()
        main.clipboard_append(selected)

#---------------------
def pasteText(e):
    global selected
    
    # check to see if keyboard was used
    if e:
        selected = main.clipboard_get()
    else:
        # check for value
        if selected:
        
            position = textBox.index(INSERT)
            textBox.insert(position, selected)

#---------------------
def colorBG():
    myColor = colorchooser.askcolor()[1]

    if myColor:
        textBox.config(bg=myColor)

#---------------------
def allTextColor():
    myColor = colorchooser.askcolor()[1]

    if myColor:
        textBox.config(fg=myColor)

#---------------------
def highlightColor():
    myColor = colorchooser.askcolor()[1]

    if myColor:
        #create font color
        highlight = font.Font(textBox, textBox.cget("font"))

        #configure a tag
        textBox.tag_configure("highlighted", font=highlight, background=myColor)

        # define currentTags
        currentTags = textBox.tag_names("sel.first") #, "sel.last"
        
        #See if text is colored
        if "highlighted" in currentTags:
            textBox.tag_remove("highlighted", "sel.first", "sel.last")
        else:
            textBox.tag_add("highlighted", "sel.first", "sel.last")

#--------themes-------
def defaultCLR():
    BG = 'white'
    FG = 'black'

    textBox.config(bg=BG,fg=FG,insertbackground=FG)

def night_1():
    BG = 'black'
    FG = 'white'

    textBox.config(bg=BG,fg=FG,insertbackground=FG)

def night_2():
    BG = 'black'
    FG = 'green'

    textBox.config(bg=BG,fg=FG,insertbackground=FG)

def parchment():
    BG = 'navajo white'
    FG = 'black'

    textBox.config(bg=BG,fg=FG,insertbackground=FG)
    

"""----- Start of the GUI -----"""
# create window
main = Tk()
main.title('JotPad')
main.geometry("800x680")

# Create Main Frame
MFrame = Frame(main, bd=0)
MFrame.pack() #pady=5

# add status bar to bottom of app
statusBar = Label(MFrame, text='Ready   ', anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=5)

# Create scrollbars for the textbox
vertScroll = Scrollbar(MFrame)
horScroll = Scrollbar(MFrame, orient="horizontal")

vertScroll.pack(side=RIGHT, fill=Y)
horScroll.pack(side=BOTTOM, fill=X)

# Create textbox
textBox = Text(MFrame, width=130, height=33, bd=0,               
               font=("Consolas", 12),
               undo=True, yscrollcommand=vertScroll.set,
               xscrollcommand=horScroll.set,
               wrap='none')

textBox.pack()

# Configure Scrollbar
vertScroll.config(command=textBox.yview)
horScroll.config(command=textBox.xview)

# Create Menu
toolMenu = Menu(main)
main.config(menu=toolMenu)

# add file menu
fileMenu = Menu(toolMenu, tearoff=False)
toolMenu.add_cascade(label="File", menu=fileMenu)

fileMenu.add_command(label="New", command=lambda: newFile(False), accelerator="(Ctrl+N)")
fileMenu.add_command(label="Open", command=lambda: openFile(False), accelerator="(Ctrl+O)")
fileMenu.add_command(label="Save", command=lambda: saveFile(False), accelerator="(Ctrl+S)")
fileMenu.add_command(label="Save As", command=lambda: saveAsFile(False)) #, accelerator="(Ctrl+Shift+S)"
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=main.destroy)

# File Menu Bindings
main.bind('<Control-Key-n>', newFile)
main.bind('<Control-Key-o>', openFile)
main.bind('<Control-Key-s>', saveFile)
#main.bind('<Control-Shift-Key-s>', saveFile)

#add edit menu
editMenu = Menu(toolMenu, tearoff=False)
toolMenu.add_cascade(label="Edit", menu=editMenu)

editMenu.add_command(label="Undo", command=textBox.edit_undo, accelerator="(Ctrl+Z)")
editMenu.add_command(label="Redo", command=textBox.edit_redo, accelerator="(Ctrl+Y)")
editMenu.add_separator()
editMenu.add_command(label="Cut", command=lambda: cutText(False), accelerator="(Ctrl+X)")
editMenu.add_command(label="Copy", command=lambda: copyText(False), accelerator="(Ctrl+C)")
editMenu.add_command(label="Paste", command=lambda: pasteText(False), accelerator="(Ctrl+V)")

# Edit Menu Bindings
main.bind('<Control-Key-x>', cutText)
main.bind('<Control-Key-c>', copyText)
main.bind('<Control-Key-v>', pasteText)

#add view menu
viewMenu = Menu(toolMenu, tearoff=False)
toolMenu.add_cascade(label="View", menu=viewMenu)

viewMenu.add_checkbutton(label="Wrap",
                         variable = wrapType,
                         onvalue = 1,
                         offvalue = 0,
                         command=lambda: wrap())

#add color menu
colorMenu = Menu(toolMenu, tearoff=False)
toolMenu.add_cascade(label="Color", menu=colorMenu)

#colorMenu.add_command(label="highlight Color", command=highlightColor)
#colorMenu.add_separator()

colorMenu.add_command(label="All Text", command=allTextColor)
colorMenu.add_command(label="Background", command=colorBG)
colorMenu.add_separator()

themesMenu = Menu(colorMenu, tearoff=False)
colorMenu.add_cascade(label="Themes", menu=themesMenu)

themesMenu.add_command(label="Default", command=defaultCLR)
themesMenu.add_command(label="Night 1", command=night_1)
themesMenu.add_command(label="Night 2", command=night_2)
themesMenu.add_command(label="Parchment", command=parchment)

# MAIN LOOP
main.mainloop()
