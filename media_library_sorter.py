import tkinter as tk
from tkinter import filedialog
import pathlib
import shutil


class LibSorter:
    # get the status of the library when obj is created
    def __init__(self, lib_status):
        # read library 'database' to see if one exists
        self.lib_status = lib_status
    
    def view_button_cmd(self):
        print("view button is clicked!")
        if(self.lib_status) == 'no-libraries':
            print("no libraries yet")

    def add_button_cmd(self):
        print("add button is clicked")

    def edit_button_cmd(self):
        print("edit button is clicked")
        # print(f"User input: {entry.get()}")

def label_updater(label, new_text, append=False):

    # if a list separate before printing in label
    if(type(new_text) == list):
        new_text = "\n".join(new_text)

    if(append is True):
        new_text = label["text"] + "\n" + new_text 
        label["text"] = new_text
    else:
        label["text"] = new_text

def entry_reader(entry):
    entry_text = entry.get()
    return entry_text

class CreateLib:

    def __init__(self):
        self.lib_items_all = []

    def add_to_lib(self):

        # clear labels
        label_updater(self.info_label, "")
        # label_updater(self.selected_items_label, "")


        # folder = filedialog.askdirectory(initialdir="lib/", title="select your folder")
        # file = filedialog.askopenfile(mode='r', filetypes=[('Text files', '*.txt')])
        print("Getting user items")

        # user selects items to add
        lib_items = filedialog.askopenfilenames(title='Multiselect Items to Add', filetypes=[('Text files', '*.txt')])
        
        self.lib_items_all = list(lib_items)
        print(f"Selected items: {self.lib_items_all}")
        label_updater(self.selected_items_label, self.lib_items_all)

    def save_to_lib(self):
        
        # get name entered by user
        lib_name = entry_reader(self.lib_name_entry)
        # remove spaces from lib name
        lib_name = lib_name.replace(" ", "")

        # create lib with files if name is not blank or valid and user has selected at least one item
        if (self.lib_items_all == []):
            label_updater(self.info_label, "ERROR: Select at least one file first")
        elif (lib_name == ""):
            label_updater(self.info_label, "ERROR: Name can't be blank")
        elif (len(lib_name) > 50):
            label_updater(self.info_label, "ERROR: Name too long")
        else:
            label_updater(self.info_label, "")
            print(f"Creating lib: {lib_name}")

            # create folder for lib
            try:
                # lib_name = "lib-"+lib_name
                lib_name = "libraries/"+lib_name
                lib_folder = pathlib.Path(lib_name)
                lib_folder.mkdir(parents=True, exist_ok=False)
                label_updater(self.info_label, f"Library '{lib_name}' created!")
            except(FileExistsError):
                label_updater(self.info_label, "ERROR: Library already exists, enter a different name")
            except Exception as except_message:
                label_updater(self.info_label, f"ERROR: {except_message}")

            # copy media items to folder
            print("Copying items to lib:")
            for each_item in self.lib_items_all:
                print(each_item)
                shutil.copy(each_item, lib_folder)

def setup_tk(media_lib):
    colour_bg_title = "white"
    colour_bg = "#abcdef"
    colour_btn = "green"
    colour_txt = "white"

    print(media_lib.lib_status)

    window = tk.Tk()
    window.geometry("500x500")
    window.rowconfigure([0, 1, 2, 3, 4], minsize=100, weight=1)
    window.columnconfigure([0, 1, 2], minsize=100, weight=1)
    window.title("Media Library Sorter")

    # main window
    main_frame = tk.Frame(window)

    tk.Label(main_frame, text="Click an option to organise your libraries", fg="white", bg="black").pack()

    view_button = tk.Button(main_frame, text="View Libraries", command=media_lib.view_button_cmd, width=25, height=5, bg="green", fg="white")
    view_button.pack()

    add_button = tk.Button(main_frame,text="Add Libraries", command=media_lib.add_button_cmd, width=25, height=5, bg="green", fg="white")
    add_button.pack()

    edit_button = tk.Button(main_frame, text="Edit Libraries", command=media_lib.edit_button_cmd, width=25, height=5, bg="green", fg="white")
    edit_button.pack()

    entry = tk.Entry(main_frame, fg="black", bg="white", width=50)
    entry.pack()

    
   # --- add libraries frame

    # object to handle creating new libs
    new_lib = CreateLib()

    addlib_frame = tk.Frame(window, bg="#abcdef")

    add_label = tk.Label(addlib_frame, text="Add New Library", font=('Aeriel 20 bold'), bg=colour_bg_title)
    add_label.grid(row=0, column=0, columnspan=2, sticky="we")

    # Button to select files
    add_button = tk.Button(addlib_frame, text="Browse Files To Add", command=new_lib.add_to_lib, bg=colour_btn, fg=colour_txt, width=15, height=2)
    add_button.grid(row=1, column=0)

    # Libs selected
    new_lib.selected_items_label = tk.Label(addlib_frame, text="None selected yet", font=('Aeriel 10 bold'), bg=colour_bg)
    # new_lib.selected_items_label.pack()
    new_lib.selected_items_label.grid(row=1, column=1)

    # Entry to get library name
    new_lib.enter_name_label = tk.Label(addlib_frame, text="Enter Name of Library:", font=('Aeriel 10 bold'), bg=colour_bg)
    # new_lib.enter_name_label.pack()
    new_lib.enter_name_label.grid(row=2, column=0, pady=10)

    new_lib.lib_name_entry = tk.Entry(addlib_frame, bg=colour_txt, width=25)
    # new_lib.lib_name_entry.pack()
    new_lib.lib_name_entry.grid(row=2, column=1)

    save_button = tk.Button(addlib_frame, text="Save Library", command=new_lib.save_to_lib, bg=colour_btn, fg=colour_txt, width=15, height=2)
    # save_button.pack()
    save_button.grid(row=3, column=0, pady=10)

    # Info label
    new_lib.info_label = tk.Label(addlib_frame, text="", fg="red", bg=colour_bg)
    # new_lib.info_label.pack()
    new_lib.info_label.grid(row=4, column=0)

    # frames to display on window
    # main_frame.pack()
    addlib_frame.pack()

    # run Tkinter event loop 
    window.mainloop()

    
def start_program_flow():

    # object to handle lib functions
    media_lib = LibSorter("no-libraries")
       
    # setup tk window, pass lib object
    setup_tk(media_lib)


if __name__ == "__main__":
    start_program_flow()