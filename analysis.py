"""Descriptive comparisons, not predictions or causal estimates."""
import sqlite3
import numpy as np
import pandas as pd
from settings import ROOT, DATA


def load(season='2015/16'):
    with sqlite3.connect(f'file:{DATA / "performance.db"}?mode=ro', uri=True) as con:
        df = pd.read_sql_query((ROOT/'queries/team_matches.sql').read_text(), con, params=(season,))
    df = df.loc[:, ~df.columns.duplicated()].copy()
    con.close()
    df['date'] = pd.to_datetime(df.date)
    df['gd'] = df.gf - df.ga
    df['xgd'] = df.xg - df.xga
    df['gap'] = df.gd - df.xgd
    return df


def summarize(df):
    result = df.groupby('team').agg(mp=('gf','size'), points=('points','sum'), gf=('gf','sum'), ga=('ga','sum'),
        xg=('xg','sum'), xga=('xga','sum'), gd=('gd','sum'), xgd=('xgd','sum'), gap=('gap','sum'),
        gap_sd=('gap','std')).reset_index()
    for label, condition in [('wins',df.gf > df.ga),('draws',df.gf == df.ga),('losses',df.gf < df.ga)]:
        result[label] = result.team.map(df.assign(value=condition).groupby('team').value.sum())
    return result.sort_values(['points','gd','gf'], ascending=False).reset_index(drop=True)


def trends(df, team, window=5):
    d = df[df.team == team].sort_values(['date','match_id']).copy()
    d['played'] = np.arange(1, len(d)+1)
    for c in ['gd','xgd','gap','points']:
        d['cumulative_'+c] = d[c].cumsum()
        d['rolling_'+c] = d[c].rolling(window, min_periods=window).mean()
    return d


def bootstrap_gap(values, seed=2026, repetitions=5000):
    """Illustrative iid match bootstrap of mean residual; not xG-model uncertainty."""
    a = np.asarray(values, dtype=float)
    if len(a) < 10:
        return None
    rng = np.random.default_rng(seed)
    means = rng.choice(a, size=(repetitions,len(a)), replace=True).mean(axis=1)
    return np.quantile(means,[.025,.975])


if __name__ == '__main__':
    d = load(); summary = summarize(d)
    summary.to_csv(DATA/'team_summary.csv', index=False)
    print(summary[['team','points','gd','xgd','gap']].to_string(index=False))
    print('Team-season Pearson r (points, xGD):', summary.points.corr(summary.xgd))
