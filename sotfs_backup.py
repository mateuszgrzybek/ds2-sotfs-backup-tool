import os
import atexit
import schedule
import time
import datetime
import sys
from keyboard import is_pressed
from shutil import copyfile


def handle_exit():
    os.system("taskkill /f /im DarkSoulsII.exe")


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
    abs_path = ["backups\\{0}".format(i) for i in list_of_backups]

    if len(list_of_backups) == 10:
        print("Removing oldest backup...")
        oldest_backup = min(abs_path, key=os.path.getctime)
        os.remove(os.path.abspath(oldest_backup))


def create_backup(save_file_path, backup_dir):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d.%H-%M-%S')
    save_file_name = save_file_path.rsplit('\\', 1)[-1]
    cleanup_backups()
    print(f"Creating backup with timestamp: {timestamp}")
    copyfile(save_file_path, backup_dir+f"{save_file_name}.{timestamp}")


current_dir = os.path.dirname(os.path.realpath(__file__))
save_file_path = handle_path_info(current_dir)
backup_dir = current_dir + "\\backups\\"

if not os.path.isdir(backup_dir):
    os.mkdir(backup_dir)

while True:
    try:
        backup_interval = int(input(">>>How often do you want the tool to create a new backup? Please specify the value in MINUTES\n>>> "))
    except ValueError:
        print("You must specify the value as minutes in numeric format")
    else:
        break

schedule.every(backup_interval).minutes.do(create_backup, save_file_path, backup_dir)
atexit.register(handle_exit)

while True:
    schedule.run_pending()
    
    if is_pressed("esc"):
        sys.exit()

    time.sleep(1)
    