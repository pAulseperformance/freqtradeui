from flask import Flask, render_template, request, redirect, url_for, flash
from rest_client import load_config, FtRestClient, main
import inspect
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)
app.secret_key = '123'


@app.route('/', methods=['GET', 'POST'])
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
            # flash(response)
            # if command == 'daily':
            #     response = parse_daily(response)

            response = daily_performance(response)
            return render_template('index.html', graphdata=response)
            # return render_template('index.html', data=response)
            # return redirect(url_for('index'))

    data = [['2019-10-12', '0.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-11', '0.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-10', '0.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-09', '0.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-08', '0.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-07', '0.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-06', '0.00000000 USDT', '0.000 USD', '0 trade']]
    return render_template('index.html')


def graph_pygal(response):
    import pygal
    bar_chart = pygal.Bar()
    bar_chart.title = 'Daily Performance'
    bar_chart.x_labels = map(str, range(2002, 2013))
    bar_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    bar_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    bar_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    bar_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    return bar_chart
    # return render_template("graphing.html", graph_data=graph_data)

def daily_performance(response):
    data = [['2019-10-12', '1.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-11', '200.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-10', '-150.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-09', '25.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-08', '22.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-07', '2.00000000 USDT', '0.000 USD', '0 trade'], ['2019-10-06', '12.00000000 USDT', '0.000 USD', '0 trade']]
    import pygal
    bar_chart = pygal.Bar()
    bar_chart.title = 'Daily Performance'
    print(map(str, range(2002,2013)))
    bar_chart.x_labels = map(str, [i[0] for i in data])
    bar_chart.add('USDT', [float(i[1].split(' ')[0]) for i in data])
    # bar_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    # bar_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    # bar_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    # bar_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    return bar_chart



def parse_daily(response):
    import json
    # data: [{x: '2016-12-25', y: 20}, {x: '2016-12-26', y: 10}]
    for day in response:
        # Parse the data
        break
    # data = [{"x": '2016-12-25', "y": 20}, {"x": '2016-12-26', "y": 10}]
    data = [1,2,3,4,5]
    return json.dumps(data)

def start_bot():
    config = load_config("config.json")
    url = config.get("api_server", {}).get("server_url", "127.0.0.1")
    port = config.get("api_server", {}).get("listen_port", "8080")
    username = config.get("api_server", {}).get("username")
    password = config.get("api_server", {}).get("password")

    server_url = f"http://{url}:{port}"
    client = FtRestClient(server_url, username, password)
    return client


def print_commands():
    # Print dynamic help for the different commands using the commands doc-strings
    client = FtRestClient(None)
    print("Possible commands:")
    for x, y in inspect.getmembers(client):
        if not x.startswith('_'):
            flash(f"{x} {getattr(client, x).__doc__}")


@app.route('/chart')
def chart():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=labels)




@app.route('/dashboard/')
def show_dashboard():
    plots = []
    plots.append(make_plot())

    return render_template('dashboard.html', plots=plots)

def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div


if __name__ == '__main__':
    app.run(debug=True)

