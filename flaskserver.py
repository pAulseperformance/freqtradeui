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

data_dict = {'performance': client.performance(),
             'daily': ['hi']}

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H2('Free Trader',
                style={'float': 'left',
                       }
                ),
    ]),
    dcc.Dropdown(id='forward-trader-graph-options',
                 options=[{'label': s, 'value': s} for s in data_dict.keys()],
                 value=['daily'],
                 multi=True,
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=0),
], className='container', style={'width': '98%', 'margin-left': 10, 'margin-right': 10})


@app.callback(
    Output(component_id='graphs', component_property='children'),
    [Input(component_id='forward-trader-graph-options', component_property='value'),
     Input(component_id='graph-update', component_property='n_intervals')]
)
def update_graph(input_data, n):
    # response = client.daily()
    response =  [['2019-10-12', '1.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-11', '200.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-10', '-150.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-09', '25.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-08', '22.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-07', '2.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-06', '12.00000000 USDT', '0.000 USD', '0 trade']]
    graphs = []
    for input in input_data:
        data = go.Scatter()
        if input == 'daily':
            print('Inside Daily')
            # response = client.daily()
            data = go.Scatter(
                x = [i[0] for i in response],
                y = [float(i[1].split(' ')[0]) for i in response],
                name = 'scatter',
                fill = 'tozeroy',
                fillcolor = '#6897bb'
            )
        if input == 'performance':
            print('inside Performance ')
            data = go.Scatter(
                x = [1,2,3,4,5,6,7],
                y = [random.uniform(1,2)*1 for i in range(8)],
                name = 'scatter',
                fill = 'tozeroy',
                fillcolor = '#6897bb'
            )

        graphs.append(html.Div(dcc.Graph(
            id=input,
            animate=True,
            figure={'data': [data],
                    'layout': go.Layout(
                        title='{}'.format(input)
                    )
                    }
        )))

    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)
