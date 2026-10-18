from apscheduler.schedulers.background import BackgroundScheduler
from app.services.backup_service import create_backup
import logging

_scheduler = BackgroundScheduler()


def run_scheduled_backup(source_folder):
    """Run a scheduled backup and record any failure."""
    try:
        create_backup(source_folder)
    except Exception:
        logging.exception("Scheduled backup failed for %s", source_folder)


def get_scheduler():
    """Start the scheduler once and return it."""
    if not _scheduler.running:
        _scheduler.start()
    return _scheduler
