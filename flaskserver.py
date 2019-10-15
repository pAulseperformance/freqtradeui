from flask import Flask, render_template, request, redirect, url_for, flash
from rest_client import load_config, FtRestClient, main
import inspect
import dash
from reusablecompents import test_layout
server = Flask(__name__)
server.secret_key = 'changthiswhendepoloying!'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Configure Dash App
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets,
    routes_pathname_prefix='/dash/'
)

app.layout = test_layout


@server.route('/', methods=['GET', 'POST'])
def index():
    client = start_bot()
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
            response = getattr(client, command)() #(*args["command_arguments"])
            flash(response)
            # if command == 'daily':
            #     response = parse_daily(response)

            return render_template('index.html', graphdata=response)
            # return render_template('index.html', data=response)
            # return redirect(url_for('index'))

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


if __name__ == '__main__':
    # server.run(debug=True)  # Just for Flask Standalone
    app.run_server(debug=True)

