class PlotStyleHelper:

    def __init__(self, title="", template="plotly_dark", yrange = [-1,1], scatter_style="lines+markers") -> None:
        self.style_dict = {
                "title": title,
                "template": template,
                "yrange": yrange,
                "scatter_style": scatter_style
                }

    def get(self, key:str):
        
        if key=="title":
            return {"text":self.style_dict["title"],
                    "x":0.5,
                    "y":0.95,
                    "font":{"size":30}}

        return self.style_dict[key]

     


