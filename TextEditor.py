import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from TabManager import TabManager


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
        self.initialize_text_frame()
        self.tab_manager = TabManager(self, self.text_field, self.master)
        self.initialize_user_interface()
        self.tab_manager.prompt_to_open_file()  # Tells user to open something

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

    def initialize_text_frame(self):
        self.text_frame = tk.Frame(self.master)
        self.text_frame['bg'] = self.BACKGROUND_COLOR
        self.text_frame['highlightthickness'] = "0"
        self.text_frame.place(relx=0, rely=0.05, relwidth=1, relheight=1)
        self.initialize_text_field()

    def create_widgets(self):
        """Createst the widgets needed for the application."""
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
            command=self.tab_manager.new_file
        )
        self.plus_button.pack(side=tk.LEFT)
        self.plus_button.config(width=3)

        # Initialize open_button
        open_button = ttk.Button(
            self.button_frame,
            style="Open.TButton",
            text="open",
            command=self.tab_manager.open_file
        )
        open_button.pack(side=tk.RIGHT)
        open_button.config(width=len(open_button['text']))

        # Initialize save_button
        save_button = ttk.Button(
            self.button_frame,
            style="TButton",
            text='save',
            command=self.tab_manager.save_file
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
        self.tab_manager.save_file()

    def ctrlO(self, event):
        self.tab_manager.open_file()

    def ctrlN(self, event):
        self.tab_manager.new_file()

    def ctrlQ(self, event):
        """Closes all tabs and files and quit the app.

        See also
        --------
        close_file : saves and quit the file.

        """
        self.tab_manager.close_all_files()

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
        self.tab_manager.left_file(event)

    def right_file(self, event):
        """Switch to the text on the right file's tab when called.

        Note
        ----
        It will stop when at right-most file tab.

        See also
        --------
        left_file : The same but for the left.

        """
        self.tab_manager.right_file(event)
