import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.font import Font as tk_font
import os


# Colors
FOREGROUND_COLOR = "#282828"
BACKGROUND_COLOR = "white"

# Fonts
BUTTON_FONT = ('Microsoft Sans Serif', 10)
# TITTLE_FONT = tk_font(family='Georgia', size=30, weight="bold")
TEXT_FONT = ('Microsoft Sans Serif', 14)


class TextEditor(tk.Frame):
    files_in_tab = []
    current_file = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.new_file()  # The blank file the user sees at start up

        # Configuring styles
        style = ttk.Style()

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
        # Initialize self.text_field
        text_canvas = tk.Canvas(self.master)
        text_canvas['bg'] = BACKGROUND_COLOR
        text_canvas['highlightthickness'] = "0"
        text_canvas.place(relx=0, rely=0.05, relwidth=1, relheight=1)

        self.text_field = tk.Text(text_canvas)
        self.text_field['border'] = '0'
        self.text_field['fg'] = FOREGROUND_COLOR
        self.text_field['font'] = TEXT_FONT
        self.text_field['wrap'] = tk.WORD
        self.text_field['insertbackground'] = FOREGROUND_COLOR
        self.text_field['selectbackground'] = FOREGROUND_COLOR
        self.text_field['selectborderwidth'] = "20px"
        self.text_field['state'] = 'normal'
        self.text_field['padx'] = '80'
        # self.text_field.bind("<Control-e>", title)
        # self.text_field.bind("<Control-r>", color)
        # self.text_field.bind("<Control-v>", paste)
        # self.text_field.bind("<Control-d>", textReset)

        self.text_field.pack(fill=tk.X)

        # Initialize plus_button
        self.plus_button = ttk.Button(
            self,
            style="Plus.TButton",
            text="+",
            command=self.new_file
        )
        self.plus_button.pack(side=tk.LEFT, fill=tk.Y)
        self.plus_button.config(width=3)

        # Initialize open_button
        open_button = ttk.Button(
            self,
            style="Open.TButton",
            text="open",
            command=self.open_file
            )
        open_button.pack(side=tk.RIGHT, fill=tk.Y)
        open_button.config(width=len(open_button['text']))

        # Initialize save_button
        save_button = ttk.Button(
            self,
            style="TButton",
            text='save',
            command=self.save_file
        )
        save_button.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        save_button.config(width=len(save_button['text']))

    def open_file(self):
        """Allows user to open a file.

        If the the file is already in the tab,
        the file will not be opened again.
        """
        file_to_open = filedialog.askopenfile(
            parent=self.master,
            mode='r+'
        )
        entry = True
        for file_reference in self.files_in_tab:
            if file_reference["file"].name == file_to_open.name:
                entry = False
            else:
                pass

        if file_to_open is not None and entry:
            file_reference = {
                "file": file_to_open,
                "tab": FileButton(self, file_to_open)
            }
            self.files_in_tab.append(file_reference)
            self.switch_tabs(file_to_open)

    def new_file(self):
        """Allows user to create a new file.

        It is automatically added to the system and
        opened in the text editor upon creation.

        It is saved in the TextEditor file directory as of now.
        """
        raw_file = open(
            "Untitled-" + str(len(self.files_in_tab)) + ".txt",
            "w+",
            encoding='utf-8'
        )
        file_reference = {"file": raw_file, "tab": FileButton(self, raw_file)}
        self.files_in_tab.append(file_reference)
        self.switch_tabs(raw_file)
        raw_file.close()

    def hideButton(self, button):
        """Hides the the tab button to access a particular file.

        Key arguments:
        button -- FileButton
        """
        button.pack_forget()

    def save_file(self):
        """Saves the file the user is on.

        If the file has not been saved before,
        the function will be directed to save_new_file() instead.
        """
        if self.current_file is not None:
            if self.current_file.name[0:8] == "Untitled":
                self.save_new_file()
            else:
                with open(self.current_file.name, 'r+', encoding='utf-8') as f:
                    current_text = self.text_field.get("1.0", tk.END).strip()
                    f.write(current_text)

    def save_new_file(self):
        """Lets the user save a newly created file.

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
                self.switch_tabs(f)

    def close_file(self, closing: bool, raw_file):
        """Allows the user to close a file.

        Key arguments:
        closing -- Boolean
        raw_file -- the file object
        """
        # If the user is closing the current tab
        if self.current_file == raw_file:
            pass
        elif self.current_file != raw_file or closing:
            file_reference_to_close = None  # To hold a dictionary
            for file_reference in self.files_in_tab:
                if file_reference["file"] == raw_file:
                    file_reference_to_close = file_reference

            file_to_close = file_reference_to_close["file"]

            if file_to_close.name[0:8] == "Untitled":  # If not saved
                with open(file_to_close.name, "r+", encoding="utf-8") as f:
                    if f.read().strip() != "":  # If there is text
                        self.display_text(f)
                        file_to_save = filedialog.asksaveasfile(
                            mode='w',
                            defaultextension=".txt",
                            title=f.name,
                            initialfile="s_"+f.name
                        )

                        if file_to_save is not None:  # If user wants to save
                            with open(
                                file_to_save.name,
                                "r+",
                                encoding="utf-8"
                            ) as save_f:
                                save_f.write(
                                    self.text_field.get('1.0', tk.END).strip()
                                )
                            os.remove(file_to_close.name)
                            file_reference_to_close["tab"].pack_forget()
                            self.files_in_tab.remove(file_reference_to_close)
                            self.display_text(self.current_file)
                        elif file_to_save is None:
                            pass

                        if closing:
                            self.display_text(self.current_file)
                    else:  # If the untitled file is empty
                        os.remove(file_to_close.name)
                        file_reference_to_close["tab"].pack_forget()
                        self.files_in_tab.remove(file_reference_to_close)
            else:  # If it is not called 'Untitled'
                os.remove(file_reference_to_close.name)
                file_reference_to_close["tab"].pack_forget()
                self.files_in_tab.remove(file_reference_to_close)

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
        if tab_file == self.current_file:
            pass
        else:
            # Reconfigure colors to show the current file in use
            self.focus_tabs(tab_file)

            # Saves the replaced text, if any
            if self.current_file is not None:
                self.save_file()
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


class FileButton(ttk.Button):
    def __init__(self, app, raw_file):
        displayed_name = os.path.basename(raw_file.name)
        super().__init__(
            app,
            style="File.TButton",
            text=displayed_name,
            command=lambda: app.switch_tabs(raw_file)
        )
        self.raw_file = raw_file
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.config(width=len(displayed_name))
        self.bind(
            '<Button-2>',  # Right click
            lambda event: app.close_file(False, self.raw_file)
        )


root = tk.Tk()
text_editor = TextEditor(master=root)

# Window settings
text_editor.master.title("Notepad^")
text_editor.master.geometry("900x700")
text_editor.master.iconbitmap('icons/Notepad.ico')

root.mainloop()  # Start the program
