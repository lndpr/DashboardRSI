import yfinance as yf
import talib
import pandas as pd
import dash
import dash_html_components as html
import dash_table

# buat list pair
pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X",
         "NZDUSD=X", "USDCHF=X", "EURJPY=X", "EURGBP=X", "EURCHF=X",
         "AUDJPY=X", "GBPJPY=X", "CHFJPY=X", "EURAUD=X", "EURCAD=X", "GC=F"]

# buat list timeframe
timeframes = ["30m", "1h", "1d", "1wk", "1mo"]

# buat dictionary untuk menampung hasil
data = {tf: [] for tf in timeframes}

# ambil data dari yfinance
for pair in pairs:
    for tf in timeframes:
        if tf == "1d":
            period = "3mo"
        elif tf == "1wk":
            period = "1y"
        elif tf == "1mo":
            period = "5y"
        else:
            period = "1mo"
        group_by = "ticker"
        if tf == "1wk":
            group_by = "auto"
        elif tf in ["1mo"]:
            group_by = "time"
        # load data dari yfinance
        df = yf.download(pair, interval=tf, period=period, group_by=group_by)
        df["Close"] = df["Adj Close"]
        
        # hitung RSI 14 dan RSI 30
        rsi14 = talib.RSi(df["Close"], timeperiod=14)
        rsi30 = talib.RSi(df["Close"], timeperiod=30)
        print(f"{pair} {tf}: RSI14: {rsi14.iloc[-1]}")
        print(f"{pair} {tf}: RSI30: {rsi30.iloc[-1]}")
        
        # tentukan tren bullish, bearish, atau sideways
        if rsi14.iloc[-1] > rsi30.iloc[-1]:
            trend = "Up"
        elif rsi14.iloc[-1] < rsi30.iloc[-1]:
            trend = "Down"
        else:
            if 45 <= rsi14.iloc[-1] <= 55 and 45 <= rsi30.iloc[-1] <= 55:
                trend = "Sideways"
            else:
                trend = ""
        print(f"{pair} {tf}: Trend: {trend}")
        
        data[tf].append({"Pair": pair, tf.upper(): trend})

# buat dataframe dari data
df = pd.DataFrame(data["30m"])

# tambahkan kolom-kolom untuk setiap timeframe
for tf in timeframes[1:]:
    df = df.merge(pd.DataFrame(data[tf]), on="Pair")

# buat table dari dataframe
table = dash_table.DataTable(
    id="table",
    columns=[{"name": col, "id": col} for col in df.columns],
    data=df.to_dict("records"),
    style_cell={
        "textAlign": "center",
        "font_size": "16px",
        "font_family": "Calibri"
    },
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold"
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)"
        },
        {
            "if": {"column_id": "Pair"},
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "30M",
                "filter_query": "{30M} eq 'Up'"
            },
            "backgroundColor": "#1f77b4",
            "color": "white"
        },
        {
            "if": {
                "column_id": "30M",
                "filter_query": "{30M} eq 'Down'"
            },
            "backgroundColor": "#d62728",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1H",
                "filter_query": "{1H} eq 'Up'"
            },
            "backgroundColor": "#1f77b4",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1H",
                "filter_query": "{1H} eq 'Down'"
            },
            "backgroundColor": "#d62728",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1D",
                "filter_query": "{1D} eq 'Up'"
            },
            "backgroundColor": "#1f77b4",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1D",
                "filter_query": "{1D} eq 'Down'"
            },
            "backgroundColor": "#d62728",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1WK",
                "filter_query": "{1WK} eq 'Up'"
            },
            "backgroundColor": "#1f77b4",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1WK",
                "filter_query": "{1WK} eq 'Down'"
            },
            "backgroundColor": "#d62728",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1MO",
                "filter_query": "{1MO} eq 'Up'"
            },
            "backgroundColor": "#1f77b4",
            "color": "white"
        },
        {
            "if": {
                "column_id": "1MO",
                "filter_query": "{1MO} eq 'Down'"
            },
            "backgroundColor": "#d62728",
            "color": "white"
        },
    ]
)

# buat aplikasi dash
app = dash.Dash(__name__)

# tambahkan table ke dalam layout
app.layout = dash.html.Div([
    dash.html.H1("OUTLOOK TREND MATARY", style={"textAlign": "center"}),
    table,
    dash.html.Br(), # tambahakn baris kosong
    dash.html.P("Outlook pada dashboard ini dapat membantu trader dalam menentukan arah trend dan mengambil keputusan transaksi yang tepat.", style={"textAlign": "center"}),
    dash.html.P("Terutama karena dashboard ini menggunakan indikator RSI (Relative Strength Index) yang dapat mengukur kekuatan trend.", style={"textAlign": "center"})
],
    style={"max-width": "850px", "margin": "auto"}
)


if __name__ == "__main__":
    app.run_server(debug=True)
