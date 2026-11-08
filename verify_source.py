"""Re-run the Phase 1 audit. Raw licensed data remain local and ignored by Git."""
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent


def audit():
    path = ROOT / 'data/audit/proposed.csv'
    df = pd.read_csv(path, dtype={'Season': str})
    numeric = ['HomeGoal', 'AwayGoal', 'HomeShot', 'AwayShot', 'XGHome', 'XGAway']
    report = {
        'source_commit': '9e3ecdc5b85616e69044440304673ef564a8ed98',
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'shape': list(df.shape), 'columns': list(df.columns),
        'missing_by_column': df.isna().sum().to_dict(),
        'duplicate_rows': int(df.duplicated().sum()),
        'duplicate_fixtures': int(df.duplicated(['Season', 'HomeTeam', 'AwayTeam']).sum()),
        'negative_values': {c: int((df[c] < 0).sum()) for c in numeric},
        'result_disagreements': int((df.Result != df.apply(lambda r: 'H' if r.HomeGoal > r.AwayGoal else 'A' if r.HomeGoal < r.AwayGoal else 'D', axis=1)).sum()),
        'seasons': df.groupby('Season').agg(matches=('Season', 'size'), home_xg=('XGHome', 'count'), away_xg=('XGAway', 'count')).reset_index().to_dict('records'),
    }
    (ROOT / 'data/audit/proposed-profile.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['columns','missing_by_column','seasons']}, indent=2))
    return report


if __name__ == '__main__':
    audit()
