# For the Organizer 
import os 
import pathlib 
import shutil

# For the interface
import sys
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox

# Create a configuration of the main app
root = ttk.Window(themename="cyborg")
root.title("File organizer")
root.geometry('500x300')

# Main Title
mainTitle = ttk.Label(
            master=root,
            text='Folder Organizer',
            font=('Arial', 30),
            bootstyle="secondary"
        )
mainTitle.pack(side="top")

# Function to select the folder thet you want to organize and store in a var
# for futures uses in our script 
folderPath = tk.StringVar()
def selectFolder():
    folderSelected = filedialog.askdirectory()
    folderPath.set(folderSelected)

# Create a frame with a colored background (to act like a border) and 
# for we organize where in our app the folder selection will be.
borderFrame = ttk.Frame(root, 
                        bootstyle = "primary", )
borderFrame.pack(side="top", fill="x", pady=2)

# Creating the Buton to select the folder
selectButton = ttk.Button(borderFrame, 
                           text="Select Folder",
                           bootstyle = "primary",
                           command=selectFolder)
selectButton.pack(side="right")

# Create the label inside the border frame for show the path the user choose
DisplayLabel = ttk.Label(borderFrame,
                        bootstyle = "primary", 
                        textvariable=folderPath)
DisplayLabel.pack(side='left', fill="x", expand="yes", padx=1, pady=1)


# Create a frame for our logs and the organizer button
logFrame = ttk.Frame(root, 
                    bootstyle = "primary", )
logFrame.pack(side="top", fill="x")

# Function to add logs to the Text widget
def add_log(log_entry):
    log_text.insert(tk.END, log_entry + '\n')
    log_text.see(tk.END)  # Auto-scroll to the end

# The organizer function

def organizeFolder():
    # For convert the var format for text
    selectedPath = folderPath.get()

    # Check if the directory is valid.
    if os.path.isdir(selectedPath)== False :
        messagebox.showinfo("Alert", "Insert a valid folder first!!")
        return()
    
    # Define which format goes to which folder
    fileFormat = {
	"Web": [".html5", ".html", ".htm", ".xhtml"], 
	
    "Pictures": [".jpeg", ".jpg", ".tiff", ".gif",
        ".bmp", ".png", ".bpg", "svg",".heif", ".psd"], 
	
    "Videos": [".avi", ".mkv",".flv", ".wmv",
        ".mov", ".mp4", ".webm", ".vob", 
        ".mng",".qt", ".mpg", ".mpeg", ".3gp", ".srt"], 
	
   "Documents": [".oxps", ".epub", ".pages", ".docx",
        ".txt", ".pdf", ".doc", ".fdf", ".bib",
        ".ods",".odt", ".pwi", ".xsn",
        ".xps", ".dotx", ".docm", ".dox",
        ".rvg", ".rtf", ".rtfd", ".wpd", 
        ".xls", ".xlsx", ".ppt","pptx"], 
	
    "Compressed": [".a", ".ar", ".cpio", ".iso", 
        ".tar", ".gz", ".rz", ".7z",
        ".dmg", ".rar", ".xar", ".zip"], 
	
    "Audios": [".aac", ".aa", ".aac", ".dvf",
        ".m4a", ".m4b", ".m4p", ".mp3",
        ".msv", "ogg", "oga", ".raw", 
        ".vox", ".wav", ".wma"], 
    } 

    fileTypes = list(fileFormat.keys())
    fileFormats = list(fileFormat.values())

    # Start the loop pickin a file in the folder and defining
    # by the format the folder that it belong 
    add_log("Organizing your folder...")
    for file in os.scandir(selectedPath):
        fileName=pathlib.Path(file)
        fileFormatType=fileName.suffix.lower()
        
        src=str(fileName)
        # This is the variable that store the distiny
        # folder that the file will be moved
        dest=os.path.join(selectedPath, "Other")
        
        # If the file has one of this extensions (like folder)
        # We just skip a iteration
        if fileFormatType =="" :
            continue
        else:
            #By default if dont belong tho our categories we will move to Others
            folder = "Others"

            # Compare the format file with our list of formats
            # To decide the folder that we will move

            for formats in fileFormats:
                if fileFormatType in formats:
                    folder=fileTypes[fileFormats.index(formats)]
            dest=os.path.join(selectedPath, folder)
            # If there is no folder yet, this will create the necessary folder
            if os.path.isdir(dest)== False :
                os.mkdir(dest)
        logText = fileName.stem + " has been moved to " + folder
        add_log(logText)
        shutil.move(src,dest)
    add_log("Done!")


#Create the button to organize the folder:

organizerButton = ttk.Button(logFrame, 
                           text="Organize",
                           bootstyle = "primary",
                           command=organizeFolder)
organizerButton.pack(fill="x", expand="yes",)

#Log display:
log_text = tk.Text(logFrame,
                   wrap=tk.WORD)
log_text.pack(fill="x", expand="yes",)


root.mainloop()