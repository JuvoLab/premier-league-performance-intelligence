"""Fetch a pinned StatsBomb season; validate before producing a local database."""
import concurrent.futures
import hashlib
import json
import sqlite3
import time
import urllib.request
import numpy as np
from settings import ROOT, DATA, SOURCE_COMMIT


def fetch(url, path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                raw = response.read()
            value = json.loads(raw)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            return value
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def shot_summary(events, team_id):
    shots = [e for e in events if e['type']['name'] == 'Shot' and e['team']['id'] == team_id and e['period'] in (1, 2)]
    xg = [e['shot'].get('statsbomb_xg') for e in shots]
    if not all(isinstance(x, (int, float)) and np.isfinite(x) and 0 <= x <= 1 for x in xg):
        raise ValueError('Missing or invalid shot xG; never impute')
    return len(shots), float(sum(xg))


def build():
    DATA.mkdir(exist_ok=True)
    pin = DATA / 'source.json'
    if pin.exists():
        commit = json.loads(pin.read_text())['commit']
        if commit != SOURCE_COMMIT:
            raise ValueError('Cached source differs from the pinned source; use a fresh data directory')
    else:
        commit = SOURCE_COMMIT
        pin.write_text(json.dumps({'commit': commit}, indent=2))
    base = f'https://raw.githubusercontent.com/statsbomb/open-data/{commit}/'
    matches = fetch(base + 'data/matches/2/27.json', DATA / 'raw/matches.json')
    if len(matches) != 380 or len({m['match_id'] for m in matches}) != 380:
        raise ValueError('Expected 380 unique fixtures')

    def process(m):
        events = fetch(base + f"data/events/{m['match_id']}.json", DATA / f"raw/events/{m['match_id']}.json")
        if len({e['id'] for e in events}) != len(events):
            raise ValueError('Duplicate event identifiers')
        if not {1, 2}.issubset({e['period'] for e in events if e['type']['name'] == 'Half End'}):
            raise ValueError('Incomplete match event stream')
        for side in ['home', 'away']:
            tid = m[side+'_team'][side+'_team_id']
            scored = sum(e['type']['name']=='Shot' and e.get('shot',{}).get('outcome',{}).get('name')=='Goal' and e['team']['id']==tid for e in events)
            own = sum(e['type']['name']=='Own Goal Against' and e['team']['id']!=tid for e in events)
            if scored + own != m[side+'_score']:
                raise ValueError(f"Event/score mismatch in {m['match_id']}")
        rows = []
        for side, opponent in [('home', 'away'), ('away', 'home')]:
            t = m[side + '_team']; other = m[opponent + '_team']
            tid = t[side + '_team_id']; oid = other[opponent + '_team_id']
            shots, xg = shot_summary(events, tid)
            shots_against, xga = shot_summary(events, oid)
            gf, ga = m[side + '_score'], m[opponent + '_score']
            rows.append((m['match_id'], tid, oid, side, gf, ga, 3 if gf > ga else 1 if gf == ga else 0, shots, shots_against, xg, xga))
        return rows

    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for i, result in enumerate(pool.map(process, matches), 1):
            rows.extend(result)
            if i % 40 == 0:
                print(f'Validated {i}/380 matches', flush=True)
    db = DATA / 'performance.tmp.db'
    with sqlite3.connect(db) as con:
        con.executescript('''
        PRAGMA foreign_keys=ON;
        DROP TABLE IF EXISTS team_match; DROP TABLE IF EXISTS matches;
        DROP TABLE IF EXISTS teams; DROP TABLE IF EXISTS seasons;
        CREATE TABLE seasons(season_id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
        CREATE TABLE teams(team_id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
        CREATE TABLE matches(match_id INTEGER PRIMARY KEY, season_id INTEGER NOT NULL REFERENCES seasons,
          date TEXT NOT NULL, home_id INTEGER NOT NULL REFERENCES teams, away_id INTEGER NOT NULL REFERENCES teams,
          CHECK(home_id != away_id), UNIQUE(season_id,home_id,away_id));
        CREATE TABLE team_match(match_id INTEGER REFERENCES matches, team_id INTEGER REFERENCES teams,
          opponent_id INTEGER REFERENCES teams, venue TEXT CHECK(venue IN ('home','away')),
          gf INTEGER CHECK(gf>=0), ga INTEGER CHECK(ga>=0), points INTEGER CHECK(points IN (0,1,3)),
          shots INTEGER, shots_against INTEGER, xg REAL CHECK(xg>=0), xga REAL CHECK(xga>=0),
          PRIMARY KEY(match_id,team_id));
        INSERT INTO seasons VALUES (27,'2015/16');
        ''')
        teams = {m[s+'_team'][s+'_team_id']: m[s+'_team'][s+'_team_name'] for m in matches for s in ['home','away']}
        con.executemany('INSERT INTO teams VALUES (?,?)', sorted(teams.items()))
        con.executemany('INSERT INTO matches VALUES (?,?,?,?,?)', [(m['match_id'],27,m['match_date'],m['home_team']['home_team_id'],m['away_team']['away_team_id']) for m in matches])
        con.executemany('INSERT INTO team_match VALUES (?,?,?,?,?,?,?,?,?,?,?)', rows)
        counts = con.execute('SELECT COUNT(*) FROM team_match GROUP BY team_id').fetchall()
        if len(counts) != 20 or any(n != 38 for (n,) in counts):
            raise ValueError('Incomplete team coverage')
        if con.execute('PRAGMA foreign_key_check').fetchall():
            raise ValueError('Broken foreign keys')
    con.close()
    db.replace(DATA / 'performance.db')
    manifest = {'commit':commit, 'matches':380, 'team_matches':760, 'files':{str(p.relative_to(DATA)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (DATA/'raw').rglob('*.json')}}
    (DATA/'manifest.json').write_text(json.dumps(manifest, indent=2))
    print('Database built; raw files and database must not be committed.')


if __name__ == '__main__':
    build()
