import tkinter as tk
from tkinter import Tk, ttk, filedialog, messagebox
import os
import sys


class Notepad():
    __root = Tk()
    __Menu = tk.Menu()
    __url = False
    __changed = False
    __icon = tk.PhotoImage('notepad.ICO')
    __width = 800
    __height = 600

    def __init__(self):
        self.__root.iconbitmap(self.__icon)
        self.__root.geometry(f'{self.__width}x{self.__height}')
        self.settitleapp()

        self.__filemenu = tk.Menu(self.__Menu, tearoff=False)

        self.__filemenu.add_command(
            label='New', accelerator='CTRL+N', command=self.newfile)
        self.__filemenu.add_command(
            label='Open', accelerator='CTRL+O', command=self.openfile)
        self.__filemenu.add_command(
            label='Save', accelerator='CTRL+S', command=self.savefile)
        self.__filemenu.add_command(
            label='Save as', accelerator='CTRL+ALT+S', command=self.saveasfile)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(
            label='Exit', accelerator='CTRL+Q', command=self.exitapp)

        self.__editmenu = tk.Menu(self.__root, tearoff=False)
        self.__editmenu.add_command(label='Pase', accelerator='CTRL+V',
                                    command=lambda: self.__root.event_generate('<Control v>'))
        self.__editmenu.add_command(label='Copy', accelerator='CTRL+C',
                                    command=lambda: self.__root.event_generate('<Control c>'))
        self.__editmenu.add_command(label='Cut', accelerator='CTRL+X',
                                    command=lambda: self.__root.event_generate('<Control x>'))

        self.__helpmenu = tk.Menu(self.__root, tearoff=False)
        self.__helpmenu.add_command(label='Help', accelerator='F1')
        self.__Menu.add_cascade(label='File', menu=self.__filemenu)
        self.__Menu.add_cascade(label='Edit', menu=self.__editmenu)
        self.__Menu.add_cascade(label='Help', menu=self.__helpmenu)

        self.__scrollbar = tk.Scrollbar(self.__root, orient='vertical')
        self.__scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        self.__editor = tk.Text(self.__root)
        self.__editor.pack(fill=tk.BOTH, expand=True)
        self.__editor.config(wrap='word', relief=tk.FLAT)

        self.__editor.configure(yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.configure(command=self.__editor.yview())

        self.__root.config(menu=self.__Menu)

        self.__root.bind('<Control-n>', self.newfile)
        self.__root.bind('<Control-o>', self.openfile)
        self.__root.bind('<Control-s>', self.savefile)
        self.__root.bind('<Control-Alt-s>', self.saveasfile)
        self.__root.bind('<Control-q>', self.exitapp)
        self.__editor.bind('<Button3-ButtonRelease>', self.rightclick)
        self.__editor.bind('<<Modified>>', self.editormodified)

    def editormodified(self, event=None):
        if self.__url:
            content = self.__editor.get(1.0, 'end-1c')
            with open(self.__url, 'r') as fr:
                contentfile = fr.read()
                if content == contentfile:
                    self.__changed = False
                else:
                    self.__changed = True
        elif len(self.__editor.get(1.0, tk.END)) > 1:
            self.__changed = True
        elif len(self.__editor.get(1.0, tk.END)) <= 1:
            self.__changed = False
        self.__editor.edit_modified(False)

    def openfile(self, event=None):
        self.__url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select a file', filetypes=(
            ('Text File', '*.txt'), ('All file', '*.*')), defaultextension='.txt')
        try:
            with open(self.__url, 'r') as fr:
                self.__editor.delete(1.0, tk.END)
                self.__editor.insert(1.0, fr.read())
            self.settitleapp()
            self.__changed = False
        except FileNotFoundError as err:
            return

    def newfile(self, event=None):
        self.__url = False
        self.__editor.delete(1.0, tk.END)
        self.settitleapp()

    def savefile(self, event=None):
        if self.__url:
            content = self.__editor.get(1.0, tk.END)
            with open(self.__url, 'w', encoding='utf-8') as fw:
                fw.write(content)
                self.__changed = False
        else:
            self.saveasfile()

    def saveasfile(self, event=None):
        try:
            self.__url = filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=(
                ('Text File', '*.txt'), ('All File', '*.*')), defaultextension='.txt')
            content = self.__editor.get(1.0, tk.END)
            with open(self.__url, 'w', encoding='utf-8') as fw:
                fw.write(content)
                self.__changed = False
        except FileNotFoundError:
            return

        self.settitleapp()

    def rightclick(self, event):
        self.__editmenu.post(event.x_root, event.y_root)

    def settitleapp(self):
        try:
            title = f'Notepad ({os.path.basename(self.__url)})'
        except TypeError:
            title = 'Notepad'

        self.__root.title(title)

    def start(self):
        self.__root.mainloop()

    def exitapp(self, event=None):
        if self.__changed:
            msg = messagebox.askyesnocancel(
                'Warning', 'Do you want to save the file?')
            if msg is True:
                self.savefile()
            else:
                self.__root.destroy()
        else:
            self.__root.destroy()
