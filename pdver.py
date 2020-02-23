import numpy as np
from scipy.linalg import *
import psycopg2
import pandas as pd
import pymc3 as pymc
import theano.tensor as tt
import math
import matplotlib.pyplot as plt
import seaborn as sns
def getdata(sql):
    try:
        conn = psycopg2.connect("dbname='mustwinbet' user='andy' host='localhost' password='andy' ")
    except:
        print ("I am unable to connect to the database")

    #cur=conn.cursor()


    #cur.execute(sql)
    dfh=pd.read_sql_query(sql, conn)
    conn.close()
    return dfh

def process():    
    df =pd.DataFrame()
    sql="select hometeam home,awayteam away,fthg home_score,ftag away_score from rescuttmp \
    where matchdate > '31-aug-2015' and div='E0' \
    ;"

    df=getdata(sql)

    teams = df.home.unique()
    teams = pd.DataFrame(teams, columns=['team'])
    teams['i'] = teams.index
    teams.head()
    #print (teams)

    df = pd.merge(df, teams, left_on='home', right_on='team', how='left')
    df = df.rename(columns = {'i': 'i_home'}).drop('team', 1)
    df = pd.merge(df, teams, left_on='away', right_on='team', how='left')
    df = df.rename(columns = {'i': 'i_away'}).drop('team', 1)
    df.head()

    observed_home_goals = df.home_score.values
    observed_away_goals = df.away_score.values
    home_team = df.i_home.values
    away_team = df.i_away.values
    num_teams = len(df.i_home.unique())
    num_games = len(home_team)

    g = df.groupby('i_away')
    att_starting_points = np.log(g.away_score.mean())
    g = df.groupby('i_home')
    def_starting_points = -np.log(g.away_score.mean())

    model = pymc.Model()
    with pymc.Model() as model:

        #hyperpriors
        home = pymc.Normal('home', 0, .0001)
        tau_att = pymc.Gamma('tau_att', .1, .1)
        tau_def = pymc.Gamma('tau_def', .1, .1)
        intercept = pymc.Normal('intercept', 0, .0001)


        #team-specific parameters
        atts_star = pymc.Normal("atts_star", 
                        mu=0, 
                        tau=tau_att, 
                        shape=num_teams) 
        defs_star = pymc.Normal("defs_star", 
                        mu=0, 
                        tau=tau_def, 
                        shape=num_teams) 
        atts        = pymc.Deterministic('atts', atts_star - tt.mean(atts_star))
        defs        = pymc.Deterministic('defs', defs_star - tt.mean(defs_star))
        home_theta  = tt.exp(intercept + home + atts[home_team] + defs[away_team])
        away_theta  = tt.exp(intercept + atts[away_team] + defs[home_team])
    
        # likelihood of observed data
        home_goals = pymc.Poisson('home_goals', 
                              mu=home_theta, 
                              observed=observed_home_goals 
                              )
        away_goals = pymc.Poisson('away_goals', 
                              mu=away_theta, 
                              observed=observed_away_goals 
                              )
    """
        mcmc = pymc.MCMC([home, intercept, tau_att, tau_def, 
                          home_theta, away_theta, 
                          atts_star, defs_star, atts, defs, 
                          home_goals, away_goals])
        map_ = pymc.MAP( mcmc )
        map_.fit()
        mcmc.sample(200000, 40000, 20)
    """
    with model:
        start = pymc.find_MAP()
        step = pymc.NUTS(state=start)
        trace = pymc.sample(2000, step, start=start)

        pymc.traceplot(trace)
        return trace
        #print (trace.original_varnames)
        #print (home_goals[0])
    #pymc.plot_posterior(trace)
    """ KEEP BELOW
    print (trace['atts'][4])
    df_trace = pymc.trace_to_dataframe(trace[:1000])
    import seaborn as sns
    df_trace_att = df_trace[['atts_star__0','atts_star__1',
     'atts_star__2',
     'atts_star__3',
     'atts_star__4',
     'atts_star__5']]
    df_trace_att.rename(columns={'atts_star__0':'atts_star_arsenal','atts_star__1':'atts_star_crystal_palace',
     'atts_star__2':'atts_star_everton',
     'atts_star__3':'atts_star_manutd',
     'atts_star__4':'atts_star_norwich',
     'atts_star__5':'atts_star_watford'}, inplace=True)
    _ = sns.pairplot(df_trace_att)
    """ 
    #END KEEP
    """
    print(atts.eval())
    
df_hpd = pd.DataFrame(atts.stats()['95% HPD interval'], 
                      columns=['hpd_low', 'hpd_high'], 
                      index=teams.team.values)
df_median = pd.DataFrame(atts.stats()['quantiles'][50], 
                         columns=['hpd_median'], 
                         index=teams.team.values)
df_hpd = df_hpd.join(df_median)
df_hpd['relative_lower'] = df_hpd.hpd_median - df_hpd.hpd_low
df_hpd['relative_upper'] = df_hpd.hpd_high - df_hpd.hpd_median
df_hpd = df_hpd.sort_index(by='hpd_median')
df_hpd = df_hpd.reset_index()
df_hpd['x'] = df_hpd.index + .5


fig, axs = plt.subplots(figsize=(10,4))
axs.errorbar(df_hpd.x, df_hpd.hpd_median, 
             yerr=(df_hpd[['relative_lower', 'relative_upper']].values).T, 
             fmt='o')
axs.set_title('HPD of Attack Strength, by Team')
axs.set_xlabel('Team')
axs.set_ylabel('Posterior Attack Strength')
_= axs.set_xticks(df_hpd.index + .5)
_= axs.set_xticklabels(df_hpd['index'].values, rotation=45)
"""
def simulate_season(trace):
    """
    Simulate a season once, using one random draw from the mcmc chain. 
    """
    #num_samples = atts.trace().shape[0]
    #df_trace = pymc.trace_to_dataframe(trace[:1000])
    num_samples=trace['atts'].shape[0]
    draw = np.random.randint(0, num_samples)
    atts_draw = pd.DataFrame({'att': trace['atts'][draw, :],})
    defs_draw = pd.DataFrame({'def': trace['defs'][draw, :],})
    home_draw = trace['home'][draw]
    intercept_draw = trace['intercept'][draw]
    season = pd.copy()
    season = pd.merge(season, atts_draw, left_on='i_home', right_index=True)
    season = pd.merge(season, defs_draw, left_on='i_home', right_index=True)
    season = season.rename(columns = {'att': 'att_home', 'def': 'def_home'})
    season = pd.merge(season, atts_draw, left_on='i_away', right_index=True)
    season = pd.merge(season, defs_draw, left_on='i_away', right_index=True)
    season = season.rename(columns = {'att': 'att_away', 'def': 'def_away'})
    season['home'] = home_draw
    season['intercept'] = intercept_draw
    season['home_theta'] = season.apply(lambda x: math.exp(x['intercept'] + 
                                                           x['home'] + 
                                                           x['att_home'] + 
                                                           x['def_away']), axis=1)
    season['away_theta'] = season.apply(lambda x: math.exp(x['intercept'] + 
                                                           x['att_away'] + 
                                                           x['def_home']), axis=1)
    season['home_goals'] = season.apply(lambda x: np.random.poisson(x['home_theta']), axis=1)
    season['away_goals'] = season.apply(lambda x: np.random.poisson(x['away_theta']), axis=1)
    season['home_outcome'] = season.apply(lambda x: 'win' if x['home_goals'] > x['away_goals'] else 
                                                    'loss' if x['home_goals'] < x['away_goals'] else 'draw', axis=1)
    season['away_outcome'] = season.apply(lambda x: 'win' if x['home_goals'] < x['away_goals'] else 
                                                    'loss' if x['home_goals'] > x['away_goals'] else 'draw', axis=1)
    season = season.join(pd.get_dummies(season.home_outcome, prefix='home'))
    season = season.join(pd.get_dummies(season.away_outcome, prefix='away'))
    return season


def create_season_table(season):
    """
    Using a season dataframe output by simulate_season(), create a summary dataframe with wins, losses, goals for, etc.
    
    """
    g = season.groupby('i_home')    
    home = pd.DataFrame({'home_goals': g.home_goals.sum(),
                         'home_goals_against': g.away_goals.sum(),
                         'home_wins': g.home_win.sum(),
                         'home_draws': g.home_draw.sum(),
                         'home_losses': g.home_loss.sum()
                         })
    g = season.groupby('i_away')    
    away = pd.DataFrame({'away_goals': g.away_goals.sum(),
                         'away_goals_against': g.home_goals.sum(),
                         'away_wins': g.away_win.sum(),
                         'away_draws': g.away_draw.sum(),
                         'away_losses': g.away_loss.sum()
                         })
    df = home.join(away)
    df['wins'] = df.home_wins + df.away_wins
    df['draws'] = df.home_draws + df.away_draws
    df['losses'] = df.home_losses + df.away_losses
    df['points'] = df.wins * 3 + df.draws
    df['gf'] = df.home_goals + df.away_goals
    df['ga'] = df.home_goals_against + df.away_goals_against
    df['gd'] = df.gf - df.ga
    df = pd.merge(teams, df, left_on='i', right_index=True)
    df = df.sort_index(by='points', ascending=False)
    df = df.reset_index()
    df['position'] = df.index + 1
    df['champion'] = (df.position == 1).astype(int)
    df['qualified_for_CL'] = (df.position < 5).astype(int)
    df['relegated'] = (df.position > 17).astype(int)
    return df  
    
def simulate_seasons(n=100):
    dfs = []
    trace=process()
    for i in range(n):
        s = simulate_season(trace)
        t = create_season_table(s)
        t['iteration'] = i
        dfs.append(t)
    return pd.concat(dfs, ignore_index=True)

simuls=simulate_seasons(100)

ax = simuls.points[simuls.team == 'Leicester'].hist(figsize=(7,5))
median = simuls.points[simuls.team == 'MNC'].median()
ax.set_title('Arsenal: 2015-16 points, 1000 simulations')
ax.plot([median, median], ax.get_ylim())
plt.annotate('Median: %s' % median, xy=(median + 1, ax.get_ylim()[1]-10))

g = simuls.groupby('team')
season_hdis = pd.DataFrame({'points_lower': g.points.quantile(.05),
                            'points_upper': g.points.quantile(.95),
                            'goals_for_lower': g.gf.quantile(.05),
                            'goals_for_median': g.gf.median(),
                            'goals_for_upper': g.gf.quantile(.95),
                            'goals_against_lower': g.ga.quantile(.05),
                            'goals_against_upper': g.ga.quantile(.95),
                            })
df_observed =pd.DataFrame()
sql="select team,pts Pts,GF,GA from prem_table"

df_observed=getdata(sql)
season_hdis = pd.merge(season_hdis, df_observed, left_index=True, right_on='team')
column_order = ['team', 'points_lower', 'Pts', 'points_upper', 
                'goals_for_lower', 'GF', 'goals_for_median', 'goals_for_upper',
                'goals_against_lower', 'GA', 'goals_against_upper',]
season_hdis = season_hdis[column_order]
season_hdis['relative_goals_upper'] = season_hdis.goals_for_upper - season_hdis.goals_for_median
season_hdis['relative_goals_lower'] = season_hdis.goals_for_median - season_hdis.goals_for_lower
season_hdis = season_hdis.sort_index(by='GF')
season_hdis = season_hdis.reset_index()
season_hdis['x'] = season_hdis.index + .5
season_hdis

fig, axs = plt.subplots(figsize=(10,6))
axs.scatter(season_hdis.x, season_hdis.GF, c=sns.palettes.color_palette()[4], zorder = 10, label='Actual Goals For')
axs.errorbar(season_hdis.x, season_hdis.goals_for_median, 
             yerr=(season_hdis[['relative_goals_lower', 'relative_goals_upper']].values).T, 
             fmt='s', c=sns.palettes.color_palette()[5], label='Simulations')
axs.set_title('Actual Goals For, and 90% Interval from Simulations, by Team')
axs.set_xlabel('Team')
axs.set_ylabel('Goals Scored')
axs.set_xlim(0, 20)
axs.legend()
_= axs.set_xticks(season_hdis.index + .5)
_= axs.set_xticklabels(season_hdis['team'].values, rotation=45)