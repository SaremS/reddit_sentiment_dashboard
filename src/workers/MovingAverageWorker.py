import threading
from datetime import datetime
import time
from copy import deepcopy


class MovingAggregationWorker(threading.Thread):
    
    def __init__(self, live_data_reference, ma_data_reference, aggregation_function, update_interval_seconds=1, filter_seconds=300, empty_filter_value=None):

        super(MovingAggregationWorker, self).__init__()

        self.live_data_reference = live_data_reference
        self.ma_data_reference = ma_data_reference
        self.aggregation_function = aggregation_function
        self.update_interval_seconds = update_interval_seconds
        self.filter_seconds = filter_seconds
        self.empty_filter_value = empty_filter_value


    def run(self):

        while True: 
        
            moving_average = self.live_data_reference.aggregate_moving_filter(self.aggregation_function, self.filter_seconds, self.empty_filter_value)
            self.ma_data_reference.append(moving_average)
            
            time.sleep(1)

