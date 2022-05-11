# Media Library Sorter

Application to organise items into libraries.

## Info and Setup
- Uses Tkinter library for GUI.
- Tested on Linux PCs only.
- Install Python3: `sudo apt-get install python3`
- Run program: `python3 media_library_sorter.py`

This program relies on the `libraries` folder contents to display status of library items.
When the program is run the first time, a directory is created in the same directory as this program called `libraries` that will be used to build and maintain the structure of library names and items.  
For example, if libraries `lib1` and `lib2` are added using the program, the following files are created: `libraries/lib1`, `libraries/lib2`.

## Usage
![app_screenshot](https://user-images.githubusercontent.com/66768334/167768051-7e450e70-da5c-45de-a454-d31eeac83c0f.png)

### Adding items to library

- Click the browse button and select the files to add
- Enter a name for the library
- Click Save library 

### Viewing libraries

- When a library is saved, the window will update to include any added libraries
- Click on the button displaying the library name to list items currently stored under the library

### Deleting libraries

- Click on the button displaying the library name or enter the name into the field
- Click the delete library button

## Known issues

- Program currently can't handle too many library items as widgets will go out of screen
- Responsiveness of GUI needs improvement
