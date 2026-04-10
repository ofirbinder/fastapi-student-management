import json

import portalocker
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.ServerError import ServerJsonParseError


def read_db() -> list:
    with portalocker.Lock(settings.DATABASE_PATH, mode="r", encoding="utf-8", timeout=5) as f:
        content = f.read().strip()

        if not content:
            return []
        try:
            data = json.loads(content)
            if not isinstance(data, list):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database Corruption Error: The internal JSON file is invalid.",
                )
            return data
        except json.JSONDecodeError as err:
            raise ServerJsonParseError() from err


def write_db(data: list) -> None:
    with portalocker.Lock(settings.DATABASE_PATH, mode="w", encoding="utf-8", timeout=5) as f:
        json.dump(data, f, indent=4)
