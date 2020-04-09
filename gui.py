from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mb

from mainFunc import main

# create our main window
root = Tk()
root.title("COVID-19 statistics")

# initialize our global variables 
UserPath = StringVar()

# main function to run
def calculate(*args):
    try:
        FilePath = UserPath.get().strip('"')
        if FilePath.endswith('.csv'):
            main(FilePath)
        else:
            raise IOError("need a csv file")

    except IOError as error:
        # will show dialogue with the text: "need a csv file"
        mb.showinfo('File error', error)

    # if exception type is not IOError- will continue to the next exception block 
    except Exception:
        mb.showinfo('some error', error)

        # print full error for debugging 
        import traceback
        traceback.print_exc()
    
    
# start working on our GUI-
# create a frame inside our window to work on. optional, but a good practice
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

ttk.Label(mainframe, text="path to csv file:").grid(column=0, row=0, sticky=(W, E))
UserPathEntry = ttk.Entry(mainframe, textvariable=UserPath, width=45)
# textvariable=UserPath == associate global variable (UserPath) with the input from the entry
UserPathEntry.grid(column=0, row=1, columnspan=2)
UserPathEntry.focus() # at the app opening - the mouse cursor will be inside the entry

# create choose file button
def getFile():
    name = filedialog.askopenfilename(filetypes = [("CSV UTF-8 (Comma delimited)","*.csv")])
    UserPath.set(name)
ttk.Button(mainframe, text='Choose File',command=getFile).grid(column=2, row=1)

ttk.Button(mainframe, text="run", command=calculate).grid(column=1, row=2,sticky=W)

# add some space between widgets
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# bind enter key to run the app (in addition to user click on button)
root.bind('<Return>', calculate)

# show the GUI
root.mainloop()
