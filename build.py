import random
from datetime import datetime
from pathlib import Path
from os.path import dirname, abspath

import requests
import xmltodict
from jinja2 import Environment, FileSystemLoader, select_autoescape, Markup

from data import PREDICTIONS

BASE_DIR = Path(dirname(abspath(__file__)))
TMPL_DIR = BASE_DIR / "templates"
DIST_DIR = BASE_DIR / "dist"


def get_date(game):
    date = datetime.strptime(game["gameDate"], "%Y-%m-%d %H:%M:%S")
    return date


def get_opponent(game):
    return "{away} at {home}".format(**game)


def get_prediction(game, j):
    pred = PREDICTIONS[game["gameId"]][j]
    if not isinstance(pred, str):
        return pred[0]
    return pred


def get_result(game):
    return random.choice(["W", "L"])
    winner = game.get("winner")
    if not winner:
        return None
    if winner == "BOS":
        result = "W"
    return "L"


def get_extra(game):
    preds = PREDICTIONS[game["gameId"]].items()
    extra = []
    for j, v in preds:
        if isinstance(v, tuple):
            J = j.capitalize()
            extra.append(f"{J}: {v[1]}")
    return Markup("<br>".join(extra))


env = Environment(
    loader=FileSystemLoader(TMPL_DIR),
    autoescape=select_autoescape(["html", "xml"])
)

xml = requests.get("https://www.fantasybasketballnerd.com/service/schedule/BOS").text
data = xmltodict.parse(xml)
tmpl = env.get_template("index.html")
table = []
record = {
    "john": {"W": 0, "L": 0},
    "jay": {"W": 0, "L": 0},
    "jam": {"W": 0, "L": 0},
}
for game in data["FantasyBasketballNerd"]["Game"]:
    date = get_date(game)
    rdata = {
        "john": get_prediction(game, "john"),
        "jay": get_prediction(game, "jay"),
        "jam": get_prediction(game, "jam"),
    }
    result = get_result(game)
    if result:
        for j in record.keys():
            record[j]["W" if result == rdata[j] else "L"] += 1
    table.append([
        date.strftime("%b %d"),
        get_opponent(game),
        date.strftime("%-I:%M %p"),
        rdata["john"],
        rdata["jay"],
        rdata["jam"],
        result if result else "-",
        get_extra(game),
    ])
context = {
    "title": "Rainin’ Predictions",
    "table": table,
    "record": record,
}

with open(DIST_DIR / "index.html", "w") as fp:
    fp.write(tmpl.render(**context))
