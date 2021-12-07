from pathlib import Path
from sys import argv


def make_component(project_path: Path,
                   component_name: str,
                   executable: bool) -> None:
    # Ensure the project exists
    if not project_path.is_dir():
        raise NotADirectoryError("Project directory does not exist",
                                 project_path.as_posix())

    project_path = project_path.resolve()

    # Attempt to make the component. If it exists, then do not continue
    # processing
    component_dir = project_path / "src" / component_name
    try:
        component_dir.mkdir(parents=True)
    except FileExistsError:
        raise FileExistsError("Project component already exists. Ignoring...")

    # Attempt to make the makefile
    component_file = component_dir / "Makefile"
    with component_file.open("wt", encoding="UTF-8") as handle:
        handle.write(LIBRARY_TEMPLATE.format(component_name=component_name))

    # Attempt to make the c file
    component_file = component_dir / f"{component_name}.c"
    with component_file.open("wt", encoding="UTF-8") as handle:
        handle.write(
            LIBRARY_C_FILE_TEMPLATE.format(
                component_name=component_name
            )
        )

    # Get the header variable based on the c file creation
    index = component_file.parts.index(project_path.name)
    header_var = "_".join(part.upper()
                          for part in component_file.parts[index:-1])

    # Attempt to make the header file
    (project_path / "include").mkdir(exist_ok=True)
    component_file = project_path / "include" / f"{component_name}.h"

    with component_file.open("wt", encoding="UTF-8") as handle:
        handle.write(
            LIBRARY_H_FILE_TEMPLATE.format(header_var=header_var)
        )

    # Create the component dir

    index = (project_path / component_name).parts.index(project_path.name)
    project_root = "/".join(root_makefile.parts[index:])


    # Update or create the root Makefile
    root_makefile = project_path / "Makefile"
    if not root_makefile.is_file():
        with root_makefile.open("wt", encoding="UTF-8") as handle:
            handle.write(
                ROOT_MAKEFILE.format(
                    project_dirs=project_root
            ))



if __name__ == "__main__":
    from constants import LIBRARY_C_FILE_TEMPLATE, LIBRARY_H_FILE_TEMPLATE, \
    LIBRARY_TEMPLATE, ROOT_MAKEFILE

    make_component(Path(argv[1]), argv[2], executable=False)
else:
    from components.constants import LIBRARY_C_FILE_TEMPLATE, \
        LIBRARY_H_FILE_TEMPLATE, LIBRARY_TEMPLATE
