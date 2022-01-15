import viewer_app.oneteam as va_oneteam
import viewer_app.sixteam as va_sixteam
import viewer_app.data_source as va_data_source
import pandas as pd


def test_oneteam():
    data = va_data_source.DataSource(event='test_event_2', season='2020')
    oneteam = va_oneteam.OneTeam(data)
    assert isinstance(oneteam.data.measures, pd.DataFrame)
    assert isinstance(oneteam.data.schedule, pd.DataFrame)
    assert oneteam.data.measures.shape[1] == 20
    assert len(oneteam.list_teams()) > 15
    plot = oneteam.plot_1t('1318')
    assert isinstance(oneteam.df_new_1t('1318'), pd.DataFrame)

def test_noshow():
    data = va_data_source.DataSource(event='test_event_2', season='2020')
    oneteam = va_oneteam.OneTeam(data)
    plot = oneteam.total_1t('1318', ['noShow'])

def test_sixteam():
    data = va_data_source.DataSource(event='wasno', season='2020')
    sixteam = va_sixteam.SixTeam(data)
    print(sixteam.data.schedule)
    # plot = sixteam.total_1t('1318', ['noShow'])
    print(sixteam.df_new_6t('red', '010-q'))
