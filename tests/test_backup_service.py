from pathlib import Path
import pytest

from app.services.backup_service import create_backup, restore_backup


def test_create_backup(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "example.txt").write_text("Backup test", encoding="utf-8")

    backup = create_backup(source)

    assert backup.is_dir()
    assert (backup / "example.txt").read_text(encoding="utf-8") == "Backup test"


def test_restore_backup(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "example.txt").write_text("Restore test", encoding="utf-8")

    backup = create_backup(source)
    destination = tmp_path / "restored"

    restore_backup(backup, destination)

    assert destination.is_dir()
    assert (destination / "example.txt").read_text(encoding="utf-8") == "Restore test"


def test_restore_refuses_existing_destination(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "example.txt").write_text("Original", encoding="utf-8")

    backup = create_backup(source)
    destination = tmp_path / "existing"
    destination.mkdir()

    with pytest.raises(ValueError, match="Destination already exists"):
        restore_backup(backup, destination)
