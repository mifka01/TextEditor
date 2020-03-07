import tkinter as tk
from tkinter import ttk
import os


FOREGROUND_COLOR = "#282828"
BACKGROUND_COLOR = "white"


class TextEditor(tk.Frame):
    files_in_tab = []
    indexes = []
    buttons = []

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.new_file()

        # Defining white bg and black fg style for ttk
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            foreground="black",
            background="white"
        )

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
            font=('MS Reference Sans Serif', 10)
        )

        style.configure(
            'Current.File.TButton',
            font=('MS Reference Sans Serif', 10),
            background=FOREGROUND_COLOR,
            foreground=BACKGROUND_COLOR
        )

    def create_widgets(self):
        # Initialize text_canvas
        text_canvas = tk.Canvas(self.master)
        text_canvas['bg'] = BACKGROUND_COLOR
        text_canvas['highlightthickness'] = "0"
        text_canvas.place(relx=0, rely=0.05, relwidth=1, relheight=1)

        self.text_field = tk.Text(text_canvas)
        self.text_field['border'] = '0'
        self.text_field['fg'] = FOREGROUND_COLOR
        # self.text_field['font'] = textFont
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
            command=self.openFile
            )
        open_button.pack(side=tk.RIGHT, fill=tk.Y)
        open_button.config(width=len(open_button['text']))

        # Initialize save_button
        save_button = ttk.Button(
            self,
            style="TButton",
            text='save',
            command=self.saveManual
        )
        save_button.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        save_button.config(width=len(save_button['text']))

    def openFile(self):
        file_to_open = tk.filedialog.askopenfile(
            parent=self.master,
            mode='r+'
        )
        entry = True
        for file_in_tab in self.files_in_tab:
            if file_in_tab is not None:
                if file_in_tab.name == file_to_open.name:
                    entry = False
            else:
                pass

        if file_to_open is not None and entry:
            self.files_in_tab.append(file_to_open)
            self.buttons.append(
                FileButton(self.files_in_tab.index(file_to_open))
            )
            self.displayText(
                self.files_in_tab.index(file_to_open), self.self.indexes
            )
            file_to_open.close()

        print(file_to_open.name)

    def new_file(self):
        f = open(
            "Untitled-" + str(len(self.files_in_tab)) + ".txt",
            "w+",
            encoding='utf-8'
        )
        self.files_in_tab.append(f)
        self.buttons.append(FileButton(self, self.files_in_tab.index(f)))
        self.displayText(self.files_in_tab.index(f), self.indexes)
        f.close()

    def hideButton(self):
        self.buttons[self.indexes[len(self.indexes)-1]].pack_forget()

    def saveManual(self):
        buttonIndex = self.indexes[len(self.indexes)-1]
        if self.files_in_tab[buttonIndex] is not None:
            if self.files_in_tab[buttonIndex].name[0:8] == "Untitled":
                self.saveNewFile()
            else:
                f = open(
                    f"{self.files_in_tab[buttonIndex].name}",
                    'r+',
                    encoding='utf-8'
                )
                f.write(self.text_field.get("1.0", tk.END).strip())
                f.close()
        else:
            pass

    def saveNewFile(self):
        f = tk.filedialog.asksaveasfile(
            mode='w',
            defaultextension=".txt",
            initialfile="s_" + self.files_in_tab[
                self.indexes[len(self.indexes) - 1]
            ].name
        )
        file = open(f.name, "r+", encoding="utf-8")
        if file is not None:
            oldIndex = self.indexes[len(self.indexes)-1]

            os.remove(self.files_in_tab[oldIndex].name)
            self.buttons[oldIndex].pack_forget()
            self.files_in_tab[oldIndex] = None
            self.buttons[oldIndex] = None
            self.files_in_tab.append(file)
            self.buttons.append(FileButton(self.files_in_tab.index(file)))
            file.write(self.text_field.get('1.0', tk.END).strip())
            file.close()
            self.displayText(self.files_in_tab.index(file), self.indexes)

    def closeFile(self, closing, index):

        # If the user is closing the current tab
        if self.current_file == self.files_in_tab[
            self.buttons[index].main_index
        ]:
            pass

        if self.current_file != self.files_in_tab[
            self.buttons[index].main_index
        ] or closing:
            for file, button in zip(self.files_in_tab, self.buttons):
                if self.files_in_tab.index(file) == index:

                    if self.files_in_tab[index].name[0:8] == "Untitled":
                        file = open(
                            self.files_in_tab[index].name,
                            "r+",
                            encoding="utf-8"
                        )
                        if file.read().strip() != "":  # If there is text
                            self.displayText(index, self.indexes)
                            f = tk.filedialog.asksaveasfile(
                                mode='w',
                                defaultextension=".txt",
                                title=self.files_in_tab[index].name,
                                initialfile="s_"+self.files_in_tab[index].name
                            )

                            if f is not None:
                                file = open(f.name, "r+", encoding="utf-8")
                                file.write(
                                    self.text_field.get('1.0', tk.END).strip()
                                )
                                file.close()
                                os.remove(self.files_in_tab[index].name)
                                self.buttons[index].pack_forget()
                                self.files_in_tab[index] = None
                                self.buttons[index] = None
                                self.displayText(
                                    self.indexes[len(self.indexes)-2],
                                    self.indexes
                                )
                            if closing:
                                self.displayText(
                                    self.indexes[len(self.indexes)-2],
                                    self.indexes
                                )
                            if f is None:
                                break
                        else:
                            file.close()
                            os.remove(self.files_in_tab[index].name)
                            self.buttons[index].pack_forget()
                            self.files_in_tab[index] = None
                            self.buttons[index] = None
                    else:
                        file.close()
                        self.buttons[index].pack_forget()
                        self.files_in_tab[index] = None
                        self.buttons[index] = None
                        print(self.indexes)
                        self.displayText(
                            self.indexes[len(self.indexes)-1], self.indexes
                        )

    def autoSave(self):

        if self.files_in_tab[self.indexes[len(self.indexes)-2]] is not None:
            f = open(
                f"{self.files_in_tab[self.indexes[len(self.indexes)-2]].name}",
                'r+',
                encoding='utf-8'
            )
            f.write(self.text_field.get("1.0", tk.END).strip())
            f.close()
        else:
            pass

    def displayText(self, index, indexes):

        self.indexes.append(index)
        # Recreates the list such that there are no repeating indexes
        self.indexes = [indexes[i] for i in range(len(indexes)) if (
                        i == 0) or indexes[i] != indexes[i-1]]

        for otherButton in self.buttons:
            if otherButton is not None:
                otherButton.configure(style="File.TButton")
            else:
                pass
        if self.buttons[index] is not None:
            self.buttons[index].configure(style="Current.File.TButton")
        else:
            pass

        self.current_file = self.buttons[index]

        self.autoSave()

        self.text_field.delete('1.0', tk.END)
        if self.files_in_tab[index] is not None:
            f = open(f'{self.files_in_tab[index].name}', "r+", encoding="utf-8")
            text = f.read()

            self.text_field.insert('1.0', text)
            f.close()
        else:
            pass


class FileButton(ttk.Button):
    def __init__(self, app, index):
        super().__init__(
            app,
            style="File.TButton",
            text=os.path.basename(app.files_in_tab[index].name),
            command=lambda: self.displayText(index, self.indexes)
        )
        self.main_index = index
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.config(width=len(os.path.basename(app.files_in_tab[index].name)))
        self.bind('<Button-3>', lambda event: self.closeFile(False, index))


root = tk.Tk()
text_editor = TextEditor(master=root)

# Window settings
text_editor.master.title("Notepad^")
text_editor.master.geometry("900x700")
text_editor.master.iconbitmap('icons/Notepad.ico')

root.mainloop()  # Start the program
