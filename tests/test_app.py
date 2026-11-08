from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_team_and_prefix_filters():
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=120)
    assert not app.exception
    assert app.metric[0].value=='81'
    app.sidebar.selectbox[1].select('Arsenal').run(timeout=120)
    assert not app.exception
    assert app.metric[0].value=='71'
    app.sidebar.slider[1].set_value(19).run(timeout=120)
    assert not app.exception
    assert app.metric[0].value=='39'
