from zipfile import ZipFile
from datetime import datetime
from src.config import config, PATHS
import shutil


def create_zip_from_processed():
    source_dir = PATHS["processed_review"]
    output_dir = PATHS["ready_to_send"]

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{config['naming']['zip_prefix']}_{timestamp}.zip"
    zip_path = output_dir / zip_name

    files = [file for file in source_dir.iterdir() if file.is_file()]

    if not files:
        print("[ZIP] No files found to zip.")
        return None, []

    with ZipFile(zip_path, "w") as zipf:
        for file in files:
            zipf.write(file, arcname=file.name)

    print(f"[ARCHIVE] Moved {len(files)} file(s) to sent_archive")
    return zip_path, files


def archive_processed_files(files):
    archive_dir = PATHS["sent_archive"]
    archive_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        destination = archive_dir / file.name
        shutil.move(str(file), str(destination))

    print(f"[ARCHIVE] Moved {len(files)} file(s) to sent_archive")