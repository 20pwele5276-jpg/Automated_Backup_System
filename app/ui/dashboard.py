import streamlit as st
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.backup_service import (
    create_backup,
    restore_backup,
    BACKUP_ROOT,
)

st.set_page_config(
    page_title="Automated Backup System",
    page_icon="💾",
    layout="wide",
)

st.title("💾 Automated Backup System")
st.caption("Create, view, and restore local folder backups.")

st.divider()

# Create backup
st.subheader("📦 Create a Backup")

source_folder = st.text_input(
    "Folder path to back up",
    placeholder="/home/WajihaGul/Documents",
)

if st.button("Create Backup", type="primary"):
    if not source_folder.strip():
        st.warning("Please enter a folder path.")
    else:
        try:
            with st.spinner("Creating backup..."):
                backup_path = create_backup(source_folder.strip())
            st.success("Backup created successfully!")
            st.code(str(backup_path))
        except Exception as error:
            st.error(f"Backup failed: {error}")

st.divider()

# List existing backups
st.subheader("📁 Existing Backups")

backups = sorted(
    [item for item in BACKUP_ROOT.iterdir() if item.is_dir()],
    key=lambda item: item.stat().st_mtime,
    reverse=True,
)

if backups:
    st.write(f"Total backups: {len(backups)}")

    selected_backup = st.selectbox(
        "Select a backup to restore",
        backups,
        format_func=lambda item: item.name,
    )

    destination_folder = st.text_input(
        "Restore destination (must be a new folder)",
        placeholder="/home/WajihaGul/restored_files",
    )

    if st.button("Restore Selected Backup"):
        if not destination_folder.strip():
            st.warning("Please enter a destination path.")
        else:
            try:
                with st.spinner("Restoring backup..."):
                    restored_path = restore_backup(
                        selected_backup,
                        destination_folder.strip(),
                    )
                st.success("Backup restored successfully!")
                st.code(str(restored_path))
            except Exception as error:
                st.error(f"Restore failed: {error}")

    with st.expander("View all backup locations"):
        for backup in backups:
            st.write(f"📁 {backup.name}")
            st.caption(str(backup))
else:
    st.info("No backups found. Create your first backup above.")

st.divider()
st.subheader("📋 Backup Activity Log")

log_file = PROJECT_ROOT / "logs" / "backup.log"

if log_file.exists() and log_file.stat().st_size > 0:
    log_text = log_file.read_text(encoding="utf-8", errors="replace")
    st.code(log_text[-10000:], language="text")
else:
    st.info("No activity recorded yet.")

from app.services.scheduler_service import get_scheduler

st.divider()
st.subheader("⏰ Automatic Backup Scheduling")

scheduled_folder = st.text_input(
    "Folder to back up automatically",
    placeholder="/home/WajihaGul/backup_test",
    key="scheduled_folder",
)

interval_minutes = st.number_input(
    "Backup interval (minutes)",
    min_value=1,
    max_value=1440,
    value=60,
    step=1,
)

if st.button("Schedule Automatic Backup"):
    if not scheduled_folder.strip():
        st.warning("Please enter a folder path.")
    else:
        try:
            from pathlib import Path

            folder = Path(scheduled_folder).expanduser().resolve()

            if not folder.is_dir():
                st.error("The selected folder does not exist.")
            else:
                scheduler = get_scheduler()
                scheduler.add_job(
                    create_backup,
                    trigger="interval",
                    minutes=int(interval_minutes),
                    args=[str(folder)],
                    id="automatic_backup",
                    replace_existing=True,
                    max_instances=1,
                )
                st.success(
                    f"Automatic backup scheduled every "
                    f"{int(interval_minutes)} minute(s)."
                )
        except Exception as error:
            st.error(f"Could not schedule backup: {error}")

scheduler = get_scheduler()

if scheduler.get_job("automatic_backup"):
    st.info("An automatic backup schedule is active while this app is running.")
    if st.button("Cancel Automatic Backup"):
        scheduler.remove_job("automatic_backup")
        st.success("Automatic backup schedule cancelled.")
        st.rerun()
else:
    st.caption("No automatic backup schedule is currently active.")
