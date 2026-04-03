import os
import shutil

def move_file_to_error(saved_file_path, error_dir):
    if not saved_file_path:
        raise ValueError("saved_file_path is required")

    if not os.path.exists(saved_file_path):
        raise FileNotFoundError(f"Source file does not exist: {saved_file_path}")

    os.makedirs(error_dir, exist_ok=True)

    error_filename = os.path.basename(saved_file_path)
    error_file_path = os.path.join(error_dir, error_filename)

    counter = 1
    while os.path.exists(error_file_path):
        base, ext = os.path.splitext(error_filename)
        error_file_path = os.path.join(error_dir, f"{base}_{counter}{ext}")
        counter += 1

    shutil.move(saved_file_path, error_file_path)
    return error_file_path