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


def reorder(file_type ,downloads_path: Path):
    if not downloads_path.exists() or not downloads_path.is_dir():
        return

    destination = downloads_path / file_type[1:]
    ensure_dir(destination)

    for entry in downloads_path.iterdir():
        if entry.is_file() and entry.suffix.lower() == file_type:
            target = destination / entry.name
            shutil.move(entry, target)


if __name__ == "__main__":
    downloads = get_downloads_dir()
    reorder(".zip",downloads)
    reorder(".pdf",downloads)
    reorder(".blend",downloads)
    reorder(".png",downloads)


    if downloads.exists():
        print(f"Downloads directory: {downloads}")
    else:
        print("Downloads directory not found.")
        print(f"Suggested location: {downloads}")
