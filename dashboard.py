import dash
from dash import dcc
from dash import html
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from stockstats import StockDataFrame as Sdf
import yahoo_fin.stock_info as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta
import random

# defining style colors
colors = {"background": "#000000", "text": "#ffFFFF"}

ticker_list = ["TSLA", "GOOGL", "AAPL",  "MSFT", "AMZN"]

# adding css
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

server=app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
        .button1 {
        background-color: #000000 ;
        padding: 8px 6px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        text-weight=bold;
        color: #ffFFFF;
        border-radius: 25px;
        border: 1.5px solid #000000;
        margin=auto;
        position:relative; top:15px; left:20px;
        margin-bottom: 28px;
        margin-right:30px
        }
        .button2 {
        background-color: #0A66C2 ;
        padding: 8px 6px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        text-weight=bold;
        color: #ffFFFF;
        border-radius: 25px;
        border: 1.5px solid #0A66C2;
        margin=auto;
        position:relative; top:15px; left30px;
        margin-bottom: 28px;
        marginh-left=20px
        }
        .button1:hover {
        background-color: #ffFFFF;
        color: #000000;
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
        }
        .button2:hover {
        background-color: #ffFFFF;
        color: #0A66C2;
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
        }
        .button:active {
    
         }
        </style>
    </head>
    <body style="background-color:#ffFFFF;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <button class = "button1" "cursor:pointer" onclick="location.href='https://github.com/shiva-84/live-stock-price-dashboard';"><b>Github</b></button>
        <button class = "button2" "cursor:pointer" onclick="location.href='https://www.linkedin.com/in/priyanshu-katiyar';"><b>Linkedin</b></button>   
        <br>
    </body>
</html>
'''

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.Div(
            [  # header Div
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Header(
                                [
                                    html.H1(
                                        "Live Stock Price Dashboard",
                                        style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                            "font-size" : "45px",
                                            "font-weight" : "650"
                                        },
                                    )
                                ]
                            )
                        )
                    ]
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            [  # Dropdown Div
                dbc.Row(
                    [
                        dbc.Col(  # Tickers
                            dcc.Dropdown(
                                id="stock_name",
                                options=ticker_list,
                                searchable=False,
                                value=str(
                                    random.choice(
                                        [
                                            "TSLA",
                                            "GOOGL",
                                            "AAPL",
                                            "MSFT",
                                            "AMZN",
                                        ]
                                    )
                                ),
                                placeholder="choose stock name",
                            ),
                            width={"size": 3, "offset": 3},
                        ),
                        dbc.Col(  # Graph type
                            dcc.Dropdown(
                                id="chart",
                                options=[
                                    {"label": "line", "value": "Line"},
                                    {"label": "candlestick",
                                        "value": "Candlestick"},
                                    {"label": "simple moving average",
                                        "value": "SMA"},
                                    {
                                        "label": "exponential moving average",
                                        "value": "EMA",
                                    }
                                ],
                                value="Line",
                                style={"color": "#000000"},
                            ),
                            width={"size": 3},
                        ),
                        dbc.Col(  # button
                            dbc.Button(
                                "Apply",
                                size="sm",
                                color="success",
                                id="submit-button",
                                className="mr-1",
                                n_clicks=1,
                            ),
                            width={"size": 3},
                        ),
                    ]
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="graph",
                                config={
                                    "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                },
                            ),
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="live price",
                                config={
                                    "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                },
                            )
                        )
                    ]
                ),
            ]
        ),
    ],
)


# Callback main graph
@app.callback(
    # output
    [Output("graph", "figure"), Output("live price", "figure")],
    # input
    [Input("submit-button", "n_clicks")],
    # state
    [State("stock_name", "value"), State("chart", "value")],
)
def graph_generator(n_clicks, ticker, chart_name):

    if n_clicks >= 1:  # Checking for user to click submit button

        # loading data
        start_date = datetime.now().date() - timedelta(days=5 * 365)
        end_data = datetime.now().date()
        df = yf.get_data(
            ticker, start_date=start_date, end_date=end_data, interval="1d"
        )
        stock = Sdf(df)

        # selecting graph type

        # line plot
        if chart_name == "Line":
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(df.index), y=list(df.close), fill="tozeroy", name="close"
                    )
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=5, label="5D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(step="all"),
                        ]
                    ),
                ),
            )

        # Candelstick
        if chart_name == "Candlestick":
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=list(df.index),
                        open=list(df.open),
                        high=list(df.high),
                        low=list(df.low),
                        close=list(df.close),
                        name="Candlestick",
                    )
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=5, label="5D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(step="all"),
                        ]
                    ),
                ),
            )

        # simple moving average
        if chart_name == "SMA":
            close_ma_10 = df.close.rolling(10).mean()
            close_ma_15 = df.close.rolling(15).mean()
            close_ma_30 = df.close.rolling(30).mean()
            close_ma_100 = df.close.rolling(100).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ma_10.index), y=list(close_ma_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_15.index), y=list(close_ma_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_30.index), y=list(close_ma_15), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_100.index), y=list(close_ma_15), name="100 Days"
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=5, label="5D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(step="all"),
                        ]
                    ),
                ),
            )

        # exponential moving average
        if chart_name == "EMA":
            close_ema_10 = df.close.ewm(span=10).mean()
            close_ema_15 = df.close.ewm(span=15).mean()
            close_ema_30 = df.close.ewm(span=30).mean()
            close_ema_100 = df.close.ewm(span=100).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ema_10.index), y=list(close_ema_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_15.index), y=list(close_ema_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_30.index), y=list(close_ema_30), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_100.index),
                        y=list(close_ema_100),
                        name="100 Days",
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list(
                        [
                            dict(count=5, label="5D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(step="all"),
                        ]
                    ),
                ),
            )

    end_date = datetime.now().date()
    start_date = datetime.now().date() - timedelta(days=2)
    res_df = yf.get_data(
        ticker, start_date=start_date, end_date=end_date, interval="1d"
    )
    price = yf.get_live_price(ticker)
    prev_close = res_df.close.iloc[0]

    live_price = go.Figure(
        data=[
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=price,
                mode="number+delta",
                title={"text": "Price (USD)"},
                delta={"reference": prev_close},
            )
        ],
        layout={
            "height": 300,
            "showlegend": True,
            "plot_bgcolor": colors["background"],
            "paper_bgcolor": colors["background"],
            "font": {"color": colors["text"]},
        },
    )

    return fig, live_price


if __name__ == "__main__":
    app.run_server(debug=True)
