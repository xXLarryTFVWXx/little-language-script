
from typing import Any


opcodes: dict[int, dict[str, int]] = {}

special_instructions = {
    "!display": {
        "size": 3,
        "arguments": ["mode", "size", "refresh_rate"],
        "options": {
            "mode": ["text", "graphic"],
            "size": ["rows", "columns", "width", "height"],
            "refresh_rate": ["fps"]
        }
    }
}

