from pathlib import Path
import pickle

GIT_IGNORE_FILES = (
    ".DS_Store",
    "cmake-build*",
    "bin/",
    ".idea/",
)

class Manager:
    MANAGER_DB = ".make_build_system"

    def __init__(self, project_path: Path, project_name: str):
        self._project_path = project_path
        self._project_name = project_name
        self._project_db = project_path / Manager.MANAGER_DB
        self._modify_git_ignore()

    def __str__(self):
        return f"{self._project_path}: {self._project_name}"

    def save_manger(self):
        try:
            # TODO: Do hash checking here
            serialized_obj = pickle.dumps(self)
            with self._project_db.open("wb") as handle:
                handle.write(serialized_obj)
        except Exception as error:
            exit(error)

    @classmethod
    def load_manager(cls, project_db: Path):
        try:
            with project_db.open("rb") as handle:
                # TODO: Add has checking here
                obj = handle.read()
                obj = pickle.loads(obj)
                if isinstance(obj, cls):
                    return obj
                else:
                    raise TypeError("Expected pickle object to be of "
                                    f"{cls.__name__} instance. Got {type(obj)}"
                                    " instead")
        except Exception as error:
            exit(error)

    def _modify_git_ignore(self):
        """Create a .gitignore or update it with the binary"""
        git_ignore = None
        build_entry = False

        # Check if there is a .gitignore file
        for file in self._project_path.iterdir():
            if file.name == ".gitignore":
                git_ignore = file

        # Create a default .gitignore if it does not exist
        if git_ignore is None:
            git_ignore = self._project_path / ".gitignore"
            with git_ignore.open("wt", encoding="UTF-8") as handle:
                for file_path in GIT_IGNORE_FILES:
                    handle.write(file_path + "\n")
                handle.write(Manager.MANAGER_DB + "\n")
                build_entry = True

        else:
            # If gitignore already exists, ensure that the build is in there
            with git_ignore.open("rt", encoding="UTF-8") as handle:
                for entry in handle:
                    if entry == Manager.MANAGER_DB:
                        build_entry = True

        # If build is not in the entries, add it
        if not build_entry:
            with git_ignore.open("rt", encoding="UTF-8") as handle:
                handle.write(Manager.MANAGER_DB + "\n")






