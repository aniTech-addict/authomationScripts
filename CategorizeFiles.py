from pathlib import Path
import re
import shutil

def get_downloads_dir():
    home = Path.home()
    xdg_config = home / ".config" / "user-dirs.dirs"

    if xdg_config.exists():
        content = xdg_config.read_text()
        match = re.search(r'XDG_DOWNLOAD_DIR="(.+)"', content)
        if match:
            path = match.group(1).replace("$HOME", str(home))
            return Path(path)

    return home / "Downloads"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def reorder(downloads_path: Path, file_type: str, files_moved: list):
    if not downloads_path.exists() or not downloads_path.is_dir():
        return

    destination = downloads_path / file_type.lstrip(".")
    ensure_dir(destination)

    for entry in downloads_path.iterdir():
        if entry.is_file() and entry.suffix.lower() == file_type.lower():
            target = destination / entry.name
            shutil.move(entry, target)
            files_moved[0] += 1


def get_file_types(path: Path):
    file_types = set()
    for entry in path.iterdir():
        if entry.is_file() and entry.suffix:
            file_types.add(entry.suffix.lower())
    return file_types


if __name__ == "__main__":
    downloads = get_downloads_dir()
    ensure_dir(downloads)

    file_types = get_file_types(downloads)
    files_moved = [0]  # mutable counter

    for file_type in file_types:
        reorder(downloads, file_type, files_moved)

    print("Reordering Completed")
    print("Number of files moved =", files_moved[0])
