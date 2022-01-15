import pandas as pd

import bokeh.models as bk_models
import bokeh.plotting as bk_plotting
import bokeh.palettes as bk_palettes
import bokeh.transform as bk_transform

import bokeh.layouts as bk_layouts
import bokeh.models.widgets as bk_widgets


class SixTeam:

    def __init__(self, data):
        self.data = data
        self.cds_r = None
        self.cds_b = None
        self.plt_pc = None
        self.layout = None
        self.layout = None

    def callback_6t(self, attr, old, new):
        self.layout.children[1] = self.total_6t(new)

    def df_new_6t(self, alliance, match, tasks=['launchOuter', 'launchLower', 'launchInner']):
        df_teams = self.data.schedule[(self.data.schedule.match == match)]
        teams_list = df_teams[(df_teams.alliance == alliance)].team.unique()
        sorted_team = self.data.measures[
        self.data.measures.team.isin(teams_list)]
        sorted_task = sorted_team[sorted_team.task.isin(tasks)]
        grouped = sorted_task.groupby(['task', 'team'])
        grouped = grouped.sum()
        grouped = grouped.drop(columns=grouped.columns[1:5])
        df_unstacked = grouped.unstack()
        df_unstacked.columns = df_unstacked.columns.droplevel()
        df_fil = df_unstacked.fillna(0)
        df_fil.loc['Total PC', :] = list(df_fil.sum())
        return df_fil

    def total_6t(self, match):
        self.cds_r = bk_models.ColumnDataSource(self.df_new_6t("red", match))
        all_teams = list(pd.unique(self.data.schedule.team.sort_values()))
        self.cds_b = bk_models.ColumnDataSource(self.df_new_6t("blue", match))
        r_teams = self.cds_r.column_names[1:4]
        b_teams = self.cds_b.column_names[1:4]
        tasks = self.cds_r.data['task']
        plt_name = "Six Team Power Cells Placed: Match " + match

        self.plt_pc = bk_plotting.figure(title=plt_name, x_range=tasks,
                                         plot_width=700, plot_height=300,
                                         toolbar_location=None, tools="hover",
                                         tooltips="$name- @task: @$name")

        self.plt_pc.vbar_stack(r_teams,
                               x=bk_transform.dodge('task', -0.17,
                                                    range=self.plt_pc.x_range),
                               width=0.3, source=self.cds_r,
                               legend_label=[" " + x for x in r_teams],
                               color=bk_palettes.Reds3)
        self.plt_pc.vbar_stack(b_teams,
                               x=bk_transform.dodge('task', 0.17,
                                                    range=self.plt_pc.x_range),
                               width=0.3, source=self.cds_b,
                               color=bk_palettes.Blues3,
                               legend_label=[" " + x for x in b_teams])
        return self.plt_pc

    def list_matches(self):
        return list(self.data.schedule.match.unique())

    def create_layout(self, match):
        plot_6t = self.total_6t(match)
        match_sel = bk_widgets.Select(title='Match', options=self.list_matches())
        match_sel.on_change('value', self.callback_6t)
        self.layout = bk_layouts.row(match_sel, plot_6t)
        return self.layout

    def panel(self, match):
        layout = self.create_layout(match)
        return bk_models.Panel(child=layout, title='Six Team Charts')

