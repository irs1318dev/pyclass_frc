import pandas as pd
import bokeh.plotting
import bokeh.models as bmodels
import bokeh.models.widgets as bmw
import bokeh.layouts as blt
import bokeh.plotting as plt
import bokeh.palettes as bpalettes
import bokeh.transform as btransform
import bokeh.io


class pointsChart:

    def __init__(self, df):
        self.df = df
        self.chart = None
        self.layout = None

    def total_pt(self):
        df_temp = self.df
        df_new = df_temp.filter(['avg_autoOuterPoints', 'avg_autoInnerPoints',
                                 'avg_teleInnerPoints', 'avg_teleLowerPoints',
                                 'avg_teleOuterPoints', 'avg_climbpoints', 'avg_parkpoints'], axis=1)
        points_cds = bmodels.ColumnDataSource(df_new)
        tm_col_name = points_cds.column_names[0]
        task = points_cds.column_names[1:]
        tooltips = [
            ("", "team: @team"),
            ("", "$name: @$name")
        ]
        p = plt.figure(title='Points Chart', x_range=points_cds.data[tm_col_name],
                       plot_width=1100, plot_height=350, tooltips=tooltips, toolbar_location="above")
        hr = p.vbar_stack(task, x=tm_col_name, width=0.5,
                          source=points_cds, color=bpalettes.RdBu7)
        legend = bokeh.models.Legend(items=[(x, [hr[task.index(x)]]) for x in task], location=(0, 0))
        p.add_layout(legend, 'right')
        p.xaxis.major_label_orientation = 3.14 / 4
        self.chart = p
        return self.chart

    def create_layout(self):
        self.chart = self.total_pt()
        self.layout = blt.row(self.chart)
        return self.layout

    def panel(self):
        self.layout = self.create_layout()
        return bmodels.Panel(child=self.layout, title='Points Chart')
