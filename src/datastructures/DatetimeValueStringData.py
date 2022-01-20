from collections import deque
from datetime import datetime

class DatetimeValueStringData:

    def __init__(self, maxlen = 3600):
        self._datetime_data = deque(maxlen = maxlen)
        self._value_data = deque(maxlen = maxlen)
        self._string_data = deque(maxlen = maxlen)

    def __len__(self):
        return len(self._datetime_data)

    def append(self, value, string=""):
        if value is not None:
            self._datetime_data.append(datetime.now())
            self._value_data.append(value)
            self._string_data.append(string)

    def get_data(self):
        return {"datetimes": list(self._datetime_data),
                "values": list(self._value_data),
                "strings": list(self._string_data)}

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
   

    def get_latest_n_entries(self, n_items: int = 20):

        datetimes = list(self._datetime_data)[-n_items:]
        values = list(self._value_data)[-n_items:]
        strings = list(self._string_data)[-n_items:]
        
        datetimes_str = [dt.strftime("%m/%d/%Y - %H:%M") for dt in datetimes]
        values_str = [val[:6] if val[0]=="-" else " "+val[:5] for val in map(lambda v: str(v), values)]
        strings_cut = [st[:140] for st in strings] 
        
        return [{"datetimes": datetimes_str[i], "values":values_str[i], "strings":strings_cut[i]} for i in range(len(values))][::-1]
