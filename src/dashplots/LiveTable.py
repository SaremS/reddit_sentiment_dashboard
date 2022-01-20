from dash import html, dcc
from dash import dash_table
import plotly.graph_objs as go
from dash import Input, Output

import plotly.io as pio

from datetime import datetime


class LiveTable:

    def __init__(self, data_reference, graph_id, plot_styles,n_items=20):
        self.data_reference = data_reference
        self.graph_id = graph_id
        self.plot_styles = plot_styles
        self.n_items = n_items

        self.backgroundColor = pio.templates[self.plot_styles.get("template")].layout["paper_bgcolor"]
    


    def register_callback(self, dash_app_reference):
        dash_app_reference.callback(
            Output(self.graph_id, 'data'),
            [Input(self.graph_id+'-update', 'n_intervals')])(self.update_table)


    def get_dash_table(self):


        return html.Div(
                [dash_table.DataTable(id=self.graph_id,data=[{}],columns=[{"id":"datetimes","name":"Time"},
                                                                          {"id":"strings","name":"Text"},
                                                                          {"id":"values","name":"Sentiment"}],
                                                                          style_cell={"backgroundColor":self.backgroundColor,"color":"white"}, style_data={'height':'auto', "whiteSpace": "normal"}),
                 dcc.Interval(
                    id = self.graph_id+"-update",
                    interval = 1000,
                    n_intervals = 0 
                 )
                 ],style={"border":"1px solid", "border-radius": 7.5,"backgroundColor": self.backgroundColor, "margin":10}
            )

    
    def update_table(self, _):
        data = self.data_reference.get_latest_n_entries(self.n_items)
        return data


