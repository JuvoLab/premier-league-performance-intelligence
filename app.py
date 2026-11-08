from pathlib import Path
import json
import plotly.express as px
import streamlit as st
from analysis import load, summarize, trends, bootstrap_gap
from settings import ROOT, DATA

st.set_page_config(page_title='Premier League Performance Intelligence', page_icon='⚽', layout='wide')
st.markdown('''<style>
.stApp {background:#0b101a;color:#edf2fa}
[data-testid="stMetric"] {background:#151e2e;border:1px solid #2c3b52;border-radius:12px;padding:16px}
h1,h2,h3 {letter-spacing:-.025em}
</style>''', unsafe_allow_html=True)
if (ROOT/'assets/juvolab-logo.png').exists():
    st.image(str(ROOT/'assets/juvolab-logo.png'),width=260)
st.caption('JUVOLAB  /  FOOTBALL PERFORMANCE RESEARCH')
st.title('Premier League Performance Intelligence')
st.write('Distinguish results from the chances teams created and conceded.')
if not (DATA/'performance.db').exists():
    st.info('Run python ingest.py to build the local database before opening the dashboard.')
    st.stop()

@st.cache_data
def get_data(version):
    return load()

d = get_data((DATA/'performance.db').stat().st_mtime_ns)
with st.sidebar:
    st.header('Explore performance')
    st.selectbox('Season', ['2015/16'])
    st.caption('One complete season. Other EPL open-data seasons are not complete league samples.')
    teams = sorted(d.team.unique())
    team = st.selectbox('Team', teams, index=teams.index('Leicester City'))
    compare = st.selectbox('Compare with', teams, index=teams.index('Arsenal'))
    window = st.slider('Rolling window (matches)',3,10,5)
    played = st.slider('Season through team appearance',5,38,38)
    st.divider()
    st.image(str(ROOT/'assets/statsbomb-logo-white.png'),width=200)
    st.caption('Data: StatsBomb Open Data · Independent noncommercial research; no affiliation or endorsement.')
    st.markdown('[Data source and user agreement](https://github.com/statsbomb/open-data)')

# Each team's first N appearances, not a common calendar cutoff.
prefix = d.sort_values(['date','match_id']).groupby('team', group_keys=False).head(played)
s = summarize(prefix); row = s[s.team == team].iloc[0]
st.subheader(team)
st.caption(f'First {played} team appearances • teams may reach this count on different dates')
cols=st.columns(4)
for col,label,value in zip(cols,['Points','Goal difference','xG difference','GD − xGD'],[row.points,row.gd,f'{row.xgd:+.1f}',f'{row.gap:+.1f}']):
    col.metric(label,value)
st.write(f'{int(row.mp)} played · {int(row.wins)} wins · {int(row.draws)} draws · {int(row.losses)} losses · Goals {int(row.gf)}–{int(row.ga)} · xG {row.xg:.1f}–{row.xga:.1f}')
tabs=st.tabs(['League overview','Season trends','Team comparison','Methods & coverage'])
def chart(fig):
    for trace in fig.data:
        trace.name={'cumulative_gd':'Actual GD','cumulative_xgd':'xG difference','rolling_gd':'Actual GD','rolling_xgd':'xG difference'}.get(trace.name,trace.name)
    fig.update_layout(template='plotly_dark',paper_bgcolor='#0b101a',plot_bgcolor='#111a28',legend_title_text='')
    st.plotly_chart(fig,use_container_width=True)
with tabs[0]:
    chart(px.scatter(s,x='xgd',y='points',hover_name='team',color='gap',color_continuous_scale='RdBu',labels={'xgd':'xG difference','points':'Points','gap':'GD − xGD'}))
    r=s.points.corr(s.xgd)
    st.write(f'Across these 20 teams, points and xG difference have Pearson r = {r:.2f}. This is a descriptive association, not a causal effect or out-of-sample accuracy estimate.')
    chart(px.bar(s.sort_values('gap'),x='gap',y='team',orientation='h',labels={'gap':'Goal difference minus xG difference','team':''}))
    st.dataframe(s.round(2),hide_index=True,use_container_width=True)
with tabs[1]:
    t=trends(prefix,team,window)
    chart(px.line(t,x='played',y=['cumulative_gd','cumulative_xgd'],labels={'played':'Team appearance','value':'Cumulative goal difference'}))
    chart(px.line(t,x='played',y=['rolling_gd','rolling_xgd'],labels={'played':'Team appearance','value':f'{window}-match mean difference'}))
    interval=bootstrap_gap(t.gap)
    if interval is not None:
        st.write(f'Mean match gap: {t.gap.mean():+.2f}; illustrative 95% bootstrap interval [{interval[0]:+.2f}, {interval[1]:+.2f}] goals per match.')
    st.caption('Bootstrap resamples matches as independent observations. Schedule, opponent strength, serial dependence, and uncertainty in the xG model are not represented. Overlapping rolling windows are dependent.')
with tabs[2]:
    st.dataframe(s[s.team.isin([team,compare])].set_index('team').T.round(2),use_container_width=True)
    st.write('A positive GD − xGD means the observed scoring margin exceeded the summed shot-quality margin. It does not prove luck, finishing skill, or future regression.')
    if played == 38:
        from player_cards import players
        @st.cache_data
        def shot_players(version):
            return players()
        p=shot_players((DATA/'performance.db').stat().st_mtime_ns)
        p=p[p.team==team].sort_values('goals',ascending=False)
        if not p.empty:
            st.subheader('Player shot contributions')
            name=st.selectbox('Player',p.name.tolist())
            player=p[p.name==name].iloc[0]
            with st.container(border=True):
                credits=json.loads((ROOT/'assets/players/credits.json').read_text())
                photo=credits.get(str(int(player.player_id)))
                if photo:
                    portrait,details=st.columns([1,3])
                    portrait.image(str(ROOT/'assets/players'/photo['file']),width=160)
                else:
                    details=st.container()
                with details:
                    st.caption('PLAYER PROFILE · 2015/16')
                    st.subheader(name)
                    st.write(team)
                    a,b,c=st.columns(3)
                    a.metric('Shot goals',int(player.goals)); b.metric('Shots',int(player.shots)); c.metric('Shot xG',f'{player.xg:.2f}')
                if photo:
                    st.caption(f"Photo: {photo['author']} · {photo['note']}")
                    st.markdown(f"[Photo source]({photo['source']}) · [{photo['license']}]({photo['license_url']})")
            st.caption('Full-season verified shot events only. Own goals excluded. Minutes, assists, positions and ratings are not inferred. Player cards require local raw events.')
with tabs[3]:
    st.write('StatsBomb Open Data • Premier League 2015/16 • 380 matches • 20 teams • 38 matches per team. xG is summed from verified shot events, including penalties. Scoreline goals include own goals; shot goals alone do not.')
    st.write('No expected-points model, betting predictions, causal claims, or fabricated player attributes. Five-match rolling means require a full window. Early-season rankings are unstable. One season cannot establish persistence across seasons.')
    st.image(str(ROOT/'assets/statsbomb-logo-white.png'),width=240)
    st.write('Data: StatsBomb Open Data. Independent noncommercial research; findings are the author’s and do not imply endorsement by StatsBomb or Hudl. Raw events and the local database are excluded from source publication under the source user agreement.')
    st.link_button('Source and terms','https://github.com/statsbomb/open-data')
