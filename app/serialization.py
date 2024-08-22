from app.domain.program import InstalledProgram


def serialize_program(prog: InstalledProgram):
    return {
        "name": prog.name,
        "directory": prog.directory,
        "start_menu": prog.start_menu_link
    }


def deserialize_program(data: dict):
    return InstalledProgram(
        name=data["name"],
        directory=data["directory"],
        start_menu_link=data["start_menu"]
    )


def serialize_repo(programs_dict):
    return {k: serialize_program(v) for k, v in programs_dict.items()}


def deserialize_repo(data: dict):
    return {k: deserialize_program(v) for k, v in data.items()}
