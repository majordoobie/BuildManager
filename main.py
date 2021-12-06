import json

from components.arg_parse import parse_args, Namespace
from pathlib import Path

from components.project_manager import Manager


def _make_defaults(db: Path, project_path: str, project_name: str) -> None:
    """
    Create the default build json
    {
        "project_path": "path_to_project",
        "project_name": "project_name"

    }
    :param path:
    :return:
    """
    _dict = {
        "project_path": project_path,
        "project_name": project_name
    }
    print(_dict)

    with db.open("wt", encoding="utf-8") as outfile:
        json.dump(_dict, outfile)


def _get_db(project_db: Path) -> dict:
    with project_db.open(encoding="utf-8") as outfile:
        return json.load(outfile)


def main():
    args = parse_args()
    project_path: Path = args.project_path

    # If project name is not used, then use the directory name
    if args.project_name is None:
        args.project_name = project_path.name

    project_db = project_path / Manager.MANAGER_DB
    if not project_db.exists():
        mgr = Manager(project_path, args.project_name)
        mgr.save_manger()

    else:
        mgr = Manager.load_manager(project_db)

    print(mgr)





if __name__ == '__main__':
    main()

