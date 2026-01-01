import os
import re
from pathlib import Path
import shutil

def get_screenshots_path():
    home = Path.home()
    xdg_config = home / ".config" / "user-dirs.dirs"

    if xdg_config.exists():
        contents = xdg_config.read_text()
        pictures_path = re.search(r'XDG_PICTURES_DIR="(.+)"', contents)

        if pictures_path:
            path = pictures_path.group(1).replace("$HOME", str(home)) + "/Screenshots"
            screenshots = Path(path)
            if screenshots.exists():
                return screenshots

    raise FileNotFoundError("Screenshots directory not found")


def time_conversion(time):
    hour, minute, sec = map(int, time.split('-'))

    suffix = "AM"
    if hour >= 12:
        suffix = "PM"
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 12

    return f"{hour}:{minute:02d} {suffix} {sec}.png"


def ensure_path(base_path, month):
    destination_path = base_path / month
    destination_path.mkdir(parents=True, exist_ok=True)
    return destination_path


def reorganize_files(path):
    for entry in path.iterdir():
        if not entry.is_file():
            continue

        parts = entry.name.split(" ")
        if len(parts) < 4:
            continue  # not a GNOME screenshot

        month = parts[2][:7]          # 2026-01
        time = parts[3].removesuffix(".png")

        new_name = time_conversion(time)
        renamed_path = entry.with_name(new_name)

        os.rename(entry, renamed_path)

        destination_path = ensure_path(path, month)
        shutil.move(renamed_path, destination_path)


if __name__ == "__main__":
    screenshots_path = get_screenshots_path()
    reorganize_files(screenshots_path)
