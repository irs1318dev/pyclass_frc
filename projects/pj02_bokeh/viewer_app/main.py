import sys
print(sys.path)

import bokeh.plotting as bk_plt
import bokeh.models as bk_models

import data_source
import sixteam
import rankingtable
import pointschart
import oneteam
import file_management

data_source = data_source.DataSource(fname= 'vif.pickle')

panels = []

file_manager = file_management.DataFile(data_source)
panels.append(file_manager.panel_file_management())

sixteam = sixteam.SixTeam(data_source)
panels.append(sixteam.panel('001-q'))

oneteam_tasks = ['launchOuter', 'climbPosition']
oneteam = oneteam.OneTeam(data_source)
panels.append(oneteam.panel_1t('1318', ['launchOuter', 'launchLower']))

rankingtable = rankingtable.rankingTable(data_source)
panels.append(rankingtable.panel())

pointschart = pointschart.pointsChart(rankingtable.df_ranktable())
panels.append(pointschart.panel())

tabs = bk_models.Tabs(tabs=panels)
bk_plt.curdoc().add_root(tabs)


