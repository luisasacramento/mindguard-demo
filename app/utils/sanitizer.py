import re
from typing import Optional

WHITELIST_USERNAME = re.compile(r'^[A-Za-z0-9_.-]{3,30}$')

def sanitize_username(value: str) -> Optional[str]:
    if not value:
        return None
    if WHITELIST_USERNAME.match(value):
        return value
    return None
