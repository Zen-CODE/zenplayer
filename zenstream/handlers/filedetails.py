from styler import Styler
from datetime import datetime
from os import stat as os_stat
import stat


class FileDetails:
    @staticmethod
    def show_file(file_name: str):
        """Display the file details."""

        # st.subheader("File")
        stat_info = os_stat(file_name)
        mtime_datetime = datetime.fromtimestamp(stat_info.st_mtime)
        ctime_datetime = datetime.fromtimestamp(stat_info.st_ctime)
        atime_datetime = datetime.fromtimestamp(stat_info.st_atime)
        file_size_mb = stat_info.st_size / (1024 * 1024)
        data = {
            "File name": file_name,
            "File Size": f"{file_size_mb:.2f} MB",
            "Device ID": f"{stat_info.st_dev}",
            "Last Modified": mtime_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "Created": ctime_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "Last Accessed": atime_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "Owner User ID (UID)": stat_info.st_uid,
            "Owner Group ID (GID)": stat_info.st_gid,
            "Permissions": stat.filemode(stat_info.st_mode),
        }
        Styler.show_dict("File details", data)
