"""Limited verified shot contributions; no inferred minutes or attributes."""
import json
from collections import defaultdict
from ingest import DATA
import pandas as pd


def players():
    cache=DATA/'player_summary.csv'
    if cache.exists() and cache.stat().st_mtime_ns >= (DATA/'performance.db').stat().st_mtime_ns:
        return pd.read_csv(cache)
    values = defaultdict(lambda: {'shots':0,'goals':0,'xg':0.0})
    matches=json.loads((DATA/'raw/matches.json').read_text(encoding='utf-8'))
    for match in matches:
        path=DATA/f"raw/events/{match['match_id']}.json"
        for e in json.loads(path.read_text(encoding='utf-8')):
            if e['type']['name'] != 'Shot' or e['period'] not in (1,2):
                continue
            key=(e['player']['id'],e['player']['name'],e['team']['name'])
            v=values[key]; v['shots']+=1
            v['goals']+= e['shot']['outcome']['name']=='Goal'
            v['xg']+=e['shot']['statsbomb_xg']
    result=pd.DataFrame([{'player_id':k[0],'name':k[1],'team':k[2],**v} for k,v in values.items()])
    result.to_csv(cache,index=False)
    return result
