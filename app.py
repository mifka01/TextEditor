import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle
import os
from random import choice
from platform import system as platform


# Colors
FOREGROUND_COLOR = "#282828"
BACKGROUND_COLOR = "white"

# Fonts
BUTTON_FONT = ('Microsoft Sans Serif', 10)
# TITLE_FONT = tk_font(family='Georgia', size=30, weight="bold")
TEXT_FONT = ('Microsoft Sans Serif', 14)


class TextEditor(tk.Frame):
    files_in_tab = []
    current_file = None
    files_count = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.prompt_to_open_file()  # Tells user to open something

        # Configuring styles
        style = ThemedStyle(master)

        style.set_theme("default")

        style.configure(
            'TButton',
            foreground=FOREGROUND_COLOR,
            background=BACKGROUND_COLOR,
            borderwidth=0,
            highlightthickness=0,
            font=('MS Reference Sans Serif', 15)
        )

        style.configure(
            'Plus.TButton',
            font=('MS Reference Sans Serif', 20)

        )

        style.configure(
            'File.TButton',
            font=BUTTON_FONT
        )

        style.configure(
            'Current.File.TButton',
            background=FOREGROUND_COLOR,
            foreground=BACKGROUND_COLOR
        )

    def create_widgets(self):
        """Createst the widgets needed for the application."""
        # Initialize text_frame
        self.text_frame = tk.Frame(self.master)
        self.text_frame['bg'] = BACKGROUND_COLOR
        self.text_frame['highlightthickness'] = "0"
        self.text_frame.place(relx=0, rely=0.05, relwidth=1, relheight=1)
        self.initialize_text_field()

        # Initialize button_frame
        self.button_frame = tk.Frame(self.master)
        self.button_frame['bg'] = BACKGROUND_COLOR
        self.button_frame['highlightthickness'] = "0"
        self.button_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        # Initialize plus_button
        self.plus_button = ttk.Button(
            self.button_frame,
            style="Plus.TButton",
            text="+",
            command=self.new_file
        )
        self.plus_button.pack(side=tk.LEFT)
        self.plus_button.config(width=3)

        # Initialize open_button
        open_button = ttk.Button(
            self.button_frame,
            style="Open.TButton",
            text="open",
            command=self.open_file
        )
        open_button.pack(side=tk.RIGHT)
        open_button.config(width=len(open_button['text']))

        # Initialize save_button
        save_button = ttk.Button(
            self.button_frame,
            style="TButton",
            text='save',
            command=self.save_file
        )
        save_button.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        save_button.config(width=len(save_button['text']))

    def initialize_text_field(self):
        """Initialize the text field."""
        self.text_field = tk.Text(self.text_frame)
        self.text_field['border'] = '0'
        self.text_field['fg'] = FOREGROUND_COLOR
        self.text_field['font'] = TEXT_FONT
        self.text_field['wrap'] = tk.WORD
        self.text_field['insertbackground'] = FOREGROUND_COLOR
        self.text_field['selectbackground'] = FOREGROUND_COLOR
        self.text_field['selectborderwidth'] = "20px"
        self.text_field['state'] = 'normal'
        self.text_field['padx'] = '60'
        self.text_field['pady'] = '20'

        # self.text_field.bind("<Control-e>", title)
        # self.text_field.bind("<Control-r>", color)
        # self.text_field.bind("<Control-v>", paste)
        # self.text_field.bind("<Control-d>", textReset)

    def prompt_to_open_file(self):
        """Prompt the user to open a file.

        This function removes the text field completely.
        """
        self.text_field.delete("1.0", tk.END)
        self.text_field.pack_forget()

    def open_file(self):
        """Allows user to open a file.

        If the the file is already in the tab,
        the user will be refered to that existing file instead.
        """
        file_to_open = filedialog.askopenfile(
            parent=self.master,
            mode='r+'
        )

        # If the user does not want to open, then return
        if file_to_open is None:
            return

        # If the file already exists in the text editor
        for file_reference in self.files_in_tab:
            if file_reference["file"].name == file_to_open.name:
                self.switch_tabs(file_reference["file"])
                return

        file_reference = {
            "file": file_to_open,
            "tab": FileButton(self, file_to_open)
        }
        self.files_in_tab.append(file_reference)
        self.switch_tabs(file_to_open)  # Open that file

    def new_file(self):
        """Allows user to create a new file.

        It is automatically added to the system and
        opened in the text editor upon creation.

        It is saved in the TextEditor file directory as of now.
        """
        with open(
            "Untitled-" + str(self.files_count) + ".txt",
            "w+",
            encoding='utf-8'
        ) as raw_file:
            file_reference = {
                "file": raw_file,
                "tab": FileButton(self, raw_file)
            }
            self.files_in_tab.append(file_reference)

            self.switch_tabs(raw_file)  # Open the nenwly created file
        self.files_count += 1

    def hideButton(self, button):
        """Hides the the tab button to access a particular file.

        Key arguments:
        button -- FileButton
        """
        button.pack_forget()

    def save_file(self, permanent=True):
        """Saves the file the user is on.

        If the file has not been saved before,
        the function will be directed to save_new_file() instead.
        If permanent is set to False, all untitled files will be saved
        as temporary files.
        """
        if self.current_file is not None:
            if permanent and self.current_file.name[0:8] == "Untitled":
                return self.save_new_file()
            else:
                with open(self.current_file.name, 'r+', encoding='utf-8') as f:
                    current_text = self.text_field.get("1.0", tk.END).strip()
                    f.write(current_text)
                f.close()
                for file_reference in self.files_in_tab:
                    if file_reference['file'] == self.current_file:
                        return file_reference

    def save_new_file(self):
        """Lets the user save a newly created file.

        Returns:
        -- file reference (if user agreed to save)
        -- None (if the user clicks no)

        The function transfers the information into a new file with a new name,
        deleting the old file's existence in the system and
        replacing it with the file with the same information.
        """
        file_to_save = filedialog.asksaveasfile(
            mode='w',
            defaultextension=".txt",
            initialfile="s_" + self.current_file.name
        )

        # If the user did not click cancel
        if file_to_save is not None:
            with open(file_to_save.name, "r+", encoding="utf-8") as f:
                os.remove(self.current_file.name)
                for index, file_reference in enumerate(self.files_in_tab):
                    if file_reference["file"].name == self.current_file.name:
                        file_reference["tab"].pack_forget()
                        self.files_in_tab.pop(index)

                new_file_reference = {"file": f, "tab": FileButton(self, f)}
                self.files_in_tab.append(new_file_reference)

                # Transfers the text from the old file into the new
                f.write(self.text_field.get('1.0', tk.END).strip())
                f.close()
                # Move from the old file to the new
                self.current_file = None
                self.switch_tabs(f)

                return(new_file_reference)
        else:
            return None

    def close_file(self, reference_to_close):
        """Allows the user to close a file.

        Key arguments:
        reference_to_close -- file reference dict or file

        If reference_to_close is a raw file,
        the function retrieve the complete file reference.
        """
        if type(reference_to_close) is not dict:
            for file_reference in self.files_in_tab:
                if file_reference["file"] == reference_to_close:
                    # Reassigns the variable to its file reference
                    reference_to_close = file_reference

        # If the user is closing the current tab
        if self.current_file == reference_to_close["file"]:
            # Save the file (if the user wants to)

            with open(self.current_file.name, "r+", encoding="utf-8") as f:
                text = f.read().strip()

            if text != "":  # If there is text
                new_file_reference = self.save_file()
                self.text_field.delete('1.0', tk.END)

                if new_file_reference is not None:
                    self.remove_file_from_app(new_file_reference)
                else:
                    self.remove_file_from_app(reference_to_close)
            else:
                # If there is no text, then there is no point keeping it
                self.current_file = None
                os.remove(reference_to_close['file'].name)
                self.remove_file_from_app(reference_to_close)

            if self.files_in_tab != []:
                # Open a random file
                random_file_reference = choice(self.files_in_tab)

                self.switch_tabs(random_file_reference["file"])
            else:
                self.prompt_to_open_file()
        else:
            file_to_close = reference_to_close["file"]
            original_file_tab = self.current_file

            if file_to_close.name[0:8] == "Untitled":  # If not saved
                with open(file_to_close.name, "r+", encoding="utf-8") as f:
                    text = f.read().strip()

                if text != "":  # If there is text
                    # Go to that file and ask if the user wants to save
                    self.switch_tabs(f)
                    new_file_reference = self.save_new_file()

                    if new_file_reference is not None:
                        self.remove_file_from_app(new_file_reference)
                    else:
                        os.remove(file_to_close.name)  # Since it is a temp
                        self.remove_file_from_app(reference_to_close)

                    # Go back to the original file once that is closed
                    self.current_file = None
                    self.switch_tabs(original_file_tab)
                else:  # If the untitled file is empty
                    os.remove(file_to_close.name)
                    self.remove_file_from_app(reference_to_close)
            else:  # If it is not called 'Untitled'
                # It is automatically saved since it is saved from tab out
                self.remove_file_from_app(reference_to_close)

    def remove_file_from_app(self, file_reference):
        """Removes the file reference from the app.

        Key argument:
        -- file_reference: dict ({"file": x, "tab": y})

        The FileButton tk.Button object disappears from the tab bar,
        and the dict is removed from the self.files_in_tab variable.
        """

        file_reference["tab"].pack_forget()

        self.files_in_tab.remove(file_reference)

    def focus_tabs(self, focused_raw_file):
        """Focus the tabs to show which one is in use.

        Key argument:
        focused_raw_file
        """
        for file_reference in self.files_in_tab:
            if (self.current_file is not None and
                    file_reference["file"] == self.current_file):
                file_reference["tab"].configure(
                    style="File.TButton"
                )
            elif file_reference["file"] == focused_raw_file:
                file_reference["tab"].configure(
                    style="Current.File.TButton"
                )

    def switch_tabs(self, tab_file):
        self.text_field.pack(fill=tk.BOTH, expand=True)  # User needs to type

        if tab_file == self.current_file:
            pass
        else:
            # Reconfigure colors to show the current file in use
            self.focus_tabs(tab_file)

            # Saves the replaced text, if any
            if self.current_file is not None and len(self.files_in_tab) != 1:
                # Changes to unsaved file are temporary
                self.save_file(False)

            self.current_file = tab_file
            self.display_text(tab_file)

    def display_text(self, new_raw_file):
        """Displays text on the text editor based on the file in use.

        Key argument:
        -- new_raw_file
        """
        # Refresh the editor
        self.text_field.delete('1.0', tk.END)

        # Replace the editor with the new file's text
        with open(new_raw_file.name, "r+", encoding="utf-8") as f:
            text = f.read()
        self.text_field.insert('1.0', text)
        f.close()

    def ctrlS(self, event):
        self.save_file()

    def ctrlO(self, event):
        self.open_file()

    def ctrlN(self, event):
        self.new_file()

    def ctrlQ(self, event):
        """Quit the application."""
        while self.files_in_tab != []:
            self.close_file(self.files_in_tab[0]['file'])

        root.quit()

    def left_file(self, event):
        for index, file_reference in enumerate(self.files_in_tab):
            if file_reference["file"] == self.current_file:
                if index - 1 < 0:  # User is already at the left-most tab
                    return

                file_to_open = self.files_in_tab[index - 1]["file"]
                self.switch_tabs(file_to_open)

    def right_file(self, event):
        for index, file_reference in enumerate(self.files_in_tab):
            if file_reference["file"] == self.current_file:
                # If the user is already at the right-most tab
                if index + 1 > len(self.files_in_tab) - 1:
                    return

                file_to_open = self.files_in_tab[index + 1]["file"]
                self.switch_tabs(file_to_open)


class FileButton(ttk.Button):
    def __init__(self, app, raw_file):
        displayed_name = os.path.basename(raw_file.name)
        super().__init__(
            app.button_frame,
            style="File.TButton",
            text=displayed_name,
            command=lambda: app.switch_tabs(raw_file)
        )
        self.raw_file = raw_file
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.config(width=len(displayed_name))
        self.bind(
            '<Button-2>',  # Right click
            lambda event: app.close_file(self.raw_file)
        )


root = tk.Tk()
root['bg'] = BACKGROUND_COLOR
text_editor = TextEditor(master=root)

# Window settings
text_editor.master.title("Notepad^")
text_editor.master.geometry("900x700")
text_editor.master.iconbitmap('icons/Notepad.ico')

# Binds (if on MACOSX, it is Cmd instead of Ctrl)
if platform() == 'Darwin':
    text_editor.master.bind('<Command-s>', text_editor.ctrlS)
    text_editor.master.bind('<Command-o>', text_editor.ctrlO)
    text_editor.master.bind('<Command-q>', text_editor.ctrlQ)
    text_editor.master.bind('<Command-n>', text_editor.ctrlN)
    text_editor.master.bind('<Command-Left>', text_editor.left_file)
    text_editor.master.bind('<Command-Right>', text_editor.right_file)
    text_editor.master.protocol(
        "WM_DELETE_WINDOW", lambda: text_editor.ctrlQ("")
    )
else:
    text_editor.master.bind('<Control-s>', text_editor.ctrlS)
    text_editor.master.bind('<Control-o>', text_editor.ctrlO)
    text_editor.master.bind('<Control-q>', text_editor.ctrlQ)
    text_editor.master.bind('<Control-n>', text_editor.ctrlN)
    text_editor.master.bind('<Control-Left>', text_editor.left_file)
    text_editor.master.bind('<Control-Right>', text_editor.right_file)
    text_editor.master.protocol(
        "WM_DELETE_WINDOW", lambda: text_editor.ctrlQ("")
    )

root.mainloop()  # Start the program
