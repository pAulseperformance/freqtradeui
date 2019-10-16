import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random

from rest_client import load_config, FtRestClient, main

def start_bot():
    config = load_config("config.json")
    url = config.get("api_server", {}).get("server_url", "127.0.0.1")
    port = config.get("api_server", {}).get("listen_port", "8080")
    username = config.get("api_server", {}).get("username")
    password = config.get("api_server", {}).get("password")

    server_url = f"http://{url}:{port}"
    client = FtRestClient(server_url, username, password)
    return client

client = start_bot()


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Div(children="Something to graph:"),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    print(input_data)
    # response = client.daily()
    response =  [['2019-10-12', '1.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-11', '200.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-10', '-150.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-09', '25.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-08', '22.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-07', '2.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-06', '12.00000000 USDT', '0.000 USD', '0 trade']]


    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [i[0] for i in response], 'y': [float(i[1].split(' ')[0]) for i in response], 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)
