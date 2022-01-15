import viewer_app.data_source as va_data_source
import viewer_app.file_management as va_fm
import pandas as pd

def test_file_manage():
    file = va_fm.DataFile()
    ds = va_data_source.DataSource()
    ds.write_file(fname='test_pickle')
    ds = va_data_source.DataSource('test_pickle')

