from argparse import ArgumentParser, Namespace, ArgumentTypeError
import tempfile
from pathlib import Path


def _valid_path(string) -> Path:
    """
    Ensure that the path provided is a writeable directory

    :param string: String passed to the path arg parser
    :return: Pathlib
    :raises argparse.ArgumentTypeError: If path does not exist or writting to
    it is not permitted
    """
    path = Path(string)

    # If not a directory, bail out
    if not path.is_dir():
        raise ArgumentTypeError("Argument must be a valid directory"
                                " path")

    # Make sure that writing to directory is permitted
    try:
        test_file = tempfile.TemporaryFile(dir=path)
        test_file.close()
    except (OSError, IOError) as error:
        raise ArgumentTypeError(f"{error.strerror}: {path}")

    # Attempt to resolve the full path
    try:
        return path.resolve(strict=True)
    except FileNotFoundError as error:
        raise ArgumentTypeError(f"{error.strerror}: {path}")


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Tool is designed to automate a Makefile build system"
    )

    # path to the project
    parser.add_argument(
        "-p",
        "--project-path",
        help="Path to the project directory. This is where the project json"
             "will be made for the tool.",
        required=True,
        dest="project_path",
        metavar="",
        type=_valid_path
    )

    parser.add_argument(
        "-n",
        "--project-name",
        help="Project name, if not used then the directory name for the "
             "project path will be used.",
        dest="project_name",
        metavar="",
        type=str
    )

    return parser.parse_args()
