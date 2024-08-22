import os.path
import shutil
import zipfile
from abc import ABC
from typing import Callable

from lnkcreator import create_shortcut

from app.domain.exceptions import ProgramAlreadyAddedException, InvalidPathException
from app.domain.program import InstalledProgram, StringPath


class InstallsRepository(ABC):
    def __init__(self, start_menu: str | None = None):
        self._installs: dict[str, InstalledProgram] = {}
        self._start_menu_path = start_menu or r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"

    def set_programs(self, programs: dict[str, InstalledProgram]):
        self._installs = programs

    def has_program(self, name: str, directory: StringPath) -> bool:
        if name in self._installs:
            return True
        directory = os.path.abspath(directory)
        for prog in self._installs.values():
            if prog.directory == directory:
                return True
        return False

    def get_programs(self) -> dict[str, InstalledProgram]:
        return self._installs

    def get_program_names(self):
        return list(self._installs.keys())

    def _abs_path_and_validate(self, name, exe_path) -> StringPath:
        exe_path = os.path.abspath(exe_path)
        if self.has_program(name, exe_path):
            raise ProgramAlreadyAddedException(exe_path)
        if not os.path.exists(exe_path):
            raise InvalidPathException(exe_path)
        return exe_path

    def _get_directory(self, exe_path) -> StringPath:
        return os.path.abspath(os.path.dirname(exe_path))

    def _create_shortcut(self, name, exe_path):
        shortcut_path = os.path.join(self._start_menu_path, f"{name}.lnk")
        create_shortcut(
            shortcut_path=shortcut_path,
            target=exe_path,
            arguments=[]
        )
        return shortcut_path

    def add_program(self, name: str, executable: StringPath) -> None:
        exe_path = self._abs_path_and_validate(name, executable)
        directory = self._get_directory(exe_path)
        shortcut_path = self._create_shortcut(name, exe_path)
        program = InstalledProgram(name, directory, shortcut_path)
        self._installs[name] = program

    def remove_program(self, name: str) -> None:
        program = self._installs[name]
        os.remove(program.start_menu_link)
        del self._installs[name]

    def uninstall_program(self, name: str) -> None:
        prog = self._installs[name]
        self.remove_program(name)
        shutil.rmtree(prog.directory)

    def install_from_zip(self, name: str, zip_path: StringPath, target_dir: StringPath,
                         exe_choosing_strategy: Callable[[StringPath], StringPath | None]) -> None:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            install_dir = os.path.join(target_dir, name)
            zip_ref.extractall(install_dir)
        exe_file = exe_choosing_strategy(install_dir)
        if exe_file is None:
            return
        self.add_program(name, exe_file)
