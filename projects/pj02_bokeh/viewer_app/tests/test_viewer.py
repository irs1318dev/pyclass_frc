import pandas as pd

import viewer_app.sixteam as svv
import server.model.event as sme
import viewer_app.data_source as va_data_source

data_source = va_data_source.DataSource(event='wasno',
                                            season='2020')

def test_viewer():
    viewer = svv.SixTeam(data_source)
    evt = sme.EventDal.get_current_event()
    assert evt[1] == 'wasno'
    assert evt[2] == '2020'

    assert viewer.measures.shape[0] > 1000
    assert viewer.measures.shape[1] == 20
    assert isinstance(viewer.schedule, pd.DataFrame)
    assert isinstance(viewer.teams, pd.DataFrame)
    matches = viewer.list_matches()
    assert len(matches) > 10
    assert matches[0] == '001-q'
