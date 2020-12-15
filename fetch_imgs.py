import requests

import config


TEAMS = [
    "BOS",
    "BKN",
    "ny",
    "PHI",
    "TOR",
    "CHI",
    "CLE",
    "DET",
    "IND",
    "MIL",
    "ATL",
    "CHA",
    "MIA",
    "ORL",
    "WAS",
    "DEN",
    "MIN",
    "OKC",
    "POR",
    "utah",
    "GSW",
    "LAC",
    "LAL",
    "PHX",
    "SAC",
    "DAL",
    "HOU",
    "MEM",
    "no",
    "SAS",
]

for code in TEAMS:
    path = config.DIST_DIR / "img" / f"{code}.png"
    url = f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{code}.png&w=50&h=50"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
