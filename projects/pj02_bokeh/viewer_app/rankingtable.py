import pandas as pd
import bokeh.plotting
import bokeh.models as bmodels
import bokeh.models.widgets as bmw
import bokeh.layouts as blt
import bokeh.plotting as plt
import bokeh.palettes as bpalettes
import bokeh.transform as btransform
import bokeh.io


class rankingTable:

    def __init__(self, data):
        self.data = data
        self.df = None
        self.datatable = None
        self.layout = None

    def df_ranktable(self):
        dft = self.data.teams.copy()
        dft = dft.rename(columns={'name': 'team'})
        dft = dft.set_index(['team'])
        df = dft.filter(['team', 'matches_played'])
        dftotal = self.data.enum_measures.copy()
        dfauto = dftotal[dftotal.phase == 'auto']
        shootertasks = ['launchLower', 'launchOuter', 'launchInner']
        dfautotask = dfauto[dfauto.task.isin(shootertasks)]
        dfautotask = dfautotask.groupby(['team', 'task']).sum()
        dfautotask = dfautotask.filter(['team', 'task', 'successes'])
        dfautotask = dfautotask.unstack()
        dfautotask.columns = dfautotask.columns.droplevel()
        grouped = dftotal.groupby(['team', 'task']).sum()
        total = grouped.filter(['team', 'task', 'successes'])
        total = total.unstack()
        total.columns = total.columns.droplevel()
        total['matches'] = df['matches_played']
        # total['autoLower'] = dfautotask['launchLower']
        total['autoOuter'] = dfautotask['launchOuter']
        total['autoInner'] = dfautotask['launchInner']
        total = total.fillna(0)
        total['teleLower'] = total['launchLower']
        total['teleOuter'] = total['launchOuter'] - total['autoOuter']
        total['teleInner'] = total['launchInner'] - total['autoInner']
        total['movePoints'] = total['movedAuto'] * 5
        # total['autoLowerPoints'] = total['autoLower'] * 2
        total['autoOuterPoints'] = total['autoOuter'] * 4
        total['autoInnerPoints'] = total['autoInner'] * 6
        total['teleInnerPoints'] = total['autoInner'] * 3
        total['teleLowerPoints'] = total['teleLower'] * 1
        total['teleOuterPoints'] = total['teleOuter'] * 2
        total['climb'] = total['climbPosition_Center'] + total['climbPosition_Side']
        total['climbpoints'] = total['climb'] * 25
        total['parkpoints'] = total['climbPosition_Park'] * 5
        # total['positionControlPoints'] = total['positionControl'] * 25
        # total['rotationControlPoints'] = total['rotationControl'] * 15
        total['points'] = (total['autoOuterPoints'] + total['teleLowerPoints'] +
                           total['teleOuterPoints'] + total['autoInnerPoints'] + total['teleInnerPoints'] +
                           total['climb'] + total['climbpoints'] + total['parkpoints'])
                           # total['positionControlPoints'] + total['rotationControlPoints'])
        average = total.div(total.matches, axis=0)
        for x in range(len(average.columns)):
            average.rename(columns={average.columns[x]: ('avg_' + average.columns[x])}, inplace=True)
        complete = total.merge(average, left_index=True, right_index=True)
        self.df = complete.sort_values(by='avg_points')
        return self.df

    def total_rt(self):
        Rank_cds = bmodels.ColumnDataSource(self.df)
        fixed2 = bmw.NumberFormatter(format='0.00')
        cols = [
            bmw.TableColumn(field='team', title='Team'),
            bmw.TableColumn(field='avg_points', title='Average Points', formatter=fixed2),
            # bmw.TableColumn(field='avg_autoLower', title='Average Shoot Lower Auto', formatter=fixed2),
            bmw.TableColumn(field='avg_autoOuter', title='Average Shoot Outer Auto', formatter=fixed2),
            bmw.TableColumn(field='avg_autoInner', title='Average Shoot Inner Auto', formatter=fixed2),
            bmw.TableColumn(field='avg_teleLower', title='Average Shoot Lower Teleop', formatter=fixed2),
            bmw.TableColumn(field='avg_teleOuter', title='Average Shoot Outer Teleop', formatter=fixed2),
            bmw.TableColumn(field='avg_teleInner', title='Average Shoot Inner Teleop', formatter=fixed2),
            bmw.TableColumn(field='avg_launchLower', title='Average Shoot Lower', formatter=fixed2),
            bmw.TableColumn(field='avg_launchOuter', title='Average Shoot Upper', formatter=fixed2),
            # bmw.TableColumn(field='positionControl', title='Total position control', formatter=fixed2),
            # bmw.TableColumn(field='rotationControl', title='Total Rotation Control', formatter=fixed2),
            bmw.TableColumn(field='movedAuto', title='Total moved auto', formatter=fixed2),
            bmw.TableColumn(field='climb', title='Total Climbs', formatter=fixed2)
        ]
        self.datatable = bmw.DataTable(source=Rank_cds, columns=cols, width=1600, height=380)
        return self.datatable

    def create_layout(self):
        self.df = self.df_ranktable()
        self.datatable = self.total_rt()
        self.layout = blt.row(self.datatable)
        return self.layout

    def panel(self):
        self.layout = self.create_layout()
        return bmodels.Panel(child=self.layout, title='Ranking Table')
