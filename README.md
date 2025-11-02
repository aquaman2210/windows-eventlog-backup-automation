# windows-eventlog-backup-automation
# Windows Event Log Backup Automation

---
## ✨ Features

- 🔄 Automatically exports Application, System logs (`.evtx`)
- 🗜 Compresses logs into a single `.zip` file with timestamp
- 🧹 Removes old backups based on retention settings
- 📁 Logs all activity to `logs/backup_log.txt`
- 💻 Displays hostname (`os.environ`) to identify which machine ran the backup
- 🕓 Easily scheduled via Windows Task Scheduler

---

## ⚙️ Installation & Usage

### 1️⃣ Prerequisites
- Windows 10 or later  
- Python 3.10+  
- Administrator privileges (required to export Event Logs)

### 2️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/windows-eventlog-backup.git
cd windows-eventlog-backup

 3️⃣ Install dependencies
pip install -r requirements.txt

 4️⃣ Run the script
python backup_eventlogs.py


Or, schedule it to run automatically using Windows Task Scheduler.