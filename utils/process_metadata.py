import re

def simplify_metadata(metadata: list[str]) -> str:
    return "-".join([item.split("_", 1)[1] for item in metadata])

def extract_metadata(encrypted: str) -> list[str]:
    return [prefix + part for prefix, part in zip(["c_", "r_", "rc_"], encrypted.split("-"))]

def is_valid_metadata(s: str) -> bool:
    parts = s.split("-")
    if len(parts) != 3: 
        return False
    return all(re.compile(r"^[0-9a-f]+$").match(p) for p in parts)