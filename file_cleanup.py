import os
import time

def cleanup_old_files(folder_path, age_limit_minutes=10):
    
    current_time = time.time()
    deleted_files = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_age = (current_time - os.path.getmtime(file_path)) / 60  # in minutes
            if file_age > age_limit_minutes:
                os.remove(file_path)
                deleted_files.append(filename)

    if deleted_files:
        print(f"Deleted old files from '{folder_path}': {deleted_files}")