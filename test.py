import ast
import tkinter as tk
import tkinter.font as font



root = tk.Tk()
root.geometry("900x700")


textField = tk.Text(root)
textField.pack()


def openfile():
    f = open("Photosythesis.txt", "r+")

    
    text = f.read()
    print(text.strip())
    textField.insert("1.0",text)
    
    
    f.close()
def save():
    f = open("Photosythesis.txt", "r+")
    text = textField.get("1.0",tk.END)
    f.write(text)
    
    f.close()

but  = tk.Button(root)
but.pack()
but['command'] = save




openfile()
root.mainloop()

