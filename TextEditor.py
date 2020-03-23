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
