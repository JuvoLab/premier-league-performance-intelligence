-- Reproduce team totals in SQL independently of the Pandas aggregation.
SELECT t.name AS team, COUNT(*) AS mp, SUM(tm.points) AS points,
       SUM(tm.gf) AS gf, SUM(tm.ga) AS ga,
       SUM(tm.gf-tm.ga) AS gd, SUM(tm.xg-tm.xga) AS xgd,
       SUM((tm.gf-tm.ga)-(tm.xg-tm.xga)) AS gap
FROM team_match tm
JOIN teams t ON t.team_id=tm.team_id
JOIN matches m ON m.match_id=tm.match_id
WHERE m.season_id=?
GROUP BY t.team_id,t.name
ORDER BY points DESC,gd DESC,gf DESC;
