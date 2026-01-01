import os 
from pkgutil import walk_packages
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
            return(Path(path))


""" INPUT: string = 24 hours formated time  ///(16-20-04.png) hour-min-sec
    OUTPUT: string = 12 Hours formated time with am/pm suffix after conversion ///4-20 PM 2.png"""
def file_name_conversion(time):
    parts = time.split('-')
    if len(parts) != 3:
        raise ValueError(f"Invalid time format: {time}")
    hour_str, min_str, sec_str = parts
    hour = int(hour_str)
    min = int(min_str)
    sec = int(sec_str)
    if hour == 0:
        display_hour = 12
        suffix = "AM"
    elif hour < 12:
        display_hour = hour
        suffix = "AM"
    elif hour == 12:
        display_hour = 12
        suffix = "PM"
    else:
        display_hour = hour - 12
        suffix = "PM"
    return f"{display_hour}-{min} {suffix} {sec}"
    
def ensure_path(path,month):
    destination_path = Path(path) / month
    destination_path.mkdir(parents=True, exist_ok=True)
    return destination_path

def reorganize_files(path):
    for entry in path.iterdir():
        if entry.is_file():
            parts = entry.name.split()
            if len(parts) >= 4:
                date_str = parts[2]
                time_with_ext = parts[3]
                time_str = time_with_ext.split('.')[0]
                month = date_str.split('-')[1]
                new_filename = file_name_conversion(time_str)

                destination_path = ensure_path(path, month)
                new_file_pathname = entry.with_name(new_filename)
                entry.rename(new_file_pathname)
                shutil.move(str(new_file_pathname), str(destination_path))
            


if __name__ == "__main__":
    
    screenshots_path = get_screenshots_path()
    reorganize_files(screenshots_path)
    

