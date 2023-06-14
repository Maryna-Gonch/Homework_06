import sys
import shutil
from pathlib import Path
import uuid
from normalize import normalize

CATEGORIES = {"images": [".jpg", ".gif", ".png", ".jpeg", ".svg"],
              "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
              "audio": [".mp3", ".ogg", ".aiff", ".wav", ".amr"],
              "video": [".avi", ".mp4", ".mov", ".mkv"],
              "archives": [".zip", ".rar", ".gz", ".tar"]}


def move_file(path: Path, root_dir: Path, categorie: str):
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(
            f"{new_name.stem}-{uuid.uuid4()}{path.suffix}")
    path.replace(new_name)


def get_categories(path: Path):
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "other"


def sort_folder(path: Path):
    for item in path.glob("**/*"):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def delete_emppty_folders(path):
    for item in path.glob("**/*"):
        if item.is_dir() and (not item.name in CATEGORIES.keys()) and (item.name != "other"):
            shutil.rmtree(path.joinpath(item))


def upack_archive(path):
    for item in path.joinpath("archives").iterdir():
        try:
            shutil.unpack_archive(
                str(item), path.joinpath(f"archives/{item.stem}"))
        except Exception:
            print(f"Can't unpack {item.name}")


def print_result(path):
    for cat in ("images", "documents", "audio", "video", "archives"):
        print(f"FIle of category {cat}:")
        lst = []
        if path.joinpath(cat).exists():
            for item in path.joinpath(cat).iterdir():
                if item.is_file():
                    print(item.name)
                    lst.append(item.suffix)
            print(f"Extensions of {cat}: {set(lst)}\n")
        else:
            print(f"Category {cat} is empty\n")

    if path.joinpath("other").exists():
        lst = [item.suffix for item in path.joinpath("other").iterdir()]
        print(f"Unknown extensions: {set(lst)}\n")
    else:
        print(f"Not found unknown extensions\n")


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    if not path.exists():
        return f"Folder with path {path} doesn't exist"
    sort_folder(path)
    delete_emppty_folders(path)
    upack_archive(path)
    print_result(path)
    return "Ok"


if __name__ == "__main__":
    print(main())
