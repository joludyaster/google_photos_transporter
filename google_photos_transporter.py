import os
import shutil
from datetime import datetime
import json
from pathlib import Path
import time


class FileTransporter:
    def __init__(self, folder: Path, folder_to_move: Path | str, who_to_move: str, files: list[str]):

        """
        Initialize class variables to manipulate them later on.

        :param folder: folder that the script is located in
        :param folder_to_move: folder to which a file should be moved
        :param who_to_move: name of the user/person whose files are being moved
        :param files: list of files that should be moved
        """

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
    def get_json_google_photo_data(path_to_file: Path | str):

        """
        Function to extract json data from a file

        Explanation: Google automatically adds .json files with the exact names of the files
        that display information about the file -> title, description, photo taken time etc.

        :param path_to_file: path to a json file
        :return: data in `dict` type
        """

        try:
            with open(f"{path_to_file}.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return f"[ERROR] JSON data was not found for file -> {path_to_file}"

    def file_selector(self):

        """
        Selects a file and sets up a folder depending on the extension of the file

        .png, .jpg etc. -> photos
        .mkv, .mp4 -> videos

        The rest of the extensions are considered to be the files, so it's automatically `files`

        :return: Nothing or an error
        """

        try:
            if os.path.exists(self.folder):
                for file in self.list_of_files:
                    check_extension = file.split(".")
                    get_metadata = self.get_json_google_photo_data(f"{self.folder}/{file}")

                    if not get_metadata:
                        continue

                    if type(get_metadata) is dict:
                        get_photo_taken_time = get_metadata.get("photoTakenTime", None)

                        if get_photo_taken_time:
                            get_timestamp = int(get_photo_taken_time.get('timestamp', None))

                            if get_timestamp:
                                get_taken_data = datetime.fromtimestamp(timestamp=get_timestamp)
                                format_date = get_taken_data.strftime("%Y-%m-%d").replace("-", "_")

                                if check_extension[-1].lower() in self.photo_formats:
                                    format_selector = self.photo_folder_format
                                elif check_extension[-1].lower() in self.video_formats:
                                    format_selector = self.video_folder_format
                                else:
                                    format_selector = self.file_folder_format

                                folder = f"{self.folder_to_move}/{format_selector}/{self.who_to_move}/{format_selector}_from_{format_date}_by_{self.who_to_move}"

                                print(f"[INFO] Trying to transport {file}...")

                                self.transport_file(
                                    folder=Path(folder),
                                    file=file
                                )

                            else:
                                print(f"[ERROR] Photo taken time was not found. Checking next file...")
                                continue
                        else:
                            print(f"[ERROR] Photo taken time was not found. Checking next file...")
                            continue

                print(f"[INFO] Finished transporting files in folder: {self.folder}")

            return f"[ERROR] The path {self.folder} is not valid."

        except Exception as e:
            return f"[ERROR] {e} occurred while processing information in transport_file() function."

    def transport_file(self, folder: Path, file: str):

        """
        Copies a file from one folder to another using `shutil` python library

        :param folder: path to a folder where a file is located that needs to be moved
        :param file: name of the file that needs to be moved
        :return: successful copy of the file or an error
        """

        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"[SUCCESS] {file} was successfully transported into -> {folder}")
                return shutil.copy(
                    src=f"{self.folder}/{file}",
                    dst=folder
                )

            else:
                if os.path.exists(f"{folder}/{file}"):
                    print(f"[WARNING] The file {file} already exists, skipping to the next file...")
                    return

                print(f"[SUCCESS] {file} was successfully transported into -> {folder}")
                return shutil.copy(
                    src=f"{self.folder}/{file}",
                    dst=folder
                )

        except Exception as e:
            return f"[ERROR] {e} occurred while transferring {file} to -> {folder}"


def main():

    folder_to_move = f"{os.getcwd().replace('\\', '/')}"

    who_to_move = "user"

    input_path = str(input("Enter the path of your Google Photos: ")).replace("\\", "/")

    try:
        if os.path.exists(Path(input_path)):

            old_time = time.time()

            for subdir, dirs, files in os.walk(input_path):
                thread = FileTransporter(
                    folder=Path(subdir),
                    folder_to_move=Path(folder_to_move),
                    who_to_move=who_to_move,
                    files=files
                )
                thread.file_selector()

            time_difference = time.time() - old_time

            text = f"""
[INFO] Program finished transporting all of the files.

Program finished it's job in {time_difference}"""

            return text

        return f"[ERROR] The path you provided doesn't exist."

    except Exception as e:
        return f"[ERROR] {e} occurred while processing {input_path}."


if __name__ == "__main__":
    print(main())
