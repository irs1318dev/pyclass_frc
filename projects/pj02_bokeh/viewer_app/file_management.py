import bokeh.models as bk_models
import bokeh.models.widgets as bk_widgets
import bokeh.layouts as bk_layouts
import data_source as va_data_source
import bokeh.io


class DataFile:

    def __init__(self, data_source):
        self.update_button = bk_widgets.Button(label='Update graphs')
        self.layout = None
        self.data_source = data_source

    def callback_button(self):
        # ds1 = va_data_source.DataSource(event='test_event_2', season='2020')
        # check boolean attribute in data_source to see whether it's from a file or sql
        if not self.data_source.from_sql:
            bokeh.io.output_file('file_input.html')

            file_input = bk_widgets.FileInput()
            bokeh.io.show(file_input)
            self.data_source.refresh(fname=file_input.filename)

        else:
            self.data_source.refresh()
        # for obj in self.data_source:
        #     obj = ds1

    def layout_file_management(self):
        btn = bk_widgets.Button(label='Update graphs')
        btn.on_click(self.callback_button)
        self.layout = bk_layouts.row(btn)
        return self.layout

    def panel_file_management(self):
                              # list_objects):
        self.layout_file_management()
            # list_objects)
        return bk_models.Panel(child=self.layout,
                               title='File Management')
