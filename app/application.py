import json
import os.path

from app import serialization
from app.domain.repo import InstallsRepository
from app.ui.main_window import MainWindow


class Application:
    def __init__(self, config_path="config.yml"):
        self._config = {}
        self._config_path = config_path
        self._load_config()
        self._installs_dir = self._config["installs_dir"]
        self._repo = self._init_repo()
        self._main_window = None

    def _load_config(self):
        if not os.path.exists(self._config_path):
            with open(self._config_path, "w") as f:
                f.write("{\"installs_dir\": \"D:\\\\Programs\", \"programs\": {}}")
        with open(self._config_path, "r") as f:
            self._config = json.loads(f.read())

    def _init_repo(self):
        _repo = InstallsRepository()
        _repo.set_programs(serialization.deserialize_repo(self._config["programs"]))
        return _repo

    def _save_config(self):
        self._config["programs"] = serialization.serialize_repo(self._repo.get_programs())
        with open(self._config_path, "w") as f:
            f.write(json.dumps(self._config))

    def run(self):
        self._main_window = MainWindow(self._repo, self._installs_dir)
        self._main_window.mainloop()
        self._save_config()
