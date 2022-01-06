import os
import atexit
import schedule
import time
import datetime
from shutil import copyfile


def handle_exit():
    print("Killing DS2 process")
    os.system("taskkill /f /im DS2.exe")


def handle_path_info(current_dir):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    storage_file_name = "save_path.txt"
    storage_file_path = f"{current_dir}/{storage_file_name}"
    if not os.path.isfile(storage_file_path):
        save_path = input(">>> Paste the absolute path to your DS2 savefile location\n>>> ")
        with open("save_path.txt", "w") as f:
            f.write(save_path)

    with open(storage_file_name, "r") as f:
        save_file_path = f.readline()

        return save_file_path


def cleanup_backups():
    list_of_backups = os.listdir("backups")
    abs_path = ["backups/{0}".format(i) for i in list_of_backups]

    if len(list_of_backups) == 10:
        print("Removing oldest backup...")
        oldest_backup = min(abs_path, key=os.path.getctime)
        os.remove(os.path.abspath(oldest_backup))


def create_backup(save_file_path, backup_dir):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
    save_file_name = save_file_path.rsplit('/', 1)[-1]
    cleanup_backups()
    print(f"Creating backup with timestamp: {timestamp}")
    copyfile(save_file_path, backup_dir+f"{save_file_name}.{timestamp}")


current_dir = os.path.dirname(os.path.realpath(__file__))
save_file_path = handle_path_info(current_dir)
backup_dir = current_dir+"/backups/"

if not os.path.isdir(backup_dir):
    os.mkdir(backup_dir)

schedule.every(2).minutes.do(create_backup, save_file_path, backup_dir)
atexit.register(handle_exit)

while True:
    schedule.run_pending()
    time.sleep(1)
