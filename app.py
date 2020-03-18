import tkinter as tk
from platform import system as platform
from TextEditor import TextEditor


root = tk.Tk()
# root['bg'] = BACKGROUND_COLOR
text_editor = TextEditor(master=root)

# Window settings
text_editor.master.title("Notepad^")
text_editor.master.configure(background='white')
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
