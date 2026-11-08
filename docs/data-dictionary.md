# Analytical data dictionary

Source: StatsBomb Open Data, competition 2, season 27, commit `4b73468fc5b0f1950f9f66fada70ad3a4f9327cb`.

| Table / field | Meaning and units |
|---|---|
| seasons.season_id / name | Provider season identifier / readable season |
| teams.team_id / name | Provider team identifier / name |
| matches.match_id | Provider unique fixture identifier |
| matches.season_id | Foreign key to seasons |
| matches.date | ISO calendar date; chronology uses date then match ID |
| matches.home_id / away_id | Foreign keys to teams |
| team_match.match_id / team_id | Composite primary key, team perspective of fixture |
| opponent_id | Opposing team identifier |
| venue | home or away |
| gf / ga | Scoreline goals scored/conceded, including own goals |
| points | 3 win, 1 draw, 0 loss; calculated from scoreline |
| shots / shots_against | Count of provider Shot events in regulation halves |
| xg / xga | Sum of provider statsbomb_xg per shot for/against, penalties included |
| gd / xgd | GF−GA / xG−xGA, goals |
| gap | GD−xGD, goals; positive = larger observed scoring margin |
| mp / wins / draws / losses | Team appearance and outcome counts |
| gap_sd | Sample standard deviation of match residuals, ddof=1 |
| played | Appearance index in chronological team order |
| cumulative_* | Running sum through appearance, inclusive |
| rolling_* | Trailing full-window mean, goals or points per match |
| player shot goals | Goal outcomes of Shot events; own goals excluded |

No observed shot xG is imputed. Zero-shot matches legitimately sum to zero. First window−1 rolling values are undefined; bootstrap intervals require at least 10 observations. Database fields contain no player minutes, assists, ratings or fabricated attributes. A single season is deliberately retained; no mixed-provider xG is used.
