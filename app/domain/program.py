StringPath = str


class InstalledProgram:
    def __init__(self,
                 name: str,
                 directory: StringPath,
                 start_menu_link: StringPath,
                 path_env_component: StringPath | None = None):
        self.name = name
        self.directory = directory
        self.path_env_component = path_env_component
        self.start_menu_link = start_menu_link

    @property
    def is_installed_to_path(self):
        return self.path_env_component is not None
