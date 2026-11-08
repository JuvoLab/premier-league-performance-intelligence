# Phase 1 source verification — 8 November 2026

## Proposed source

[Reza Asadi's dataset](https://github.com/RezaGooner/english-premier-league-match-dataset), inspected at commit `9e3ecdc5b85616e69044440304673ef564a8ed98`.

Actual file: `Data/EPL_Match_Data_2000_2026.csv`; 9,880 rows × **85 columns**, unlike the README's 65-column description. All 26 season codes from 0001 through 2526 have 380 rows. No duplicate full rows or season/home/away fixtures; score-derived results agree with Result. No negative goals, shots or xG were found. These checks establish internal consistency, not independent historical accuracy.

Columns include date components, team names, full/half-time goals and results, shots, shots on target, fouls, corners, cards, xG, final-season summaries, location, managers, form, trophies and VAR. The full column and missingness inventory is generated locally by `verify_source.py` in `data/audit/proposed-profile.json`.

No xG before 2018/19. In 2018/19 home xG exists for 198/380 and away xG for 197/380 rows; 2019/20–2025/26 each have 380 values per side. Completeness alone does not establish consistent provider, model, or accurate historical values. The README lists multiple upstream websites without per-value xG provenance. It also contains differing citation DOI references. Final-season fields must not be treated as information available during the season. The match-level file contains no player statistics.

The publisher states CC BY-NC 4.0, but the repository's declaration does not independently verify upstream sublicensing authority. This source is not selected for the public application because xG comparability and redistribution rights remain insufficiently traceable. No upstream websites were scraped.

## Selected alternative

StatsBomb Open Data, EPL competition 2, season 27 (2015/16): all **380 unique matches**, with raw match and event JSON available directly from the provider's repository. Season 44 (2003/04) has **38 matches**, so it is excluded as a full-league sample. The limited available EPL seasons preclude a meaningful multi-season persistence analysis.

Match JSON contains identifiers, dates, scores, teams, competition/season and metadata. Event JSON includes team and player identifiers, event type, period, shot outcomes and `shot.statsbomb_xg`. xG will only be summed from valid finite probabilities in [0,1]. Missing xG triggers failure; no imputation is permitted. Player names, shots, shot goals and shot xG support limited secondary cards; minutes, assists and ratings are omitted.

The source agreement permits research and public analytical conclusions with StatsBomb credit and logo. It restricts raw-data redistribution and commercial exploitation. Raw data and databases remain local, outside source control. The public dashboard must present analytical outputs and meet logo attribution requirements before release. This is a noncommercial research portfolio scope; the agreement is not a blanket open-source data license.

## Exact minimum metrics

Played, W/D/L, score-derived points, goals for/against, GD; shots for/against; summed shot xG/xGA and xGD; residual GD−xGD; full-window rolling means (default five matches); cumulative GD/xGD; Pearson correlation of points and xGD across teams. An illustrative seeded match-bootstrap interval describes mean residual variability under independent-match sampling, with explicit limitations. No expected-points model or causal effect is estimated.

“Consistent” means direction of residuals in non-overlapping first/second 19-appearance blocks within this season. It does not imply stable ability across seasons. Team-appearance filters are not common calendar cutoffs. Goals include own goals; shot contributions exclude own goals. Penalties remain included in provider xG.
