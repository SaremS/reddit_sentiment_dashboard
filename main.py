from src.datastructures.DatetimeValueData import DatetimeValueData
from src.datastructures.DatetimeValueStringData import DatetimeValueStringData

from src.models.RobertaSentimentModel import RobertaSentimentModel

from src.utils.EnvironmentVariableHelper import EnvironmentVariableHelper 
from src.utils.PlotStyleHelper import PlotStyleHelper

from src.workers.MovingAverageWorker import MovingAggregationWorker
from src.workers.RedditSentimentWorker import RedditSentimentWorker

from src.dashplots.LiveDatetimeValuePlot import LiveDatetimeValuePlot
from src.dashplots.LiveTable import LiveTable

from dash import html

import dash
import dash_bootstrap_components as dbc

import plotly.io as pio


class LiveDashboard:
   

    live_data = DatetimeValueStringData() 
    ma_data  = DatetimeValueData()
    volume_data = DatetimeValueData()

    environment_variable_helper = EnvironmentVariableHelper()
    
    sentiment_model = RobertaSentimentModel()
    sentiment_model.init_model()
      
    reddit_sentiment_worker  = RedditSentimentWorker(sentiment_model, environment_variable_helper, live_data)
    moving_average_worker = MovingAggregationWorker(live_data, ma_data, lambda x: sum(x)/len(x),filter_seconds=60)
    moving_volume_worker = MovingAggregationWorker(live_data, volume_data, lambda x: len(x), filter_seconds=60, empty_filter_value=0)



    def __init__(self):
        
        self.dash_app = self.init_dash_app()
        self.reddit_sentiment_worker.start()
        self.moving_average_worker.start()
        self.moving_volume_worker.start()

    
    
    def init_dash_app(self):

        app = dash.Dash(__name__,
                        meta_tags=[], external_stylesheets=[dbc.themes.BOOTSTRAP]) 
       

        
        live_data_plot = LiveDatetimeValuePlot(self.live_data, "live-data", PlotStyleHelper(title="Reddit Live sentiment for r/{}".format(self.environment_variable_helper.get_target_subreddit())))
        live_data_plot.register_callback(app)

        ma_data_plot = LiveDatetimeValuePlot(self.ma_data, "ma-data",PlotStyleHelper(title="60 seconds sentiment Moving Average", scatter_style="lines"))
        ma_data_plot.register_callback(app)

        vol_data_plot = LiveDatetimeValuePlot(self.volume_data, "vol-data", PlotStyleHelper(title="60 second volume", yrange=[0,50], scatter_style="lines"))
        vol_data_plot.register_callback(app)

        live_data_table = LiveTable(self.live_data, "live-table", PlotStyleHelper())
        live_data_table.register_callback(app)

        app.layout = html.Div([dbc.Row([dbc.Col([live_data_plot.get_dash_plot(),
                               ma_data_plot.get_dash_plot(),
                               vol_data_plot.get_dash_plot()],width=7,md=8),
                               dbc.Col([live_data_table.get_dash_table()], width=5,md=4)])])


        return app



if __name__ == '__main__':
    dashboard = LiveDashboard()
    dashboard.dash_app.run_server(debug=True,host="0.0.0.0", port=5555)
