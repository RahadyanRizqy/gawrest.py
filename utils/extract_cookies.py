import re
from typing import Dict, Optional

def extract_cookies(cookie_header: str) -> Dict[str, Optional[str]]:
    """
    Extract __Secure-1PSID and __Secure-1PSIDTS cookies from COOKIE_HEADER environment variable.
    
    Returns:
        Dict containing psid and psidts if found, None otherwise
    """
    if not cookie_header:
        return {"psid": None, "psidts": None}
    
    # Remove any single quotes that might be around the cookie header
    cookie_header = cookie_header.strip("'\"")
    
    # Find the secure cookies using regex
    psid_match = re.search(r'__Secure-1PSID=([^;]+)', cookie_header)
    psidts_match = re.search(r'__Secure-1PSIDTS=([^;]+)', cookie_header)
    
    psid = psid_match.group(1) if psid_match else None
    psidts = psidts_match.group(1) if psidts_match else None
    
    return {"__Secure-1PSID": psid, "__Secure-1PSIDTS": psidts}