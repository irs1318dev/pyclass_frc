import viewer_app.rankingtable as rankingtable
import viewer_app.data_source as va_data_source


def test_rankingtable():
    data_source = va_data_source.DataSource(event='wasno', season='2020')
    rt = rankingtable.rankingTable(data_source)
    rt.panel()
