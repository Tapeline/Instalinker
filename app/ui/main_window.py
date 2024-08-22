import os.path
import tkinter

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from ttkbootstrap.dialogs.dialogs import Messagebox

from app.domain.repo import InstallsRepository


class MainWindow(ttk.Window):
    def __init__(self, repo, installs_dir):
        super().__init__()
        self._repo: InstallsRepository = repo
        self._installs_dir = installs_dir
        self._setup_ui()

    def _setup_ui(self):
        self.title("Instalinker")
        self.geometry("600x400")
        self._add_program_button = ttk.Button(
            self,
            text="Add program",
            bootstyle="primary",
            command=self._handle_add_program
        )
        self._remove_program_button = ttk.Button(
            self,
            text="Remove program",
            bootstyle="warning",
            command=self._handle_remove_program
        )
        self._install_program_button = ttk.Button(
            self,
            text="Install program",
            bootstyle="success",
            command=self._handle_install_program
        )
        self._uninstall_program_button = ttk.Button(
            self,
            text="Uninstall program",
            bootstyle="danger",
            command=self._handle_uninstall_program
        )
        self._program_names_var = tkinter.Variable(value=self._repo.get_program_names())
        self._program_list = tkinter.Listbox(
            self,
            listvariable=self._program_names_var
        )
        self._add_program_button.pack()
        self._remove_program_button.pack()
        self._install_program_button.pack()
        self._uninstall_program_button.pack()
        self._program_list.pack()

    def _handle_add_program(self):
        program_file = filedialog.askopenfilename(
            defaultextension=".exe",
            filetypes=[("Executable", (".exe", ".cmd", ".bat", ".ps1"))]
        )
        if program_file is None:
            return
        program_name = ttk.Querybox.get_string(
            "Enter program name", "Adding program",
            os.path.basename(program_file).split(".")[0]
        )
        if program_name is None:
            return
        try:
            self._repo.add_program(program_name, program_file)
        except Exception as e:
            Messagebox.show_error(str(e), "Error occurred")
        self._program_names_var.set(self._repo.get_program_names())

    def _handle_install_program(self):
        zip_file = filedialog.askopenfilename(
            defaultextension=".zip",
            filetypes=[("Zip File", (".zip",))]
        )
        if zip_file is None:
            return
        program_name = ttk.Querybox.get_string(
            "Enter program name", "Adding program",
            os.path.basename(zip_file).split(".")[0]
        )
        if program_name is None:
            return
        self._repo.install_from_zip(
            program_name, zip_file, self._installs_dir,
            lambda directory: filedialog.askopenfilename(
                defaultextension=".exe",
                filetypes=[("Executable", (".exe", ".cmd", ".bat", ".ps1"))],
                initialdir=directory
            )
        )
        self._program_names_var.set(self._repo.get_program_names())

    def _handle_remove_program(self):
        sel = self._program_list.curselection()
        if len(sel) != 1:
            Messagebox.show_error("Select one program!")
            return
        program_name = self._program_list.get(sel[0])
        ans = Messagebox.yesno("Do you want to remove program?\n"
                               "(this will only remove it from list\n"
                               "and start menu. Directory won't be deleted)")
        if ans.lower() == "yes":
            self._repo.remove_program(program_name)
            self._program_names_var.set(self._repo.get_program_names())

    def _handle_uninstall_program(self):
        sel = self._program_list.curselection()
        if len(sel) != 1:
            Messagebox.show_error("Select one program!")
            return
        program_name = self._program_list.get(sel[0])
        ans = Messagebox.yesno("Do you want to remove program?\n"
                               "(this will remove it from list\n"
                               "and start menu AND DIRECTORY WILL BE DELETED)")
        if ans.lower() == "yes":
            self._repo.uninstall_program(program_name)
            self._program_names_var.set(self._repo.get_program_names())
