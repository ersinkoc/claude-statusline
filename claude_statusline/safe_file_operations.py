#!/usr/bin/env python3
"""
Safe file operations with retry and atomic writes
"""

import json
import time
import tempfile
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def safe_json_read(file_path: Path, max_retries: int = 3, retry_delay: float = 0.1):
    """
    Safely read JSON file with retries
    """
    for attempt in range(max_retries):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (IOError, OSError) as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            raise
        except json.JSONDecodeError:
            # File might be corrupted or being written
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            raise
    
def safe_json_write(data: dict, file_path: Path, max_retries: int = 3, retry_delay: float = 0.1):
    """
    Safely write JSON file with atomic operation
    """
    # Create temp file in same directory for atomic rename
    temp_fd, temp_path = tempfile.mkstemp(
        dir=file_path.parent,
        prefix=file_path.stem + '_',
        suffix='.tmp'
    )
    
    try:
        # Write to temp file
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename with retries
        for attempt in range(max_retries):
            try:
                # On Windows, need to remove target first if exists
                if os.name == 'nt' and file_path.exists():
                    try:
                        os.remove(file_path)
                    except:
                        pass
                
                # Rename temp to target
                os.rename(temp_path, file_path)
                return True
                
            except (OSError, IOError) as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    # Last attempt failed
                    logger.error(f"Failed to write {file_path}: {e}")
                    raise
    finally:
        # Clean up temp file if still exists
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass
    
    return False

def safe_update_json(file_path: Path, update_func, max_retries: int = 5, retry_delay: float = 0.2):
    """
    Safely update JSON file with read-modify-write pattern
    
    Args:
        file_path: Path to JSON file
        update_func: Function that takes data dict and modifies it
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    """
    for attempt in range(max_retries):
        try:
            # Read current data
            if file_path.exists():
                data = safe_json_read(file_path)
            else:
                data = {}
            
            # Apply update
            update_func(data)
            
            # Write back
            safe_json_write(data, file_path)
            return True
            
        except Exception as e:
            if attempt < max_retries - 1:
                logger.debug(f"Retry {attempt + 1}/{max_retries} for {file_path}: {e}")
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                continue
            else:
                logger.error(f"Failed to update {file_path} after {max_retries} attempts: {e}")
                raise
    
    return False