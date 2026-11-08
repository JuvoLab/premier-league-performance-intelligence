-- One row per team per match; parameter binding keeps season filtering explicit.
SELECT m.date, s.name AS season, t.name AS team,
       o.name AS opponent, tm.*
FROM team_match tm
JOIN matches m ON tm.match_id=m.match_id
JOIN teams t ON tm.team_id=t.team_id
JOIN teams o ON tm.opponent_id=o.team_id
JOIN seasons s ON m.season_id=s.season_id
WHERE s.name=?
ORDER BY m.date, m.match_id, tm.team_id;
