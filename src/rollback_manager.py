"""
Rollback Manager
Version control and backup system
"""
import shutil
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger

BACKUP_PATH = "backup/"
SRC_PATH = "src/"

class RollbackManager:
    """Manage backups and rollbacks"""
    
    def __init__(self):
        os.makedirs(BACKUP_PATH, exist_ok=True)
    
    def create_backup(self):
        """Create backup of current code"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(BACKUP_PATH, f"backup_{timestamp}")
        
        try:
            shutil.copytree(SRC_PATH, backup_dir)
            logger.info(f"✅ Backup created: {backup_dir}")
            return backup_dir
        except Exception as e:
            logger.exception(f"Backup failed: {e}")
            return None
    
    def rollback(self, backup_name=None):
        """Rollback to previous version"""
        if not os.path.exists(BACKUP_PATH):
            logger.error("No backups found")
            return False
        
        backups = sorted([d for d in os.listdir(BACKUP_PATH) if d.startswith("backup_")])
        
        if not backups:
            logger.error("No backup directories found")
            return False
        
        if backup_name:
            source = os.path.join(BACKUP_PATH, backup_name)
        else:
            source = os.path.join(BACKUP_PATH, backups[-1])  # Latest backup
        
        try:
            if os.path.exists(SRC_PATH):
                shutil.rmtree(SRC_PATH)
            shutil.copytree(source, SRC_PATH)
            logger.info(f"🔄 Rollback successful: {source}")
            return True
        except Exception as e:
            logger.exception(f"Rollback failed: {e}")
            return False

def rollback():
    """Quick rollback to latest backup"""
    manager = RollbackManager()
    return manager.rollback()
