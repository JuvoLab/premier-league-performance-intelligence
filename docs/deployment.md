# Public deployment

Dashboard: https://juvolab-premier-league.streamlit.app/

Source: https://github.com/JuvoLab/premier-league-performance-intelligence

Hosted on Streamlit Community Cloud, branch `main`, entry point `app.py`, Python 3.12 (observed cloud patch version 3.12.16). Provider data are fetched directly into private runtime storage on first use, validated, and reused across sessions. Raw data and SQLite files remain outside GitHub. A cold container or resumed sleeping app may take time to initialize; the app displays a preparation message.

Deployment verification completed 9 November 2026:

- Public dashboard loads with JuvoLab branding and all 380 matches.
- Team selection changes Leicester's 81 points to Arsenal's 71.
- Arsenal's first 19 appearances show 39 points with updated trend views.
- Team comparison and Jamie Vardy's photo card display 24 shot goals, 118 shots, and 22.30 shot xG, with photo credit and license.
- The app loads successfully after a dependency update and warm restart.
- Seven local automated tests pass, including automatic cold and cached initialization. The final GitHub Actions run is linked from the repository's Actions tab.

`pyarrow==24.0.0` is pinned to match the compatible version selected by the hosting platform. The first incomplete Python 3.14 deployment was removed with explicit approval and replaced with Python 3.12. No other app was changed. Future Python-version changes on Community Cloud require recreating the deployment; select the version in Advanced settings and verify it persists before deploying.
