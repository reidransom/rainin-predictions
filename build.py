import random
from copy import deepcopy
from datetime import datetime

import requests
import xmltodict
from jinja2 import Environment, FileSystemLoader, select_autoescape, Markup

import config
from data import PREDICTIONS



def get_date(game):
    date = datetime.strptime(game["gameDate"], "%Y-%m-%d %H:%M:%S")
    return date


def get_opponent(game):
    opp = game["home"]
    place = "@"
    if game["home"] == "BOS":
        opp = game["away"]
        place = "vs"
    html = f"{place} <img class='opp' src='/img/{opp}.png' /> {opp}"
    html = Markup(html)
    return html


def get_prediction(game, j):
    pred = PREDICTIONS[game["gameId"]][j]
    if not isinstance(pred, str):
        return pred[0]
    return pred


def get_result(game):
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
    loader=FileSystemLoader(config.TMPL_DIR),
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
season = deepcopy(record)
for game in data["FantasyBasketballNerd"]["Game"]:
    date = get_date(game)
    rdata = {
        "john": get_prediction(game, "john"),
        "jay": get_prediction(game, "jay"),
        "jam": get_prediction(game, "jam"),
    }
    for j in record.keys():
        season[j][rdata[j]] += 1
    result = get_result(game)
    if result:
        for j in record.keys():
            record[j]["W" if result == rdata[j] else "L"] += 1
    table.append([
        date.strftime("%a, %b %d"),
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
    "season": season,
}

with open(config.DIST_DIR / "index.html", "w") as fp:
    fp.write(tmpl.render(**context))
