from flask import Flask, render_template, request, redirect, url_for, flash
from rest_client import load_config, FtRestClient, main
import inspect
import dash
from reusablecompents import test_layout

server = Flask(__name__)
server.secret_key = 'changthiswhendepoloying!'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Configure Dash App
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets, routes_pathname_prefix='/dash/')


@server.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        m = [x for x, y in inspect.getmembers(client) if not x.startswith('_')]
        command = request.form['command'].lower()
        if command not in m:
            # logger.error(f"Command {command} not defined")
            for x, y in inspect.getmembers(client):
                if not x.startswith('_'):
                    flash(f"{x} {getattr(client, x).__doc__}")
            return redirect(url_for('index'))
        else:
            response = getattr(client, command)()  # (*args["command_arguments"])
            flash(response)
            # if command == 'daily':
            #     response = parse_daily(response)

            # return render_template('index.html', graphdata=response)
            # return render_template('index.html', data=response)
            return redirect(url_for('index'))

    return render_template('index.html')
@server.route('/forcebuy')
def force_buy():
    response = client.forcebuy('ETH/USDT')
    flash(response)
    return render_template('index.html')

@server.route('/forcesell/<int:id>')
def force_sell(id):
    response = client.forcesell(id)
    flash(response)
    return render_template('index.html')


def start_bot():
    config = load_config("config.json")
    url = config.get("api_server", {}).get("server_url", "127.0.0.1")
    port = config.get("api_server", {}).get("listen_port", "8080")
    username = config.get("api_server", {}).get("username")
    password = config.get("api_server", {}).get("password")

    server_url = f"http://{url}:{port}"
    client = FtRestClient(server_url, username, password)
    return client


def daily_layout(response):
    import dash_core_components as dcc
    import dash_html_components as html
    # import plotly.graph_objects as go
    import plotly.graph_objs as go

    data = [['2019-10-12', '1.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-11', '200.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-10', '-150.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-09', '25.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-08', '22.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-07', '2.00000000 USDT', '0.000 USD', '0 trade'],
            ['2019-10-06', '12.00000000 USDT', '0.000 USD', '0 trade']]
    # name = data[0][1].split(' ')[1])
    xaxis = [i[0] for i in data]
    yaxis = [float(i[1].split(' ')[0]) for i in data]
    layout = dcc.Graph(figure=go.Figure(
        data=[go.bar(x=[2], y=[1], name='ust')])

    )
    return layout

app.layout = test_layout
client = start_bot()

if __name__ == '__main__':
    # server.run(debug=True)  # Just for Flask Standalone
    app.run_server(debug=True)
