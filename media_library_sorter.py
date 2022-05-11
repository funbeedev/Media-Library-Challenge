import tkinter as tk
from tkinter import filedialog
import pathlib
import shutil
from abc import ABC, abstractmethod

def label_updater(label, label_text, append=False):

    # if list is supplied print each portion separately
    if(type(label_text) == list):
        if(append is False):  # clear label to refresh full list
            label["text"] = ""

        for element in label_text:  
            if(len(element) == 1):
                label_text = "\n".join(element)
            else:  # TODO: avoid separated elements when multiple items are selected in dialogue
                label_text = "".join(element)
            label_text = label["text"] + "\n" + label_text
            label["text"] = label_text 
        return

    # if a string add to label, append if specified
    if(append is True):
        label_text = label["text"] + "\n" + label_text
        label["text"] = label_text
    else:
        label["text"] = label_text


def entry_reader(entry):
    entry_text = entry.get()
    return entry_text


class TkElements(ABC):
    lib_folder = "libraries/"
    lib_config_file = "libraries.config"

    colour_bg_title = "white"
    colour_bg = "#abcdef"
    colour_btn = "green"
    colour_txt = "white"
    colour_info = "red"
    window = tk.Tk()

    # construct the GUI window
    def __init__(self):
       self.window.geometry("700x700")
       self.window.rowconfigure([0, 1, 2, 3, 4], minsize=100, weight=1)
       self.window.columnconfigure([0, 1, 2], minsize=100, weight=1)
       self.window.title("Media Library Sorter")

    # ensure method is used in inherited classes
    @abstractmethod
    def draw_frame(self):
        pass

class CreateLib(TkElements):

    # draw widgets for creating libraries  
    def draw_frame(self):
        
        self.lib_items_all = []

        # construct frame for adding items to a library    
        addlib_frame = tk.Frame(TkElements.window, bg="#abcdef")

        add_label = tk.Label(addlib_frame, text="Add New Library", font=('Aeriel 20 bold'), bg=TkElements.colour_bg_title)
        add_label.grid(row=0, column=0, columnspan=2, sticky="we")

        # Button to select files
        add_button = tk.Button(addlib_frame, text="Browse Files To Add", command=self.add_to_lib, bg=TkElements.colour_btn, fg=TkElements.colour_txt, width=15, height=2)
        add_button.grid(row=1, column=0)

        # Label to show files selected
        self.selected_items_label = tk.Label(
            addlib_frame, text="Select items to add", font=('Aeriel 10 bold'), bg=TkElements.colour_bg)
        self.selected_items_label.grid(row=1, column=1)

        # Entry to get library name
        enter_name_label = tk.Label(addlib_frame, text="Enter Name of Library:", font=('Aeriel 10 bold'), bg=TkElements.colour_bg)
        enter_name_label.grid(row=2, column=0, pady=10)

        self.lib_name_entry = tk.Entry(addlib_frame, bg=TkElements.colour_txt, width=25)
        self.lib_name_entry.grid(row=2, column=1)

        # Button to save library
        save_button = tk.Button(addlib_frame, text="Save Library", command=self.save_to_lib, bg=TkElements.colour_btn, fg=TkElements.colour_txt, width=15, height=2)
        save_button.grid(row=3, column=0, pady=10)

        # Info label will provide feedback to user
        self.info_label = tk.Label(
            addlib_frame, text="", fg=TkElements.colour_info, bg=TkElements.colour_bg)
        self.info_label.grid(row=4, column=0)

        # display frame on window
        addlib_frame.pack()


    def add_to_lib(self):

        # clear labels
        label_updater(self.info_label, "")
        print("Browse button clicked")

        # dialog asks user for items to add, append each to a list
        selected_items = filedialog.askopenfilenames(title='Select one or multiple items', filetypes=[('Any', '*')])

        # handle when user multi selects items from dialog
        if (len(selected_items) > 1):
            for each_item in list(selected_items):
                self.lib_items_all.append(each_item)
        else:
            self.lib_items_all.append(list(selected_items))
        
        # update label with selected items
        print(f"Selected items: {self.lib_items_all}")
        label_updater(self.selected_items_label, self.lib_items_all)

    def save_to_lib(self):
        
        # get name entered by user
        lib_name = entry_reader(self.lib_name_entry)
        # remove spaces from lib name if any
        lib_name = lib_name.replace(" ", "")

        # create lib with files if name is not blank or invalid and if user has selected at least one item
        if (self.lib_items_all == []):
            label_updater(self.info_label, "ERROR: Select at least one file first")
        elif (lib_name == ""):
            label_updater(self.info_label, "ERROR: Name can't be blank")
        elif (len(lib_name) > 50):
            label_updater(self.info_label, "ERROR: Name too long")
        else:
            label_updater(self.info_label, "")
            print(f"Creating lib: {lib_name}")

            # create folder representing lib
            try:
                # lib_name = "lib-"+lib_name
                lib_name = "libraries/"+lib_name
                lib_folder = pathlib.Path(lib_name)
                lib_folder.mkdir(parents=True, exist_ok=False)
                label_updater(self.selected_items_label, "Select items to add")

                #  get file path and copy items to lib folder
                print("Copying items to lib:")
                for each_item in self.lib_items_all:
                    print(each_item)
                    shutil.copy("".join(each_item), lib_folder)

                label_updater(self.info_label, f"Library '{lib_name}' created!")
                self.lib_items_all = []
                # refresh lib structure
                refresh_lib_config_file()

            except(FileExistsError):
                label_updater(self.info_label, "ERROR: Library already exists, enter a different name")
            except Exception as except_message:
                label_updater(self.info_label, "ERROR: exception")
                print(except_message)
                self.lib_items_all = []




class ViewLib(TkElements):

    all_libs_list = []

    # frame to hold dynamic buttons for each  existing lib 
    libbuttons_frame = tk.Frame(TkElements.window)  

    def __init__(self):
        # ensure lib folder exists, if not create
        lib_path = pathlib.Path(self.lib_folder)
        if(lib_path.is_dir() is False):
            print("libraries folder doesn't exist, creating")
            lib_path.mkdir()

    # draw widgets for viewing libraries  
    def draw_frame(self):
        viewlib_frame = tk.Frame(TkElements.window) 

        yourlib_label = tk.Label(viewlib_frame, text="Your Existing Libraries", font=('Aeriel 20 bold'), bg=TkElements.colour_bg_title)
        yourlib_label.grid(row=0, column=0, columnspan=2, sticky="we")

        # viewlib_button = tk.Button(viewlib_frame, text="View Existing Libraries", command=get_and_list_libs, bg=TkElements.colour_btn, fg=TkElements.colour_txt, width=15, height=2)
        # viewlib_button.grid(row=1, column=0)

        ViewLib.viewlib_label = tk.Label(viewlib_frame, text=".", font=('Aeriel 10 bold'))
        ViewLib. viewlib_label.grid(row=2, column=0)

        # display frame in window
        viewlib_frame.pack()
        self.libbuttons_frame.pack()


def refresh_lib_config_file():
    # iterate through all items in library folders. get name of lib and items in each lib
    # generate list of lists representing all library items - format: [[lib1-name, lib1-item1, lib1-item2], [lib2-name, lib2-item1], [...]]
    index = 0
    ViewLib.all_libs_list = []
    for folder_path in pathlib.Path(TkElements.lib_folder).iterdir():
        if(folder_path.is_dir()):
            ViewLib.all_libs_list.append([])
            # print(index)
            # print(folder_path)
            remove_folder_path = str(folder_path).replace(TkElements.lib_folder, "")  # remove folder path from string before appending to list
            ViewLib.all_libs_list[index].append(remove_folder_path)

            for file_path in pathlib.Path(folder_path).iterdir():
                if file_path.is_file():
                    # print(file_path)
                    str_remove = TkElements.lib_folder + remove_folder_path + "/"
                    remove_file_path = str(file_path).replace(str_remove, "")  # remove file path from string before appending to list
                    ViewLib.all_libs_list[index].append(remove_file_path)
            index += 1

    # write list representing library config to file
    path_to_write = TkElements.lib_folder+TkElements.lib_config_file
    with open(path_to_write, "w+") as f_config:
        for element in ViewLib.all_libs_list:
            # element = str(element) + "\n" # write to file as pure list
            element = ",".join(element) # write to file as comma separated
            f_config.write(element+"\n")
    
    # show the current lib status after refreshing
    get_and_list_libs()

def get_and_list_libs():
    

    print("refreshing lib list") 
    # print(*ViewLib.all_libs_list, sep="\n")     

    if(len(ViewLib.all_libs_list) == 0):
        print("No library items")
        label_updater(ViewLib.viewlib_label, "No library items found, add one first")
        return

    # label_updater(self.viewlib_label, "")
    # extract lib names and create widget for each
    index = 0
    label_updater(ViewLib.viewlib_label, "Select a library to view or edit")
    for element in ViewLib.all_libs_list:
        get_lib_name = element[0]
        print(f"lib name: {get_lib_name}")

        # create buttons for each lib item, button can be referenced by index in library list
        tk.Button(ViewLib.libbuttons_frame, text=get_lib_name, command=lambda x=index+1: edit_lib_item(x), width=10, height=3, bg="blue", fg="white").grid(row=0, column=0+index)
        index += 1


def edit_lib_item(lib_index):
    print("edit lib button clicked")
    print(lib_index)


def setup_window():
    # handle common tk elements
    # tk_elements = TkElements()
    
    # handle creating new libs
    new_lib = CreateLib()
    new_lib.draw_frame()
    
    # handle viewing libs
    view_lib = ViewLib()
    view_lib.draw_frame()

    # regenerate config file from current library structure
    refresh_lib_config_file()

    # start Tkinter event loop
    TkElements.window.mainloop()
    

def start_program_flow():
    print("--- Start ---")
    setup_window()


if __name__ == "__main__":
    start_program_flow()
