"""Uses data to generate one team graphs.
"""
import bokeh.models as bk_models
import bokeh.plotting as bk_plotting
import bokeh.layouts as bk_layouts
import bokeh.models.widgets as bk_widgets
import bokeh.palettes as bk_palettes
import pandas as pd


class OneTeam:

    def __init__(self, data):
        self.data = data
        self.cds = None
        self.pcplot = None
        self.layout = None
        self.tasks = None
        self.team_sel = None
        self.task_sel = None

    def team_callback(self, attr, old, new):
        self.layout.children[1] = self.total_1t(new, self.task_sel.value)

    def button_callback(self):
        self.layout.children[1] = self.total_1t(self.team_sel.value,
                                                self.task_sel.value)

    def df_new_1t(self, team, tasks):
        self.tasks = tasks
        measures = self.data.enum_measures[
            (self.data.enum_measures.team == team) &
            (self.data.enum_measures.task.isin(tasks))].copy()

        # get matches
        grouped = measures.groupby(['match', 'task'])
        grouped = grouped.sum()
        grouped = grouped.drop(columns=grouped.columns[1:5])
        grouped = grouped['successes']
        df_unstacked = grouped.unstack()
        df_fil = df_unstacked.fillna(0)
        return df_fil

    def total_1t(self, team, tasks):
        self.cds = bk_models.ColumnDataSource(self.df_new_1t(team, tasks))
        tasks = self.cds.column_names
        tasks = tasks[1:]
        matches = self.cds.data['match']
        plt_title = "Team " + team
        num_tasks = len(tasks)
        if num_tasks == 0:
            colors=[]
        elif num_tasks == 1:
            colors = ['#5900b3']
        elif num_tasks == 2:
            colors = ['#5900b3', '#e6b800']
        else:
            colors = bk_palettes.Category20[len(tasks)]
        self.pcplot = bk_plotting.figure(x_range=matches, plot_height=250,
                                         title=plt_title, tools="hover",
                                         tooltips="$name: @$name")

        glyphs = self.pcplot.vbar_stack(tasks, x='match', width=0.4,
                               source=self.cds, color=colors)
        legend_items = [(tasks[i], [glyphs[i]])
                        for i in range(0, len(tasks), 1)]
        legend = bk_models.Legend(items=legend_items, location='center')
        self.pcplot.add_layout(legend, 'right')
        return self.pcplot

    def list_teams(self):
        return list(self.data.schedule.team.unique())

    def layout_1t(self, team, tasks):
        self.total_1t(team, tasks)

        self.team_sel = bk_widgets.Select(title='Match',
                                          options=self.list_teams(),
                                          value=team)
        self.team_sel.on_change('value', self.team_callback)
        self.task_sel = bk_widgets.MultiSelect(title='Tasks',
                                               options=self.data.enum_tasks,
                                               size=40, value=tasks)

        btn = bk_widgets.Button(label='Update')
        btn.on_click(self.button_callback)

        col_layout = bk_layouts.column(self.team_sel, self.task_sel, btn)
        self.layout = bk_layouts.row(col_layout, self.pcplot)
        return self.layout

    def panel_1t(self, team, tasks):
        self.layout_1t(team, tasks)
        return bk_models.Panel(child=self.layout,
                               title='One Team Charts')
