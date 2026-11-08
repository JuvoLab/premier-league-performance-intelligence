import json
import bootstrap

def test_warm_start_does_not_download(monkeypatch, tmp_path):
    monkeypatch.setattr(bootstrap,'DATA',tmp_path)
    (tmp_path/'performance.db').touch()
    (tmp_path/'manifest.json').write_text(json.dumps({'commit':bootstrap.SOURCE_COMMIT}))
    import ingest, player_cards
    monkeypatch.setattr(ingest,'build',lambda: (_ for _ in ()).throw(AssertionError('Unexpected download')))
    monkeypatch.setattr(player_cards,'players',lambda: None)
    assert bootstrap.ensure_data()==bootstrap.SOURCE_COMMIT

def test_cold_start_builds_before_player_summary(monkeypatch,tmp_path):
    monkeypatch.setattr(bootstrap,'DATA',tmp_path)
    import ingest, player_cards
    calls=[]
    monkeypatch.setattr(ingest,'build',lambda: calls.append('build'))
    monkeypatch.setattr(player_cards,'players',lambda: calls.append('players'))
    bootstrap.ensure_data()
    assert calls==['build','players']
