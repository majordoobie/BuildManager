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
    CMAKE_FILE_NAME = "CMakeLists.txt"
    CMAKE_DEFAULT = "3.20"
    C_STANDARD = "99"

    def __init__(
            self,
            project_path: Path,
            project_name: str,
            make_version: str = CMAKE_DEFAULT,
            c_standard: str = C_STANDARD
    ):
        self._project_path = project_path
        self._project_name = project_name
        self._project_db = project_path / Manager.MANAGER_DB

        # Compiler defaults
        self._make_version = make_version
        self._c_standard = c_standard

        # Create the git ignore
        self._modify_git_ignore()

        # Instance constants
        self._main_cmake = self._project_path / Manager.CMAKE_FILE_NAME

        # List of files
        self._project_files = []

    def __str__(self):
        return f"Project path:  {self._project_path}\n" \
               f"Project name:  {self._project_name}\n" \
               f"CMake Version: {self._make_version}\n" \
               f"C Standard:    {self._c_standard}\n" \


    def _refactor(self, project_name: str) -> None:
        pass

    def run(self, project_name: str = None) -> None:
        # If a new project name is specified then refactor
        if project_name != self._project_name:
            self._refactor(project_name)

        # if not self._main_cmake.exists():
        #     self._make_cmake_file()

    def save_manger(self):
        """"Save the instance to disk"""
        try:
            # TODO: Do hash checking here
            serialized_obj = pickle.dumps(self)
            with self._project_db.open("wb") as handle:
                handle.write(serialized_obj)
        except Exception as error:
            exit(error)

    @classmethod
    def load_manager(cls, project_db: Path):
        """Load a potential project into memory"""
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

    def _make_cmake_file(self) -> None:
        pass
