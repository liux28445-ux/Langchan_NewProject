import os


def get_project_root() -> str:

    current_File = os.path.abspath(__file__)

    current_dir = os.path.dirname(current_File)
    project_root = os.path.dirname(current_dir)
    return project_root


def get_abs_path(relative_path:str) -> str:
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)

if __name__ == '__main__':
    print(get_project_root())