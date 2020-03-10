import tkinter as tk
from tkinter.font import Font as tk_font
from tkinter import filedialog
import os


# Variables -- check
files = []
indexes = []
buttons = []

# Colors
fgColor = "#282828"
bgColor = "white"

# Window Settings
root = tk.Tk()
root.title("Notepad^")
root.geometry("900x700")
root.iconbitmap('icons/Notepad.ico')


# Fonts -- check
buttonFont = tk_font(family='Microsoft Sans Serif', size=10)
titleFont = tk_font(family='Georgia', size=30, weight="bold")
textFont = tk_font(family='Microsoft Sans Serif', size=14)

# Canvases
textCanvas = tk.Frame(root)
textCanvas['bg'] = bgColor
textCanvas['highlightthickness'] = "0"
textCanvas.place(relx=0, rely=0.05, relwidth=1, relheight=1)

buttonCanvas = tk.Frame(root)
buttonCanvas['bg'] = bgColor
buttonCanvas['highlightthickness'] = "0"
buttonCanvas.place(relx=0, rely=0, relwidth=1, relheight=0.05)


# Classes


class FileButton(tk.Button):
    def __init__(self, index):
        super().__init__(buttonCanvas)
        self['bg'] = bgColor
        self['text'] = os.path.basename(files[index].name)
        self['fg'] = fgColor
        self['border'] = '0'
        self["font"] = buttonFont
        self['command'] = lambda: displayText(index, indexes)
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.config(width=len(os.path.basename(files[index].name)))
        self.bind('<Button-3>', lambda event: closeFile(False, index))


class TextField(tk.Text):
    def __init__(self):
        super().__init__(textCanvas)
        # Settings
        self['border'] = '0'
        self['fg'] = fgColor
        self['font'] = textFont
        self['wrap'] = tk.WORD
        self['insertbackground'] = fgColor
        self['selectbackground'] = fgColor
        self['selectborderwidth'] = "20px"
        self['state'] = 'normal'
        self['padx'] = '60'
        self['pady'] = '20'
        self.bind("<Control-e>", title)
        self.bind("<Control-r>", color)
        self.bind("<Control-v>", paste)
        self.bind("<Control-d>", textReset)
        self.pack(fill=tk.BOTH, expand=True)

# Methods


def openFile():
    file = filedialog.askopenfile(parent=root, mode='r+')
    entry = True
    for x in files:
        if x is not None:
            if x.name == file.name:
                entry = False
        else:
            pass

    if file is not None and entry:
        files.append(file)
        buttons.append(FileButton(files.index(file)))
        displayText(files.index(file), indexes)
        file.close()


def createNewFile():
    f = open("Untitled-" + str(len(files)) + ".txt", "w+", encoding='utf-8')
    files.append(f)
    buttons.append(FileButton(files.index(f)))
    displayText(files.index(f), indexes)
    f.close()


def hideButton():
    buttons[indexes[len(indexes)-1]].pack_forget()


def saveManual():
    buttonIndex = indexes[len(indexes)-1]
    if files[buttonIndex] is not None:
        if files[buttonIndex].name[0:8] == "Untitled":
            saveNewFile()
        else:
            f = open(f"{files[buttonIndex].name}", 'r+', encoding='utf-8')
            f.write(textField.get("1.0", tk.END).strip())
            f.close()
    else:
        pass


def saveNewFile():
    f = tk.filedialog.asksaveasfile(
        mode='w', defaultextension=".txt",
        initialfile="s_"+files[indexes[len(indexes)-1]].name)
    file = open(f.name, "r+", encoding="utf-8")
    if file is not None:

        oldIndex = indexes[len(indexes)-1]

        os.remove(files[oldIndex].name)
        buttons[oldIndex].pack_forget()
        files[oldIndex] = None
        buttons[oldIndex] = None
        files.append(file)
        buttons.append(FileButton(files.index(file)))
        file.write(textField.get('1.0', tk.END).strip())
        file.close()
        displayText(files.index(file), indexes)


def closeFile(closing, index):

    if buttons[index]["bg"] == fgColor:
        pass

    if buttons[index]["bg"] == bgColor or closing:

        for file, button in zip(files, buttons):
            if files.index(file) == index:

                if files[index].name[0:8] == "Untitled":
                    file = open(files[index].name, "r+", encoding="utf-8")
                    if file.read().strip() != "":
                        displayText(index, indexes)
                        f = tk.filedialog.asksaveasfile(
                            mode='w', defaultextension=".txt",
                            title=files[index].name,
                            initialfile="s_"+files[index].name)

                        if f is not None:
                            file = open(f.name, "r+", encoding="utf-8")
                            file.write(textField.get('1.0', tk.END).strip())
                            file.close()
                            os.remove(files[index].name)
                            buttons[index].pack_forget()
                            files[index] = None
                            buttons[index] = None
                            displayText(indexes[len(indexes)-2], indexes)
                        if closing:

                            displayText(indexes[len(indexes)-2], indexes)
                        if f is None:
                            break
                    else:
                        file.close()
                        os.remove(files[index].name)
                        buttons[index].pack_forget()
                        files[index] = None
                        buttons[index] = None
                else:
                    file.close()
                    buttons[index].pack_forget()
                    files[index] = None
                    buttons[index] = None
                    print(indexes)
                    displayText(indexes[len(indexes)-1], indexes)


def autoSave():
    if files[indexes[len(indexes)-2]] is not None:
        f = open(f"{files[indexes[len(indexes)-2]].name}",
                 'r+', encoding='utf-8')
        f.write(textField.get("1.0", tk.END).strip())
        f.close()
    else:
        pass


def displayText(index, indexes):

    indexes.append(index)
    indexes = [indexes[i] for i in range(len(indexes)) if (
        i == 0) or indexes[i] != indexes[i-1]]

    for otherButton in buttons:
        if otherButton is not None:
            otherButton['bg'] = bgColor
            otherButton['fg'] = fgColor
        else:
            pass
    if buttons[index] is not None:
        buttons[index]['bg'] = fgColor
        buttons[index]['fg'] = bgColor
    else:
        pass

    autoSave()

    textField.delete('1.0', tk.END)
    if files[index] is not None:

        f = open(f'{files[index].name}', "r+", encoding="utf-8")
        text = f.read()

        textField.insert('1.0', text)
        f.close()
    else:
        pass


# Shortcuts
def paste(event):
    tk.Entry.event_delete(textField, "<<Paste>>")
    tk.Entry.event_generate(textField, '<<Paste>>')
    textField.see(tk.END)


def color(event):

    if textField.tag_ranges("sel"):
        textField.tag_add("color", "sel.first", "sel.last")
        textField.tag_config("color", foreground="#8A2BE2")
    else:
        word_start = textField.index("insert-1c wordstart")
        word_end = textField.index("insert")
        textField.tag_add('color', word_start, word_end)
        textField.tag_config("color", foreground="#8A2BE2")


def textReset(event):
    if textField.tag_ranges("sel"):
        textField.tag_add("color", "sel.first", "sel.last")
        textField.tag_config("color", foreground="black")

        textField.tag_add("nadpis", "sel.first", "sel.last")
        textField.tag_config("nadpis", font=textFont)
    else:
        textField.tag_add('color', "insert-1c wordstart", "insert")
        textField.tag_config("color", foreground="black")

        textField.tag_add('nadpis', "insert linestart", "insert")
        textField.tag_config("nadpis", font=textFont)


def title(event):
    if textField.tag_ranges("sel"):
        textField.tag_add("nadpis", "sel.first", "sel.last")
        textField.tag_config("nadpis", font=titleFont)

    if not textField.tag_ranges("sel"):
        cur_cursor = textField.index("insert")
        line_start = textField.index("insert-1c linestart")
        textField.tag_add('nadpis', line_start, cur_cursor)
        textField.tag_config("nadpis", font=titleFont)


def ctrlS(event):
    saveManual()


def ctrlO(event):
    openFile()


def ctrlN(event):
    createNewFile()


def ctrlQ(event):
    for x in files:
        if x is not None:
            if x.name[0:8] == "Untitled":
                closeFile(True, files.index(x))

        else:
            pass
    root.quit()


def leftFile(event):
    currentButton = indexes[len(indexes)-1]
    workingButtons = [i for i, x in enumerate(buttons) if x is not None]
    nextButtonIndex = workingButtons.index(currentButton)-1

    if nextButtonIndex >= 0:
        displayText(workingButtons[nextButtonIndex], indexes)


def rightFile(event):
    currentButton = indexes[len(indexes)-1]
    workingButtons = [i for i, x in enumerate(buttons) if x is not None]
    nextButtonIndex = workingButtons.index(currentButton)+1

    if nextButtonIndex <= len(workingButtons)-1:
        displayText(workingButtons[nextButtonIndex], indexes)


# Static parts
textField = TextField()

plusButton = tk.Button(buttonCanvas)
plusButton['bg'] = bgColor
plusButton['text'] = '+'
plusButton['fg'] = fgColor
plusButton['border'] = '0'
plusButton["font"] = tk_font(family='MS Reference Sans Serif', size=20)
plusButton['command'] = createNewFile
plusButton.pack(side=tk.LEFT, fill=tk.Y)
plusButton.config(width=3)

openButton = tk.Button(buttonCanvas)
openButton['bg'] = bgColor
openButton['text'] = 'open'
openButton['fg'] = fgColor
openButton['border'] = '0'
openButton["font"] = tk_font(family='MS Reference Sans Serif', size=15)
openButton['command'] = openFile
openButton.pack(side=tk.RIGHT, fill=tk.Y)
openButton.config(width=len(openButton['text']))


saveButton = tk.Button(buttonCanvas)
saveButton['bg'] = bgColor
saveButton['text'] = 'save'
saveButton['fg'] = fgColor
saveButton['border'] = '0'
saveButton["font"] = tk_font(family='MS Reference Sans Serif', size=15)
saveButton['command'] = saveManual
saveButton.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
saveButton.config(width=len(saveButton['text']))


# Binds
root.bind('<Control-s>', ctrlS)
root.bind('<Control-o>', ctrlO)
root.bind('<Control-q>', ctrlQ)
root.bind('<Control-n>', ctrlN)
root.bind('<Control-Left>', leftFile)
root.bind('<Control-Right>', rightFile)
root.protocol("WM_DELETE_WINDOW", lambda: ctrlQ(""))


# Loop
createNewFile()
root.mainloop()
