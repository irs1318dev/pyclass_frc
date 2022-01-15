import os
import os.path

import pandas as pd

import viewer_app.data_source as va_data_source
import viewer_app.oneteam as va_oneteam

test_event_name = 'wasno'
test_season = '2020'
test_file_name = r'\data_write_test.pickle'


def test_data_source():
    data = va_data_source.DataSource(event=test_event_name,
                                     season=test_season)
    assert isinstance(data, va_data_source.DataSource)
    assert isinstance(data.measures, pd.DataFrame)
    assert data.measures.shape[0] > 1000
    assert data.measures.shape[1] == 20

    assert isinstance(data.schedule, pd.DataFrame)
    assert isinstance(data.teams, pd.DataFrame)
    assert data.teams.shape[1] == 8
    assert data.teams.shape[0] > 20

    assert data.event == test_event_name
    assert data.season == test_season


def test_write_file():
    path = os.path.abspath(__file__)
    for _ in range(4):
        path = os.path.dirname(path)
    data = va_data_source.DataSource(event=test_event_name,
                                     season=test_season)
    fpath = path + test_file_name
    data.write_file(fpath)
    file_data = va_data_source.DataSource(fpath)
    os.remove(fpath)
    assert isinstance(file_data, va_data_source.DataSource)
    assert file_data.event == test_event_name
    assert file_data.season == test_season
    assert not file_data.from_sql
    assert isinstance(file_data.status, pd.DataFrame)


def test_write_vif():
    path = os.path.abspath(__file__)
    for _ in range(4):
        path = os.path.dirname(path)
    data = va_data_source.DataSource(event=test_event_name,
                                     season=test_season)
    fpath = path + r'\vif.pickle'
    data.write_file(fpath)

def test_panel():
    data = va_data_source.DataSource(event=test_event_name,
                                     season=test_season)
    oneteam = va_oneteam.OneTeam(data)
    panel = oneteam.panel_1t('1318', ['launchOuter', 'climbPosition'])


def test_enum_measures():
    data = va_data_source.DataSource(event=test_event_name,
                                     season=test_season)
    enum_meas = data._enum_preprocess()


def test_num_teams():
    data = va_data_source.DataSource(event=test_event_name, season=test_season)
    print()
    print(data.teams)

def test_multiselect():
    data = va_data_source.DataSource(event=test_event_name, season=test_season)
    assert isinstance(data.enum_tasks, list)
    assert len(data.enum_tasks) > 7
    assert 'launchLower' in data.enum_tasks

    oneteam = va_oneteam.OneTeam(data)
    layout = oneteam.layout_1t('2046', ['launchLower'])
