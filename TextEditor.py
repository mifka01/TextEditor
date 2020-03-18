import os
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle
from random import choice
from FileButton import FileButton


class TextEditor(tk.Frame):
    """Application instance.

    Note
    ----
    Requires tkinter.Tk() as a parameter.

    Attributes
    ----------
    files_in_tab : list of dict ({"file": x, "tab": y})
    current_file_ref : dict ({"file": x, "tab": y})
    untitled_count : 0
        For the purposes of keeping track of the untitled files.

    Methods
    -------
    initialize_user_interface()
        Creates the widgets and styles.
    new_file()
        Gives the user a new blank untitled page.
    prompt_to_open_file()
        Tells the user to append a new file into the tab.
    open_file()
        Gives the user the 'select file to open' menu and
        adds the corresponding file to the application.
    remove_file_from_app(file reference, os_remove=False)
        Removes the file reference from the `files_in_tab` list and
        from the system if wanted.
    save_file(permanent=True, file_ref=None)
        Stores the text in the text field into the file
        in the user's system, and saves the untitled file
        as a new text file if the user agrees.
    switch_tabs(tab_file_ref)
        Changes the text field to contain the text of the new file,
        and saving the previous tab's data.

    """
    files_in_tab = []
    current_file_ref = None
    untitled_count = 0

    # Colors
    FOREGROUND_COLOR = "#282828"
    BACKGROUND_COLOR = "white"

    # Fonts
    BUTTON_FONT = ('Microsoft Sans Serif', 10)
    # TITLE_FONT = tk_font(family='Georgia', size=30, weight="bold")
    TEXT_FONT = ('Microsoft Sans Serif', 14)

    def __init__(self, master=None):
        """Initialize the app instance.

        Parameter
        ---------
        master : tkinter.Tk()
            The toplevel widget of Tk.

        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.initialize_user_interface()
        self.prompt_to_open_file()  # Tells user to open something

    def initialize_user_interface(self):
        """Create the widgets and configure the styles."""
        self.create_widgets()
        self.configure_styles()

    def configure_styles(self):
        style = ThemedStyle(self.master)

        style.set_theme("default")

        style.configure(
            'TButton',
            foreground=self.FOREGROUND_COLOR,
            background=self.BACKGROUND_COLOR,
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
            font=self.BUTTON_FONT
        )

        style.configure(
            'Current.File.TButton',
            background=self.FOREGROUND_COLOR,
            foreground=self.BACKGROUND_COLOR
        )

    def create_widgets(self):
        """Createst the widgets needed for the application."""
        # Initialize text_frame
        self.text_frame = tk.Frame(self.master)
        self.text_frame['bg'] = self.BACKGROUND_COLOR
        self.text_frame['highlightthickness'] = "0"
        self.text_frame.place(relx=0, rely=0.05, relwidth=1, relheight=1)
        self.initialize_text_field()

        # Initialize button_frame
        self.button_frame = tk.Frame(self.master)
        self.button_frame['bg'] = self.BACKGROUND_COLOR
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
        self.text_field['fg'] = self.FOREGROUND_COLOR
        self.text_field['font'] = self.TEXT_FONT
        self.text_field['wrap'] = tk.WORD
        self.text_field['insertbackground'] = self.FOREGROUND_COLOR
        self.text_field['selectbackground'] = self.FOREGROUND_COLOR
        self.text_field['selectborderwidth'] = "20px"
        self.text_field['state'] = 'normal'
        self.text_field['padx'] = '60'
        self.text_field['pady'] = '20'

        # self.text_field.bind("<Control-e>", title)
        # self.text_field.bind("<Control-r>", color)
        # self.text_field.bind("<Control-v>", paste)
        # self.text_field.bind("<Control-d>", textReset)

    def prompt_to_open_file(self):
        """Removes the text field."""
        self.text_field.delete("1.0", tk.END)
        self.text_field.pack_forget()

    def create_file_reference(self, filename):
        """Returns a file reference dict in the right format."""
        file_reference = {
            "file": filename,
            "tab": FileButton(self, filename)
        }
        return file_reference

    def open_file(self):
        """Adds an existing file in the user's system to the tab.

        If the the file is already in the tab,
        the user will be refered to that existing file instead.

        Returns
        -------
        None
            If the user decides not to open a file after the prompt.
        file_reference: dict ({"file": x, "tab": y})
            The file reference of the file that is opened or switched to.

        """
        file_to_open = filedialog.askopenfile(
            parent=self.master,
            mode='r+'
        )

        # If the user does not want to open
        if file_to_open is None:
            return None

        # If the file already exists in the text editor
        for file_reference in self.files_in_tab:
            if file_reference["file"].name == file_to_open.name:
                self.switch_tabs(file_reference)
                return file_reference

        self.add_file_to_app(file_to_open)
        self.switch_tabs(file_reference)  # Open that file

        return file_reference

    def new_file(self, filename=None, open_instantly=True):
        """Adds a temporary or permanent file to the app.

        Note
        ----
        It is saved in the TextEditor file directory as of now.

        Parameter
        ---------
        filename : str, optional
            If left blank, a temporary untitled file will be created.

        Returns
        -------
        file_ref : dict ({"file": x, "tab": y})

        """
        if filename is None:
            filename = "Untitled-" + str(self.untitled_count) + ".txt"

        with open(filename, "w+", encoding='utf-8') as raw_file:
            file_ref = self.add_file_to_app(raw_file)

        if open_instantly:
            self.switch_tabs(file_ref)

        self.untitled_count += 1

        return file_ref

    def save_new_file(self):
        """Transfer the temporary file's content into a new permanent file.

        The function transfers the information into a new file with a new name,
        deleting the old file's existence in the system and
        replacing it with the file with the same information.

        Note
        ----
        The user has to be on the tab of the file that needs to be saved,
        since the functions works off the `current_file_ref` attribute.

        Returns
        -------
        file reference : dict ({"file": x, "tab": y})
            If user agreed to save.
        None
            If the user clicks no.

        """
        file_to_save = filedialog.asksaveasfile(
            mode='w',
            defaultextension=".txt",
            initialfile="s_" + self.current_file_ref["file"].name
        )

        # If the user click cancel
        if file_to_save is None:
            return None

        # Delete the old untitled file
        self.remove_file_from_app(self.current_file_ref, os_remove=True)

        # Create the new file and appending the text to it
        new_file_ref = self.new_file(file_to_save.name, open_instantly=False)
        self.write_to_file(new_file_ref)

        return new_file_ref

    def hideButton(self, button):
        """Forgets the tab button's pack.

        Parameters
        ----------
        button : FileButton

        """
        button.pack_forget()

    def save_file(self, permanent=True):
        """Stores the text in the text field into the file.

        If the file has not been saved before,
        the function will be directed to save_new_file() instead.
        If permanent is set to False, all untitled files will be saved
        as temporary files.

        Note
        ----
        The user must be on the tab that is going to be saved.

        Parameters
        ----------
        permanent : bool
            Directed towards unsaved files.
        file_ref : dict ({"file": x, "tab": y})

        Returns
        -------
        file_ref : dict ({"file": x, "tab": y})
            The file reference that was recently saved.
        None
            If the user clicks cancel.

        See also
        --------
        save_new_file : If the file had not been saved before.

        """
        file_ref = self.current_file_ref
        is_perm_save = permanent and file_ref["file"].name[0:8] == "Untitled"
        if is_perm_save:
            new_file_ref = self.save_new_file()
            return new_file_ref
        else:
            self.write_to_file(file_ref)
            return file_ref

    def write_to_file(self, file_ref: dict):
        """Writes text field text into the file."""
        with open(file_ref["file"].name, 'r+', encoding='utf-8') as f:
            current_text = self.text_field.get("1.0", tk.END).strip()
            f.truncate()
            f.write(current_text)

    def check_untitled_empty(self, file_reference):
        """Checks if it is an untitled file and if it is empty.

        Parameter
        ---------
        file_reference: dict ({"file": x, "tab": y})

        Returns
        -------
        bool

        """
        if file_reference["file"].name[0:8] != "Untitled":
            return False

        # To ensure that the function is checking on the most updated version
        if self.is_current_file(file_reference):
            self.save_file(permanent=False)

        file_to_check = file_reference["file"]
        with open(file_to_check.name, "r+", encoding="utf-8") as f:
            text = f.read().strip()

        if text == "":
            return True
        else:
            return False

    def find_file_reference(self, raw_file):
        """Iterates through the `files_in_tab` list to find it.

        Parameter
        ---------
        raw_file : IO

        Returns
        -------
        file_reference : dict ({"file": x, "tab": y})
            If found.
        None
            If not found.
        """
        for file_reference in self.files_in_tab:
            if file_reference["file"] == raw_file:
                return file_reference

        return None

    def close_file(self, ref_to_close):
        """Save and quit the file.

        If `ref_to_close` is a raw file,
        the function will retrieve the complete file reference.

        Parameter
        ---------
        ref_to_close : dict ({"file": x, "tab": y})

        """
        # If the parameter isn't the file reference, find it
        if type(ref_to_close) is not dict:
            ref_to_close = self.find_file_reference(ref_to_close)

        if self.check_untitled_empty(ref_to_close):
            self.remove_file_from_app(ref_to_close, os_remove=True)
        else:
            self.save_and_quit(ref_to_close)

        if self.files_in_tab != []:
            if self.is_current_file(ref_to_close):
                self.random_open()
        else:
            self.prompt_to_open_file()

    def save_and_quit(self, ref_to_close):
        """Updates the file's content and close the file.

        It switches to the tab of the file if it is not the
        current tab.

        Parameter
        ---------
        ref_to_close : dict ({"file": x, "tab": y})

        """
        current = False
        if self.is_current_file(ref_to_close):
            current = True

        original_tab = self.current_file_ref

        self.switch_tabs(ref_to_close)
        close_saved = self.save_file()
        if close_saved is not None:  # If user wants to save
            self.remove_file_from_app(close_saved)
        else:  # If the user clicks cancel
            self.remove_file_from_app(ref_to_close, os_remove=True)

        # If the user came from a different tab before, switch back to it
        if not current:
            self.switch_tabs(original_tab)

    def random_open(self):
        """Opens a file in `files_in_tab`.

        Note
        ----
        There needs to be at least one element in `files_in_tab`.

        """
        random_file_reference = choice(self.files_in_tab)
        self.switch_tabs(random_file_reference)

    def add_file_to_app(self, raw_file):
        """Creates file reference and appends it to `files_in_tab`.

        Parameter
        ---------
        raw_file : IO

        Returns
        -------
        file_ref : dict ({"file": x, "tab": y})
            The one that was created.

        """
        file_ref = self.create_file_reference(raw_file)
        self.files_in_tab.append(file_ref)

        return file_ref

    def remove_file_from_app(self, file_reference, os_remove=False):
        """Removes the file tab and as well as the file reference.

        The FileButton tk.Button object disappears from the tab bar,
        and the dict is removed from the `files_in_tab` attribute.

        Parameters
        ----------
        file_reference: dict ({"file": x, "tab": y})
        os_remove : bool, optional

        """
        if file_reference is None:
            return

        file_reference["tab"].pack_forget()
        self.files_in_tab.remove(file_reference)

        if os_remove:
            os.remove(file_reference["file"].name)

        if self.is_current_file(file_reference):
            self.current_file_ref = None

    def focus_tabs(self, focused_raw_file):
        """Reconfigure the styles of the tabs to show which is in use.

        Parameter
        ---------
        focused_raw_file : dict ({"file": x, "tab": y})

        """
        for file_reference in self.files_in_tab:
            if self.is_current_file(file_reference):
                file_reference["tab"].configure(
                    style="File.TButton"
                )
            elif file_reference["file"] == focused_raw_file:
                file_reference["tab"].configure(
                    style="Current.File.TButton"
                )

    def is_current_file(self, file_ref):
        """Returns a bool."""
        current = self.current_file_ref
        if current is not None and file_ref == current:
            return True

        return False

    def switch_tabs(self, tab_file_ref):
        """Save current text and change it to the new file's.

        Parameter
        ---------
        tab_file_ref : dict ({"file": x, "tab": y})

        """
        if type(tab_file_ref) is not dict:
            tab_file_ref = self.find_file_reference(tab_file_ref)

        self.text_field.pack(fill=tk.BOTH, expand=True)  # User needs to type

        if not self.is_current_file(tab_file_ref):
            # Reconfigure colors to show the current file in use
            self.focus_tabs(tab_file_ref["file"])

            # Temporarily save untitled files
            if self.current_file_ref is not None:
                self.save_file(permanent=False)

            self.current_file_ref = tab_file_ref
            self.display_text(tab_file_ref["file"])

    def display_text(self, new_raw_file):
        """Displays text on the text editor based on the file in use.

        Parameter
        ---------
        new_raw_file : IO

        """
        # Refresh the editor
        self.text_field.delete('1.0', tk.END)

        # Replace the editor with the new file's text
        with open(new_raw_file.name, "r+", encoding="utf-8") as f:
            text = f.read()
        self.text_field.insert('1.0', text)

    def ctrlS(self, event):
        self.save_file()

    def ctrlO(self, event):
        self.open_file()

    def ctrlN(self, event):
        self.new_file()

    def ctrlQ(self, event):
        """Closes all tabs and files and quit the app.

        See also
        --------
        close_file : saves and quit the file.

        """
        while self.files_in_tab != []:
            self.close_file(self.files_in_tab[0]['file'])

        self.master.quit()

    def left_file(self, event):
        """Switch to the text on the left file's tab when called.

        Note
        ----
        It will stop when at left-most file tab.

        See also
        --------
        right_file : The same but for the right.

        """
        for index, file_reference in enumerate(self.files_in_tab):
            if self.is_current_file(file_reference):
                if index - 1 < 0:  # User is already at the left-most tab
                    return

                file_ref_to_open = self.files_in_tab[index - 1]

        self.switch_tabs(file_ref_to_open)

    def right_file(self, event):
        """Switch to the text on the right file's tab when called.

        Note
        ----
        It will stop when at right-most file tab.

        See also
        --------
        left_file : The same but for the left.

        """
        for index, file_reference in enumerate(self.files_in_tab):
            if self.is_current_file(file_reference):
                # If the user is already at the right-most tab
                if index + 1 > len(self.files_in_tab) - 1:
                    return

                file_ref_to_open = self.files_in_tab[index + 1]

        self.switch_tabs(file_ref_to_open)
