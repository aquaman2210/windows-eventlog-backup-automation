import os
import datetime
import shutil
import subprocess
import json
import zipfile
import logging

#information
HOSTNAME = os.environ.get("COMPUTERNAME","Unknown")

CONFIG = "config.json"
if not os.path.exists(CONFIG):
    raise FileNotFoundError("CREATE FILE JSON FIRST!!")
#READ CONFIG.JSON
with open(CONFIG,"r",encoding="utf-8") as f:
    config = json.load(f)

#MAPPING JSON
BACKUP_FOLDER = config["backup_folder"]
LOG_FOLDER = config["log_folder"]
KEEP_DAYS = config["keep_days"]
EVENTS = config["events"]
OUTPUT_FORMAT = config["output_format"]

#Create folders
os.makedirs(BACKUP_FOLDER,exist_ok=True)
os.makedirs(LOG_FOLDER,exist_ok=True)

#Set up file log
logging.basicConfig(
    filename=os.path.join(LOG_FOLDER,"backup_log.txt"),
    level=logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s"
)

#Export log
def export_event_log():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = os.path.join(BACKUP_FOLDER,f"eventlog_{timestamp}")
    os.makedirs(export_dir,exist_ok=True)

    for log_name in EVENTS:
        output_path = os.path.join(export_dir,f"{log_name}.{OUTPUT_FORMAT}")
        try:
            subprocess.run(["wevtutil", "epl", log_name, output_path], check=True)
            logging.info(f"Export {log_name} log to {output_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to export {log_name}: {e}")
    return export_dir

# ZIP FOLDER
def compress_backup(folder_path):
    zipname = folder_path + ".zip"
    shutil.make_archive(folder_path, 'zip', folder_path)
    shutil.rmtree(folder_path)
    logging.info(f"Compress backup to: {zipname}")
    return zipname

#Clear backup after keep_days
def cleanup_old_backup():
    now = datetime.datetime.now()
    for filename in os.listdir(BACKUP_FOLDER):
        path = os.path.join(BACKUP_FOLDER, filename)
        if os.path.isfile(path) and filename.endswith(".zip"):
            filetime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            if (now - filetime).days > KEEP_DAYS:
                os.remove(path)
                logging.info(f"Deleted old backup: {filename}")

#main
def main():
    logging.info(f"HOST: {HOSTNAME} 🚀 Starting Event Log Backup......")
    folder = export_event_log()
    compress_backup(folder)
    cleanup_old_backup()
    logging.info(f"[HOST: {HOSTNAME}] ✅ Backup Completed Successful.\n")

if __name__ == "__main__":
    main()

