from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go

import plotly.io as pio

from datetime import datetime


class LiveDatetimeValuePlot:

    def __init__(self, data_reference, graph_id,
                       plot_styles):
        self.data_reference = data_reference
        self.graph_id = graph_id
        self.plot_styles = plot_styles
    


    def register_callback(self, dash_app_reference):
        dash_app_reference.callback(
            Output(self.graph_id, 'figure'),
            [Input(self.graph_id+'-update', 'n_intervals')])(self.update_graph)


    def get_dash_plot(self):


        return html.Div(
                [
                    dcc.Graph(id = self.graph_id, animate = True, style={"margin":5}),
                    dcc.Interval(
                        id = self.graph_id+"-update",
                        interval = 1000,
                        n_intervals = 0
                    )
                    ],style={"border":"1px solid", "border-radius": 7.5,"backgroundColor": pio.templates[self.plot_styles.get("template")].layout["paper_bgcolor"], "margin": 10}
            )

    
    def update_graph(self, _):
        data = self.data_reference.get_data()

        plot_data = go.Scatter(
			    x = data["datetimes"],
			    y = data["values"],
			    name ='Scatter',
                mode = self.plot_styles.get("scatter_style")
		)
        
        layout = go.Layout( xaxis=dict(range=[self.data_reference.get_minimum_date(), datetime.now()]),
                            yaxis=dict(range=self.plot_styles.get("yrange")), 
                            template=self.plot_styles.get("template"),
                            title=self.plot_styles.get("title"))

        
        return {"data": [plot_data], "layout": layout}


