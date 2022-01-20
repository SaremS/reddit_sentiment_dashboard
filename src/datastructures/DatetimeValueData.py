from collections import deque
from datetime import datetime

class DatetimeValueData:

    def __init__(self, maxlen = 3600):
        self._datetime_data = deque(maxlen = maxlen)
        self._value_data = deque(maxlen = maxlen)

    def __len__(self):
        return len(self._datetime_data)

    def append(self, value):
        if value is not None:
            self._datetime_data.append(datetime.now())
            self._value_data.append(value)

    def get_data(self):
        return {"datetimes": list(self._datetime_data),
                "values": list(self._value_data)}

    def get_minimum_date(self):
        if self.__len__()>0:
            return self._datetime_data[0]
        else:
            return datetime.now()

    def aggregate_moving_filter(self, aggregation_function, filter_seconds = 300, empty_filter_value=None):
        now = datetime.now()
        data = [val for (dt, val) in zip(self._datetime_data, self._value_data) if (now-dt).seconds <= filter_seconds]

        if len(data)>0:
            return aggregation_function(data)
        else:
            return empty_filter_value
    
        
