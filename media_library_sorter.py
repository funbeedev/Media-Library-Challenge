import tkinter as tk


class LibSorter:
    # get the status of the library when obj is created
    def __init__(self, lib_status):
        # read library 'database' to see if one exists
        self.lib_status = 'no-libraries'
    
    def view_button_cmd(self):
        print("view button is clicked!")
        if(self.lib_status) == 'no-libraries':
            print("no libraries yet")

    def add_button_cmd(self):
        print("add button is clicked")

    def edit_button_cmd(self):
        print("edit button is clicked")
        # print(f"User input: {entry.get()}")


def setup_tk(media_lib):
    print(media_lib.lib_status)

    window = tk.Tk()
    window.geometry("500x500")
    window.title("Media Library Sorter")

    # main window
    main_frame = tk.Frame(window)

    tk.Label(main_frame, text="Click an option to organise your libraries", foreground="#abcdef", bg="black").pack()

    view_button = tk.Button(main_frame, text="View Libraries", command=media_lib.view_button_cmd, width=25, height=5, bg="green", fg="white")
    view_button.pack()

    add_button = tk.Button(main_frame,text="Add Libraries", command=media_lib.add_button_cmd, width=25, height=5, bg="green", fg="white")
    add_button.pack()

    edit_button = tk.Button(main_frame, text="Edit Libraries", command=media_lib.edit_button_cmd, width=25, height=5, bg="green", fg="white")
    edit_button.pack()

    entry = tk.Entry(main_frame, fg="red", bg="white", width=50)
    entry.pack()

    main_frame.pack()
    
    # run Tkinter event loop 
    window.mainloop()

    
def start_program_flow():

    # object to handle lib functions
    media_lib = LibSorter("no-libraries")
       
    # setup tk window, pass lib object
    setup_tk(media_lib)


if __name__ == "__main__":
    start_program_flow()