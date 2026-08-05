import urllib.request
from datetime import date
from typing import Dict, Optional

AMFI_NAV_URL = "https://www.amfiindia.com/spages/NAVAll.txt"

def fetch_amfi_nav_data() -> Dict[str, float]:
    """
    Fetches latest Mutual Fund NAVs directly from AMFI official text endpoint.
    Format: Scheme Code;ISIN Div Payout;ISIN Div Reinvestment;Scheme Name;Net Asset Value;Date
    """
    nav_map: Dict[str, float] = {}
    try:
        req = urllib.request.Request(AMFI_NAV_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            lines = response.read().decode('utf-8').splitlines()
            for line in lines:
                parts = line.split(';')
                if len(parts) >= 6:
                    scheme_code = parts[0].strip()
                    try:
                        nav = float(parts[4].strip())
                        nav_map[scheme_code] = nav
                    except ValueError:
                        continue
    except Exception as e:
        print(f"AMFI NAV fetch warning: {e}")
        
    return nav_map
