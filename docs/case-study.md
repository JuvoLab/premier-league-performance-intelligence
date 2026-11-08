# Results versus underlying performance in the 2015/16 Premier League

Status: local review candidate; isolated-environment QA complete as documented in qa-review.md. Source publication is authorized; application hosting remains deferred.

## Problem and methods

League points measure outcomes but hide the quality of chances created and conceded. We ask which clubs' observed scoring margins exceed their shot-quality margins and how those differences evolve during the season.

We use one complete StatsBomb season, avoiding incomparable xG models and incomplete league samples. Each match generates two team-perspective records. Points are 3 for a win, 1 for a draw and 0 for a loss. GD = goals for − goals against; xGD = shot xG for − shot xG against. Residual = GD − xGD. Positive values indicate a higher observed scoring margin than the xG margin. They are not a decomposition into finishing skill, goalkeeper ability and luck.

The Python pipeline downloads a versioned snapshot, checks event identifiers and shot probabilities, and validates coverage before storing team, season, match and team-match tables in SQLite. SQL joins provide traceable analytical input. Pandas aggregates results, NumPy generates seeded bootstrap samples, and Plotly/Streamlit provide interactive interpretation.

## Main findings

Across 20 teams, Pearson correlation between points and xGD is **0.8989**. This is a strong in-sample descriptive association. Twenty team observations share fixtures and are not independent; no significance test or causal claim is warranted. A squared correlation is not an out-of-sample measure of predictive accuracy.

West Ham's GD was +14 versus xGD +0.26: a **+13.74-goal** gap. Leicester's +32 versus +20.15 produced **+11.85**; Manchester United's +14 versus +3.68 produced **+10.32**. At the other end, Aston Villa's −49 versus −30.01 yielded **−18.99**, Bournemouth's −22 versus −6.35 yielded **−15.65**, and Norwich's −28 versus −20.51 yielded **−7.49**.

The temporal picture is not fixed. Crystal Palace's gap fell from **+12.34 after 19 appearances to −1.58 after 38**, implying −13.92 in the second half. Manchester United moved from **−0.68 to +10.32**, implying +11.00 in the second half. West Ham remained positive in both halves (+9.86, +3.88), Leicester likewise (+6.94, +4.92). Aston Villa remained negative (−11.15, −7.84), as did Bournemouth (−7.90, −7.75). This answers the within-season consistency question while showing why full-season totals hide changes. Unequal opposition and venue mixes limit half-season comparisons.

## Uncertainty and limits

Default five-match rolling means expose local patterns but overlapping windows are dependent and early observations are suppressed until a full window exists. Cumulative gaps show accumulated outcomes, not significance or calibrated uncertainty.

A 5,000-resample seeded bootstrap estimates an illustrative interval for the mean match residual. It assumes exchangeable independent matches. It does not model schedule, game state, serial dependence, opponent strength or error in StatsBomb xG. Intervals should not be used to select statistically significant teams from 20 simultaneous comparisons.

xG measures shot quality, not every aspect of attacking or defensive quality. Goals and xG arise during the same matches and are related by construction. Penalties, own goals, tactical choices, score effects and finishing/goalkeeping all influence interpretation. Historical data cannot answer present-day team-quality questions. One season cannot establish repeated overperformance across seasons.

## Technical implementation and validation

The implementation combines inspectable ingestion, validation, Pandas/NumPy transformations, relational SQL joins, descriptive statistics and interactive scientific communication.

Five automated tests pass in an isolated environment, including SQL/Pandas aggregate agreement and app filter checks. Event/score reconciliation passed for all 380 matches. Fresh downloads reproduced the original file hashes and database rows. Official provider attribution is displayed. Desktop/mobile and selected keyboard interactions were checked; no claim of complete accessibility conformance is made. Before publication, obtain owner approval and verify hosting on its actual operating system. Future work could assess more complete seasons from the same authorized provider if available; adding unrelated models is unnecessary.
