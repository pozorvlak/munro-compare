import re

from flask import Flask, render_template
import requests


app = Flask(__name__)


@app.route('/')
@app.route('/<user1>/<user2>')
def hello(user1=None, user2=None):
    return render_template('hello.html', user1=user1, user2=user2)

@app.route('/<user1>/<user2>.json')
def json(user1=None, user2=None):
    rows1 = html_to_rows(html_path_for_user(user1))
    rows2 = html_to_rows(html_path_for_user(user2))
    all = compare_rows(rows1, rows2)
    return all


LATLNG = re.compile(r'latlng = \{WGS84: \[(-?\d{1,2}\.\d+),(-?\d{1,2}\.\d+)\]\};')
MARKER = re.compile(f'var marker2 = createMarker\(map,.*?,.*?,"(\d+)",.*?,"(.*?)",.*?,latlng,(blue|red)Icon\);')


def compare_rows(rows1, rows2):
    all = []
    for r1, r2 in zip(rows1, rows2):
        climbed1, climbed2 = r1[3], r2[3]
        if climbed1 and climbed2:
            all.append(r1[:3] + ["both"])
        elif climbed1:
            all.append(r1[:3] + ["only1"])
        elif climbed2:
            all.append(r1[:3] + ["only2"])
        else:
            all.append(r1[:3] + ["neither"])
    return all


def html_path_for_user(user_id):
    return f"https://www.walkhighlands.co.uk/Forum/memberlist.php?mode=viewmap&u={user_id}"


def html_to_rows(html_path):
    rows = []
    html = requests.get(html_path).text
    for line in html.splitlines():
        m = LATLNG.search(line)
        if m:
            lat, lng = m.group(1, 2)
            loc = (float(lat), float(lng))
        else:
            m = MARKER.search(line)
            if m:
                height, name, colour = m.group(1, 2, 3)
                climbed = (colour == "blue")
                row = [name, loc, int(height), climbed]
                rows.append(row)
    return rows
