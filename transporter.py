import os
import shutil
from datetime import datetime
import json
from pathlib import Path


class FileTransporter:
    def __init__(self, folder, folder_to_move, who_to_move, files):
        self.folder = folder
        self.list_of_files = files
        self.folder_to_move = folder_to_move
        self.who_to_move = who_to_move

        self.photo_formats = ["jpeg", "jpg", "gif", "tiff", "raw", "png"]
        self.video_formats = ["mp4", "mov", "avi", "wmv", "avchd", "webm", "flv", "mkv", "mpeg-4"]

        self.photo_folder_format = "photos"
        self.video_folder_format = "videos"
        self.file_folder_format = "files"

    @staticmethod
    def get_json_google_photo_data(path_to_file):
        try:
            with open(f"{path_to_file}.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return f"[ERROR] JSON data was not found for file -> {path_to_file}"

    def file_selector(self):
        try:
            if os.path.exists(self.folder):
                for file in self.list_of_files:
                    check_extension = file.split(".")
                    get_metadata = self.get_json_google_photo_data(f"{self.folder}/{file}")
                    if not get_metadata:
                        continue

                    if type(get_metadata) is dict:

                        get_timestamp = int(get_metadata["photoTakenTime"]["timestamp"])
                        get_taken_data = datetime.fromtimestamp(timestamp=get_timestamp)
                        get_date = get_taken_data.strftime("%Y-%m-%d").replace("-", "_")

                        new_folder = f"{self.folder_to_move}/{self.file_folder_format}/{self.who_to_move}/{self.file_folder_format}_from_{get_date}_by_{self.who_to_move}"

                        if check_extension[-1].lower() in self.photo_formats:
                            new_folder = f"{self.folder_to_move}/{self.photo_folder_format}/{self.who_to_move}/{self.photo_folder_format}_from_{get_date}_by_{self.who_to_move}"
                        elif check_extension[-1].lower() in self.video_formats:
                            new_folder = f"{self.folder_to_move}/{self.video_folder_format}/{self.who_to_move}/{self.video_folder_format}_from_{get_date}_by_{self.who_to_move}"

                        print(f"[INFO] Trying to transport {file}...")
                        self.transport_file(
                            folder=new_folder,
                            file=file
                        )

                print(f"[INFO] Finished transporting files in folder: {self.folder}")

            return f"[ERROR] The path {self.folder} is not valid."
        except Exception as e:
            return f"[ERROR] {e} occurred while processing information in transport_file() function."

    def transport_file(self, folder, file):
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"[SUCCESS] {file} was successfully transported into -> {folder}")
                shutil.copy(
                    src=f"{self.folder}/{file}",
                    dst=folder
                )

            else:
                print(f"[SUCCESS] {file} was successfully transported into -> {folder}")
                shutil.copy(
                    src=f"{self.folder}/{file}",
                    dst=folder
                )
        except Exception as e:
            return f"[ERROR] {e} occurred while transferring {file} to -> {folder}"


def main():
    folder_to_move = f"{os.getcwd().replace('\\', '/')}"  # Get current directory's name
    who_to_move = "davyd"

    input_path = str(input("Enter the path of your Google Photos: ")).replace("\\", "/")

    try:
        if os.path.exists(Path(input_path)):

            for subdir, dirs, files in os.walk(input_path):
                thread = FileTransporter(
                    folder=subdir,
                    folder_to_move=folder_to_move,
                    who_to_move=who_to_move,
                    files=files
                )
                thread.file_selector()

            print(f"[INFO] Program finished transporting all of the files.")

        return f"[ERROR] The path you provided doesn't exist."
    except Exception as e:
        return f"[ERROR] {e} occurred while processing {input_path}."


if __name__ == "__main__":
    main()
