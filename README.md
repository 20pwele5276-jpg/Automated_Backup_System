# Automated Backup System

A Python-based application for creating, restoring, and scheduling local folder backups through a Streamlit dashboard.

## Features

- **Create Backups:** Copy selected folders into timestamped backup directories.
- **Restore Backups:** Restore files to a new destination.
- **Automatic Scheduling:** Schedule backups at a chosen interval while the application is running.
- **Activity Logs:** Record backup and restore operations.
- **Backup History:** View previously created backups.
- **Automated Testing:** Test core backup and restore functionality.

## Technologies Used

- Python
- Streamlit
- APScheduler
- Pytest
- Logging
- Git and GitHub

## Project Structure

```text
Automated_Backup_System/
├── app/
│   ├── services/
│   │   ├── backup_service.py
│   │   └── scheduler_service.py
│   └── ui/
│       └── dashboard.py
├── backups/
├── logs/
├── tests/
│   └── test_backup_service.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
