import json
import logging
import os
import uuid
from asyncio import Lock
from collections import defaultdict
from pathlib import Path
from typing import Dict, Any, List

import aiofiles

logger = logging.getLogger(__name__)

data_dir = Path("data")
try:
    data_dir.mkdir(exist_ok=True)
except FileExistsError:
    pass

file_locks = defaultdict(Lock)


async def save_json(filename: str, data: List[Dict[str, Any]]):
    file_path = data_dir / f"{filename}.json"
    temp_file_path = file_path.with_suffix(".tmp")

    async with file_locks[filename]:
        try:
            # Read existing data
            if file_path.exists():
                async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.loads(await f.read())
                        if not isinstance(existing_data, list):
                            existing_data = []  # If somehow corrupted, reset to empty list
                    except json.JSONDecodeError:
                        existing_data = []  # Handle corrupt file case
            else:
                existing_data = []

            # Add new entries
            new_data = [{"id": str(uuid.uuid4()), "RawData": entry} for entry in data]
            updated_data = existing_data + new_data  # Append new episodes

            # Write back to file
            async with aiofiles.open(temp_file_path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(updated_data, indent=4))

            os.replace(temp_file_path, file_path)
            logger.info(f"Successfully saved {len(new_data)} new entries to {file_path}")

        except IOError as e:
            logger.error(f"File I/O error while saving {filename}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving {filename}: {e}")