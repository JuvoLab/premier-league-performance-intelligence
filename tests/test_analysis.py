import numpy as np
from analysis import load, summarize, trends, bootstrap_gap
from ingest import shot_summary

def test_shots_not_invented():
    assert shot_summary([],1)==(0,0)
    import pytest
    with pytest.raises(ValueError):
        shot_summary([{'type':{'name':'Shot'},'team':{'id':1},'period':1,'shot':{}}],1)
    for value in [-.1,1.1,float('nan'),float('inf')]:
        with pytest.raises(ValueError):
            shot_summary([{'type':{'name':'Shot'},'team':{'id':1},'period':1,'shot':{'statsbomb_xg':value}}],1)

def test_complete_database_and_symmetry():
    d=load()
    assert len(d)==760
    assert d.groupby('team').size().eq(38).all()
    assert d.gf.sum()==d.ga.sum()==1026
    assert np.isclose(d.xg.sum(),d.xga.sum())
    assert d.groupby('match_id').gd.sum().eq(0).all()
    assert np.allclose(d.groupby('match_id').xgd.sum(),0)
    s=summarize(d)
    leicester=s[s.team=='Leicester City'].iloc[0]
    assert leicester.points==81
    assert leicester.gf==68 and leicester.ga==36

def test_temporal_prefix_and_bootstrap():
    d=load(); team=d.team.iloc[0]
    full=trends(d,team)
    prefix=trends(d[d.date<=full.date.iloc[9]],team)
    assert np.allclose(full.cumulative_gap.iloc[:len(prefix)],prefix.cumulative_gap)
    assert full.rolling_gd.iloc[:4].isna().all()
    assert bootstrap_gap([1]*9) is None
    assert np.allclose(bootstrap_gap([1]*38),[1,1])

def test_sql_pandas_agreement():
    import sqlite3
    import pandas as pd
    from analysis import ROOT, DATA
    with sqlite3.connect(DATA/'performance.db') as con:
        sql=pd.read_sql_query((ROOT/'queries/season_summary.sql').read_text(),con,params=(27,)).set_index('team').sort_index()
    py=summarize(load()).set_index('team').sort_index()
    for column in sql.columns:
        assert np.allclose(sql[column],py[column])
