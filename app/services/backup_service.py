from pathlib import Path
from datetime import datetime
import shutil
import logging

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKUP_ROOT = (PROJECT_ROOT / "backups").resolve()
LOG_ROOT = PROJECT_ROOT / "logs"

BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
LOG_ROOT.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_ROOT / "backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_backup(source_folder):
    """Create a timestamped copy of a folder."""
    source = Path(source_folder).expanduser().resolve()

    if not source.is_dir():
        raise ValueError("Please select an existing folder.")

    if source == BACKUP_ROOT or BACKUP_ROOT in source.parents:
        raise ValueError("You cannot back up the backup directory itself.")

    destination = BACKUP_ROOT / (
        f"{source.name}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    )

    try:
        shutil.copytree(source, destination)
        logging.info("Backup created: %s -> %s", source, destination)
        return destination
    except Exception:
        logging.exception("Backup failed for %s", source)
        raise


def restore_backup(backup_folder, destination_folder):
    """Restore a backup to a new destination folder."""
    backup = Path(backup_folder).expanduser().resolve()
    destination = Path(destination_folder).expanduser().resolve()

    if backup.parent != BACKUP_ROOT or not backup.is_dir():
        raise ValueError("Please select a valid backup from this project.")

    if destination.exists():
        raise ValueError("Destination already exists. Choose a new folder.")

    if destination == BACKUP_ROOT or BACKUP_ROOT in destination.parents:
        raise ValueError("Choose a destination outside the backups directory.")

    if backup == destination or backup in destination.parents:
        raise ValueError("Choose a destination outside the selected backup.")

    try:
        shutil.copytree(backup, destination)
        logging.info("Backup restored: %s -> %s", backup, destination)
        return destination
    except Exception:
        logging.exception("Restore failed for %s", backup)
        raise
