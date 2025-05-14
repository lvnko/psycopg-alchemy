import os, subprocess

def generate_path_to_file(file_name = None):
    """
    Finds the absolute path to the root directory of the Git repository.

    It works even if the script is executed from a nested subdirectory.

    Returns:
        str or None: The absolute path to the repository root, or None if not found.
    """
    try:
        # Use git rev-parse --show-toplevel to find the repository root
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                             stderr=subprocess.PIPE,
                                             text=True,
                                             encoding='utf-8').strip()
        repo_path = os.path.abspath(repo_root)
        if file_name is None:
            return repo_path
        else:
            return os.path.join(repo_path, file_name)
    except subprocess.CalledProcessError:
        # Handle the case where the script is not inside a Git repository
        return None
    except FileNotFoundError:
        # Handle the case where git is not installed
        return None