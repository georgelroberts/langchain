from __future__ import annotations

import json
import re
from typing import List

from langchain.schema import OutputParserException


def parse_json_markdown(json_string: str) -> dict:
    # Try to find JSON string within triple backticks
    match = re.search(r"```(json)?(.*?)```", json_string, re.DOTALL)

    # If no match found, assume the entire string is a JSON string
    json_str = json_string if match is None else match[2]
    # Strip whitespace and newlines from the start and end
    json_str = json_str.strip()

    return json.loads(json_str)


def parse_and_check_json_markdown(text: str, expected_keys: List[str]) -> dict:
    try:
        json_obj = parse_json_markdown(text)
    except json.JSONDecodeError as e:
        raise OutputParserException(f"Got invalid JSON object. Error: {e}")
    for key in expected_keys:
        if key not in json_obj:
            raise OutputParserException(
                f"Got invalid return object. Expected key `{key}` "
                f"to be present, but got {json_obj}"
            )
    return json_obj
