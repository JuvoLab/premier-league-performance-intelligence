"""Initialize private runtime data on first use; never publish provider files."""
import json
from settings import DATA, SOURCE_COMMIT


def ensure_data():
    from ingest import build
    from player_cards import players
    manifest = DATA / 'manifest.json'
    ready = (DATA/'performance.db').exists() and manifest.exists()
    if ready and json.loads(manifest.read_text())['commit'] != SOURCE_COMMIT:
        raise ValueError('Runtime data does not match the pinned research source.')
    if not ready:
        build()
    players()
    return SOURCE_COMMIT
