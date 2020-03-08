import tkinter as tk
from tkinter.font import Font as tk_font
from app import TextEditor as app


TITLE_FONT = tk_font(family='Georgia', size=30, weight="bold")
TEXT_FONT = tk_font(family='Microsoft Sans Serif', size=14)


def paste(event):
    tk.Entry.event_delete(app.text_field, "<<Paste>>")
    tk.Entry.event_generate(app.text_field, '<<Paste>>')
    app.text_field.see(tk.END)


def color(event):
    if app.text_field.tag_ranges("sel"):
        app.text_field.tag_add("color", "sel.first", "sel.last")
        app.text_field.tag_config("color", foreground="#8A2BE2")
    else:
        word_start = app.text_field.index("insert-1c wordstart")
        word_end = app.text_field.index("insert")
        app.text_field.tag_add('color', word_start, word_end)
        app.text_field.tag_config("color", foreground="#8A2BE2")


def textReset(event):
    if app.text_field.tag_ranges("sel"):
        app.text_field.tag_add("color", "sel.first", "sel.last")
        app.text_field.tag_config("color", foreground="black")

        app.text_field.tag_add("nadpis", "sel.first", "sel.last")
        app.text_field.tag_config("nadpis", font=TEXT_FONT)
    else:
        app.text_field.tag_add('color', "insert-1c wordstart", "insert")
        app.text_field.tag_config("color", foreground="black")

        app.text_field.tag_add('nadpis', "insert linestart", "insert")
        app.text_field.tag_config("nadpis", font=TEXT_FONT)


def title(event):
    if app.text_field.tag_ranges("sel"):
        app.text_field.tag_add("nadpis", "sel.first", "sel.last")
        app.text_field.tag_config("nadpis", font=TITLE_FONT)

    if not app.text_field.tag_ranges("sel"):
        cur_cursor = app.text_field.index("insert")
        line_start = app.text_field.index("insert-1c linestart")
        app.text_field.tag_add('nadpis', line_start, cur_cursor)
        app.text_field.tag_config("nadpis", font=TITLE_FONT)
