import shutil
import os

BACKUP_PATH = "backup/"
CURRENT_PATH = "src/"

def rollback():
    """Restores the last working version of the bot."""
    if os.path.exists(BACKUP_PATH):
        shutil.rmtree(CURRENT_PATH)
        shutil.copytree(BACKUP_PATH, CURRENT_PATH)
        print("🔄 Rollback successful!")
    else:
        print("❌ No backup found.")

